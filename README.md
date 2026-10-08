# 🌌 Whispers of the Sky (WOTS)

> **WOT's in the sky tonight?**  
> *The screenless, audio-first celestial guide that protects your night vision.*

[![Model](https://img.shields.io/badge/LLM-Google%20Gemma%202B-4285F4.svg)](https://ai.google.dev/gemma)
[![Tabular AI](https://img.shields.io/badge/Forecasting-Prior%20Labs%20TabPFN-00C49F.svg)](https://docs.priorlabs.ai/)
[![Voice](https://img.shields.io/badge/Voice-ElevenLabs-black.svg)](https://elevenlabs.io/)
[![Astronomy](https://img.shields.io/badge/Astro-Astropy%20v7-E05A47.svg)](https://www.astropy.org/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## 🍃 Why WOTS? The Philosophy

Every traditional stargazing app asks you to hold a bright 6-inch glowing rectangle in front of your face while standing outside in the dark.

**The Biological Flaw:** The human eye relies on rhodopsin (a photopigment in rod cells) to perceive faint nebulae, stellar nurseries, and distant galaxies. A single second of exposure to smartphone screen glare bleaches rhodopsin and destroys dark adaptation for **20 to 30 minutes**.

**Whispers of the Sky (WOTS)** takes a completely different approach:

1. **Screen Time Under 30 Seconds**: Pick your session and immediately tap **"Eyes to Sky"**.
2. **True OLED Blanket Mode**: The screen turns pitch black (0-nit black). Put your phone in your pocket or face down on the grass.
3. **Immersive Audio Star-Hopping**: A calm, whispered voice guides your bare eyes across the constellations using physical, tactile landmarks (*"Tilt your chin up forty degrees... Two fist-widths to your left... Feel the cool night air"*).
4. **100% Offline in the Wilderness**: National parks, dark-sky reserves, and mountain trails often have zero cell signal. WOTS runs local open-weight AI directly on your device.

---

## 🏗️ Architecture

```mermaid
flowchart TD
    subgraph Physical World
        Observer["Observer with Headphones (Screen Off)"]
        NightSky["Night Sky (Cassiopeia, Andromeda M31, Saturn, Jupiter)"]
    end

    subgraph WOTS Engine Stack
        TabPFN["Prior Labs TabPFN\n(Tabular Seeing & Transparency Forecaster)"]
        Astropy["Astropy Engine\n(Real-time Alt/Az Horizontal Coordinates)"]
        Gemma["Google Gemma 2B\n(Local Offline Astronomer via Ollama)"]
        Voice["ElevenLabs & Web Audio\n(Whispered Night Narration & Disk Cache)"]
    end

    TabPFN -->|Atmospheric Seeing & Transparency| Gemma
    Astropy -->|Naked-Eye Horizon Targets| Gemma
    Gemma -->|Spoken Guidance Narrative| Voice
    Voice -->|Audio Stream| Observer
    Observer -.->|Bare Eyes (Full Night Vision)| NightSky
```

---

## 🛠️ The Technology Stack

- **Google Gemma 2B**: Local open-weight language model running via Ollama. Composes poetic, scientifically accurate star-hopping audio scripts and answers live voice questions completely offline.
- **Prior Labs TabPFN**: Tabular foundation model forecasting atmospheric seeing (FWHM arcseconds), sky transparency (%), and the golden observation window from meteorological sensor data.
- **ElevenLabs**: High-fidelity, low-timbre whispered audio narration calibrated for dark outdoor listening, backed by deterministic disk caching.
- **Astropy**: Computes exact horizontal coordinates (Altitude/Azimuth) and naked-eye visibility thresholds.
- **FastAPI + OLED UI**: Monochromatic 650nm Red Mode & "Blank Blanket Mode" that eliminates blue light emission.

---

## 🚀 Quickstart Guide

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/FrozenLionMax/whispers-of-the-sky.git
cd whispers-of-the-sky
pip install -r requirements.txt
```

### 2. Run Local Gemma (100% Offline)
Make sure [Ollama](https://ollama.ai) is installed, then pull the lightweight Gemma 2B model:
```bash
ollama pull gemma2:2b
```

### 3. Launch WOTS
```bash
python run.py
```
Open **`http://localhost:8000`** in your browser.

*(Optional)* Set your ElevenLabs API key for studio-grade narration (a native browser Web Audio synthesizer is enabled automatically if no key is present):
```bash
export ELEVENLABS_API_KEY="your-key-here"
```

---

## 🌙 How to Use in the Field

1. **Step Outside**: Take your blanket or chair outside to your backyard, a local park, or a mountain trail.
2. **Check Seeing**: Review the **TabPFN Seeing Forecast** to confirm atmospheric transparency and the best observation window.
3. **Launch the Tour**: Tap **"Start Screenless Tour"**.
4. **Blank the Screen**: Tap **"Eyes to Sky"**. The display turns pitch black. Put your phone in your pocket or face down on the grass.
5. **Listen & Look Up**: Let WOTS whisper star-hopping paths directly into your headphones. Tap anywhere on the dark screen to pause or resume.

---

## 🗺️ What's Next for WOTS?

- [ ] **Smart Telescope & Binocular Sync**: Auto-syncing audio narration with manual telescope azimuth mounts.
- [ ] **Binaural Spatial Orientation**: Spatial 3D directional audio clues that pan into your left/right ear as you turn your head toward targets.
- [ ] **Community Dark-Sky Logbook**: Decentralized, local-first logging of Bortle ratings and seeing conditions.

---

## 📄 License

MIT License. Built for open science, astronomy lovers, and night sky observers.
