"""
Audio Generator Engine for DarkSky Whisperer.
Integrates with ElevenLabs API to generate high-fidelity, whispered late-night narration,
with automated offline caching and browser Web Audio fallback.
"""

import os
import hashlib
from typing import Optional, Dict, Any
from pathlib import Path

# Voice IDs suited for deep, calm nighttime astronomical narration
# 'George' or 'Adam' or 'Callum' in ElevenLabs standard library
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # George (Deep, soothing British narrator)
MODEL_ID = "eleven_multilingual_v2"

AUDIO_CACHE_DIR = Path(__file__).resolve().parent.parent / "audio_cache"
AUDIO_CACHE_DIR.mkdir(exist_ok=True, parents=True)


class AudioNarrator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "")
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initializes ElevenLabs client if API key is present."""
        if self.api_key:
            try:
                from elevenlabs.client import ElevenLabs
                self.client = ElevenLabs(api_key=self.api_key)
            except Exception as e:
                print(f"[AudioNarrator] Warning initializing ElevenLabs: {e}")
                self.client = None
        else:
            self.client = None

    def synthesize_speech(self, text: str, voice_id: str = DEFAULT_VOICE_ID) -> Dict[str, Any]:
        """
        Synthesizes speech into an MP3 file, caching on disk to support 100% offline trail playback.
        Returns metadata including local URL and fallback instructions.
        """
        # Create deterministic hash for caching
        text_hash = hashlib.md5(f"{voice_id}:{text}".encode("utf-8")).hexdigest()
        filename = f"stargaze_{text_hash[:12]}.mp3"
        cached_path = AUDIO_CACHE_DIR / filename

        # Return cached audio if already generated
        if cached_path.exists() and cached_path.stat().st_size > 100:
            return {
                "success": True,
                "audio_url": f"/audio/{filename}",
                "cached": True,
                "provider": "ElevenLabs (Cached)",
                "filename": filename,
            }

        # Generate via ElevenLabs if credentials exist
        if self.client:
            try:
                audio_stream = self.client.text_to_speech.convert(
                    voice_id=voice_id,
                    optimize_streaming_latency="0",
                    output_format="mp3_44100_128",
                    text=text,
                    model_id=MODEL_ID,
                    voice_settings={
                        "stability": 0.65,
                        "similarity_boost": 0.85,
                        "style": 0.20,
                        "use_speaker_boost": True
                    }
                )
                with open(cached_path, "wb") as f:
                    for chunk in audio_stream:
                        if chunk:
                            f.write(chunk)

                return {
                    "success": True,
                    "audio_url": f"/audio/{filename}",
                    "cached": False,
                    "provider": "ElevenLabs",
                    "filename": filename,
                }
            except Exception as e:
                print(f"[AudioNarrator] ElevenLabs synthesis error: {e}")

        # Web Speech API / local browser synthesizer fallback
        return {
            "success": False,
            "audio_url": None,
            "cached": False,
            "provider": "Web Speech Synthesizer (Zero-key offline fallback)",
            "message": "Using browser Web Speech API with nighttime cadence.",
            "text": text
        }


if __name__ == "__main__":
    narrator = AudioNarrator()
    print("ElevenLabs Configured:", narrator.client is not None)
    res = narrator.synthesize_speech("Look up toward the North Star, resting gently above the horizon.")
    print("Synthesis result:", res)
