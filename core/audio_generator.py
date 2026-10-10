"""
Audio Generator Engine for Whispers of the Sky (WOTS).
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
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "sk_fd6721c4b684df60389d7e10d3d7e421e75c00dca92afbec")

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
                "provider": "ElevenLabs Studio Voice (Cached)",
                "filename": filename,
            }

        # Generate via direct ElevenLabs REST API
        if self.api_key:
            try:
                import urllib.request
                import json
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                payload = json.dumps({
                    "text": text,
                    "model_id": MODEL_ID,
                    "voice_settings": {
                        "stability": 0.75,
                        "similarity_boost": 0.85,
                        "style": 0.15,
                        "use_speaker_boost": True
                    }
                }).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=payload,
                    headers={"xi-api-key": self.api_key, "Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=25) as resp:
                    audio_data = resp.read()
                    with open(cached_path, "wb") as f:
                        f.write(audio_data)

                return {
                    "success": True,
                    "audio_url": f"/audio/{filename}",
                    "cached": False,
                    "provider": "ElevenLabs Studio Voice (George)",
                    "filename": filename,
                }
            except Exception as e:
                print(f"[AudioNarrator] ElevenLabs HTTP synthesis error: {e}")

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
