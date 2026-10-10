"""
Whispers of the Sky (WOTS) - Launcher Script
Runs the FastAPI server with local Ollama Gemma, TabPFN, and ElevenLabs support.
"""

import sys
import os
import uvicorn

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    print("=" * 68)
    print("  * WHISPERS OF THE SKY (WOTS) *")
    print("  WOT's in the sky tonight? - Screenless Audio Celestial Guide")
    print("  Protect Night Vision - 100% Offline Capable")
    print("=" * 68)
    print("\n[+] Initializing local astronomical engines...")
    print("    - TabPFN: Prior Labs Tabular Foundation Model (Seeing Forecaster)")
    print("    - Gemma: Google Gemma 2B (Local Offline Celestial Narrator)")
    print("    - Astropy: Real-time Altitude/Azimuth Horizontal Coordinate Engine")
    print("    - ElevenLabs: Deep Whispered Audio Narration\n")
    print("[*] Starting Web Server on http://127.0.0.1:8000")
    print("[*] Open http://127.0.0.1:8000 in your browser, lie back on the grass,")
    print("    put in your headphones, and tap 'Eyes to Sky'.\n")

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
