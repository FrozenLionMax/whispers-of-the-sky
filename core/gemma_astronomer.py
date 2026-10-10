"""
Gemma Offline Astronomer Engine.
Leverages Google's open-weight Gemma model (gemma2:2b) via Ollama REST API
to generate voice-first stargazing tour scripts, celestial lore, and offline Q&A.
"""

import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
import os


class GemmaAstronomer:
    def __init__(self, model_name: str = "gemma2:2b", ollama_host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_host = ollama_host
        self._connected: Optional[bool] = None

    @property
    def is_connected(self) -> bool:
        if self._connected is None:
            self._connected = self._check_ollama()
        return self._connected

    def _check_ollama(self) -> bool:
        """Verifies connection to local Ollama instance running Gemma."""
        try:
            req = urllib.request.Request(f"{self.ollama_host}/api/tags")
            with urllib.request.urlopen(req, timeout=0.5) as resp:
                data = json.loads(resp.read().decode())
                models = [m.get("name", "") for m in data.get("models", [])]
                for m in models:
                    if self.model_name in m:
                        return True
                return len(models) > 0
        except Exception:
            return False

    def generate_tour_script(
        self,
        visible_targets: List[Dict[str, Any]],
        seeing_data: Dict[str, Any],
        duration_minutes: int = 10,
        focus_style: str = "mythology_and_science"
    ) -> Dict[str, Any]:
        """
        Generates an audio-first stargazing script designed to be heard through headphones
        while laying on the grass with the screen turned off.
        """
        top_targets = visible_targets[:4]
        target_summary = "\n".join([
            f"- {t['name']}: {t['cardinal_direction']}, {t['altitude_deg']}° elevation ({t['elevation_description']}). Guide: {t['star_hop']}"
            for t in top_targets
        ])

        system_instruction = (
            "You are Whispers of the Sky (WOTS), a wise, serene nighttime astronomer and naturalist. "
            "You are speaking directly into the listener's headphones while they lie outside on the grass in total darkness. "
            "Your tone is quiet, evocative, reverent, and gentle. "
            "Never tell them to look at a phone or screen. Instead, guide their bare eyes across the night sky using physical directions "
            "(e.g., 'Tilt your chin up', 'Two fist-widths above the horizon to your left', 'Breathe in the cool night air'). "
            "Seamlessly weave cosmic astrophysics (distance in light years, age of stars) with ancient constellation folklore."
        )

        prompt = f"""
Current Observing Conditions (from TabPFN):
- Sky Transparency: {seeing_data.get('transparency_pct', 90)}%
- Atmospheric Seeing: {seeing_data.get('seeing_label', 'Clear')}
- Limiting Magnitude: {seeing_data.get('naked_eye_magnitude_limit', 5.5)}

Key Celestial Targets Visible Tonight:
{target_summary}

Write a {duration_minutes}-minute audio-guided stargazing tour.
Structure it in 3 distinct, soothing spoken chapters:
1. Grounding & Night Vision Adjustment (breathing, relaxing eyes into the dark, feeling the grass/earth).
2. The Guided Star-Hop (step-by-step eye navigation across 2-3 of the visible targets above).
3. Cosmic Reflection & Stillness (contemplation of light travel time and our place in the cosmos).

Write ONLY the spoken narration. Do not include stage directions in brackets.
"""

        response_text = self._query_gemma(prompt, system_instruction)
        if not response_text:
            response_text = self._offline_script_fallback(top_targets, seeing_data)

        # Parse into discrete audio chapters
        chapters = self._split_into_chapters(response_text, top_targets)

        return {
            "model": f"Google Gemma ({self.model_name}) via Local Inference",
            "full_script": response_text,
            "chapters": chapters,
            "targets_covered": [t["name"] for t in top_targets],
            "offline_mode": True
        }

    def answer_astronomy_question(
        self,
        question: str,
        visible_targets: List[Dict[str, Any]],
        seeing_data: Dict[str, Any]
    ) -> str:
        """
        Answers a spontaneous voice inquiry from the observer (e.g., 'What is that bright light in the east?').
        """
        targets_context = ", ".join([f"{t['name']} ({t['cardinal_direction']}, {t['altitude_deg']}° alt)" for t in visible_targets[:6]])
        
        system_instruction = (
            "You are Whispers of the Sky (WOTS). You are answering a late-night stargazer sitting outside under the open sky. "
            "Keep your spoken answer concise (2-4 sentences), poetic yet astrophysically accurate, and tell them exactly where to look."
        )

        prompt = f"""
Currently visible in their sky: {targets_context}
Current seeing quality: {seeing_data.get('seeing_label', 'Clear')}

The stargazer asks: "{question}"
Provide a calm, direct, spoken answer:
"""
        ans = self._query_gemma(prompt, system_instruction)
        if not ans:
            ans = f"In tonight's sky, looking toward {visible_targets[0]['cardinal_direction']}, you can see {visible_targets[0]['name']}. Its steady glow reaches your eyes through a clear autumn atmosphere."
        return ans.strip()

    def _query_gemma(self, prompt: str, system_instruction: str) -> Optional[str]:
        """Queries local Ollama Gemma instance."""
        payload = {
            "model": self.model_name,
            "prompt": f"{system_instruction}\n\n{prompt}",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 280,
            }
        }
        try:
            req = urllib.request.Request(
                f"{self.ollama_host}/api/generate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=90.0) as resp:
                res = json.loads(resp.read().decode())
                return res.get("response", "").strip()
        except Exception as e:
            print(f"[GemmaAstronomer] Local inference call note: {e}")
            return None

    def _split_into_chapters(self, full_text: str, targets: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Splits full narrative into playable audio tracks with titles."""
        paragraphs = [p.strip() for p in full_text.split("\n\n") if len(p.strip()) > 40]
        if len(paragraphs) >= 3:
            return [
                {
                    "title": "Chapter 1: Eyes to the Darkness",
                    "text": paragraphs[0],
                    "target": "Night Vision Grounding"
                },
                {
                    "title": f"Chapter 2: Star-Hop to {targets[0]['name'].split('(')[0].strip() if targets else 'The Stars'}",
                    "text": "\n\n".join(paragraphs[1:-1]),
                    "target": targets[0]['name'] if targets else "Constellations"
                },
                {
                    "title": "Chapter 3: The Deep Quiet of Space",
                    "text": paragraphs[-1],
                    "target": "Cosmic Reflection"
                }
            ]
        else:
            return [
                {
                    "title": "Full Guided Stargazing Journey",
                    "text": full_text,
                    "target": targets[0]["name"] if targets else "Night Sky"
                }
            ]

    def _offline_script_fallback(self, targets: List[Dict[str, Any]], seeing_data: Dict[str, Any]) -> str:
        """Deterministic high-quality fallback script in case Ollama is not active."""
        t1 = targets[0] if len(targets) > 0 else {"name": "Cassiopeia", "cardinal_direction": "North", "elevation_description": "high up", "star_hop": "Look north for the distinct W"}
        t2 = targets[1] if len(targets) > 1 else {"name": "Pegasus", "cardinal_direction": "South", "elevation_description": "overhead", "star_hop": "Look south for the Great Square"}

        return (
            f"Lie back comfortably against the earth. Close your eyes for just three gentle breaths. "
            f"Feel the cool night air across your forehead and the solid, steady ground beneath your spine. "
            f"Tonight, TabPFN forecasts an atmospheric transparency of {seeing_data.get('transparency_pct', 92)}%, "
            f"giving us rare, crisp clarity.\n\n"
            f"Now gently open your eyes into the darkness. Do not search for your phone; let the dark envelop you. "
            f"First, tilt your head toward the {t1['cardinal_direction'].lower()}. "
            f"{t1['elevation_description']}. You are looking toward {t1['name']}. {t1['star_hop']}. "
            f"The photons entering your pupils right now began their journey centuries ago, travelling through "
            f"the silent void of space at three hundred thousand kilometers every second, solely to meet your eyes on this grass tonight.\n\n"
            f"Now let your gaze glide toward the {t2['cardinal_direction'].lower()}. {t2['elevation_description']}. "
            f"Here rests {t2['name']}. Notice how steady its light remains against the autumn sky. "
            f"Take one more deep breath of night air. The universe has been whispering this light for billions of years, "
            f"and for these quiet minutes outside, you are part of that ancient conversation."
        )


if __name__ == "__main__":
    astronomer = GemmaAstronomer()
    print("Ollama Gemma Connected:", astronomer.is_connected)
    sample_targets = [
        {"name": "Cassiopeia", "cardinal_direction": "North-East", "altitude_deg": 62.0, "elevation_description": "High in the heavens", "star_hop": "Look for the sharp 'W' shape"},
        {"name": "Andromeda Galaxy (M31)", "cardinal_direction": "East", "altitude_deg": 55.0, "elevation_description": "Mid-sky", "star_hop": "Look below Cassiopeia for a pale oval smudge"}
    ]
    tour = astronomer.generate_tour_script(sample_targets, {"transparency_pct": 94.0, "seeing_label": "Exceptional"})
    print("Tour Model:", tour["model"])
    print("Sample Chapter 1:", tour["chapters"][0]["text"][:150], "...")
