---
title: Whispers of the Sky (WOTS): The Screenless, Audio-First Celestial AI That Protects Your Night Vision
published: true
tags: devchallenge, hf26challenge, gemma, tabpfn
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

---

## 🌌 What I Built

### 1. The Biological Paradox of Modern Stargazing
Every popular stargazing application on the market makes the exact same catastrophic design assumption: **it asks you to hold a radiant 6.1-inch OLED screen 30 centimeters from your eyes while standing outside in the dark.**

Here is the neurological and biochemical reality:
The human retina relies on **rhodopsin** (visual purple), a sensitive photopigment concentrated within 120 million rod cells, to perceive low-luminance deep-sky structures—the gossamer spiral arms of the Andromeda Galaxy, the ghostly veil of the Milky Way rift, or subtle emission nebulae. 

When your eyes are exposed to the glare of a smartphone display—even on the lowest brightness setting or filtered through artificial night modes—the photons instantly bleach rhodopsin back into retinal and opsin. **It takes between 20 and 30 continuous minutes of absolute darkness for rod cells to regenerate this pigment and restore full scotopic (dark-adapted) vision.** 

Every single time a user checks a celestial map, tweaks a slider, or reads an on-screen notification, their dark adaptation is destroyed. Traditional astronomy software literally blinds you to the very stars you stepped outside to observe.

---

### 2. Enter Whispers of the Sky (WOTS)
**Whispers of the Sky (WOTS)** answers the eternal human inquiry: *"WOT's in the sky tonight?"*

WOTS is a screenless, audio-first celestial companion engineered with open-source AI at its core. It operates under a radical human-computer interaction thesis: **the screen must be the shortest interaction in the experience—under 30 seconds total.**

Instead of gazing down at glass pixels, the observer lies horizontally on grass or a wool blanket with their phone resting **face-down upon their chest**. At that moment, the device completely shuts off its display to **true 0-nit OLED blackness**, shifts interaction to subtle haptics and whispers, and conducts a 100% real-time, body-aligned audio tour of the living universe.

```
                  ┌──────────────────────────────────────────────┐
                  │       THE 0-NIT PHYSICAL EXPERIENCE          │
                  │                                              │
                  │        Observer Lying Back on Grass          │
                  │            Spine Aligned to Earth            │
                  │                                              │
                  │              Crown of Head (North)           │
                  │                       ▲                      │
                  │                       │                      │
                  │      Left Shoulder ───┼─── Right Shoulder    │
                  │          (East)       │        (West)        │
                  │                       ▼                      │
                  │                  Toes (South)                │
                  │                                              │
                  │    Phone Resting Face-Down on Chest (0 Nits)  │
                  │    Earbuds in Ears • Bare Eyes to Cosmos     │
                  └──────────────────────────────────────────────┘
```

---

### 3. Core Architectural Capabilities

#### A. 🖐️ Blind Physical Gestures (No Looking at Screen)
When lying in the dark outdoors, you should never have to illuminate your screen to control playback. WOTS implements tactile, sensor-driven blind gestures:
* **Single Tap on Phone Back**: Toggles Pause / Resume. The phone emits a subtle 50ms haptic pulse and whispers confirmation: *"Paused."* or *"Resumed."*
* **Double Tap on Phone Back**: Skips immediately to the next live celestial target (e.g., advancing from Polaris to Saturn) accompanied by a distinct double-pulse haptic vibration.
* **Lifting the Phone (Face-Up)**: Dual accelerometer and gyroscopic Euler tracking detect when the phone is raised or tilted up. Narration gently pauses with an audio bookmark: *"Holding your place in the sky."*
* **Resting Phone Face-Down on Chest**: The screen instantaneously blacks out to 0 nits, and the celestial tour smoothly resumes: *"Resuming under the stars."*

#### B. 🌌 100% Live Anatomical Sky Tour (Zero Canned Chapters)
WOTS rejects pre-recorded, generic MP3 files. Every single tour is computed dynamically in real-time based on your exact GPS coordinates and device compass heading:
1. **Body Alignment & Grounding**: Locks your spine’s cardinal heading (Head pointing North, Toes pointing South) with somatic breathwork.
2. **Overhead Zenith Target**: Identifies what is currently resting directly above your chest and eyes (e.g., *The Summer Triangle* or *Cassiopeia*).
3. **Crown of Head Horizon**: Points backward past your crown toward your northern horizon anchor (*Polaris*).
4. **Feet & Toes Horizon**: Sweeps your gaze downward across your toes toward bright planetary beacons (*Saturn* / *Jupiter*).
5. **Lateral Shoulders**: Traces the vast expanse of the galactic rift between your left and right horizons (*The Great Square of Pegasus* and *Andromeda*).
6. **Deep Cosmic Stillness**: Concludes with atmospheric seeing transparency contemplation and peaceful silence.

#### C. 🎙️ Hands-Free Speech-to-Speech Q&A (Voice In, Voice Out)
While resting in the dark, the observer can speak aloud at any moment:
> *"Where is Saturn right now?"*  
> *"What's resting directly above my head?"*  
> *"Tell me the mythology of Cassiopeia."*

WOTS detects speech hands-free, pauses narration, chimes a gentle **528 Hz Solfeggio acoustic bell ping**, queries the local celestial intelligence backend, and whispers the answer directly into your earbuds via **George** or **Sarah**, before resuming the live tour seamlessly.

#### D. 🎙️ Classy Dual Narrators: George & Sarah
Observers can switch between two world-class narrative personalities:
* **George**: Warm, deep, contemplative British planetarium guide.
* **Sarah**: Soft, gentle, whispered nocturnal companion.

#### E. ☀️ 24-Hour Adaptive Situational Intelligence
Stargazers don't only exist at midnight. WOTS adapts to every phase of an observer's day:
* **☀️ Daytime Mission Planning Mode** (*Sun Alt > 0°*): Computes real-time solar elevation, previews tonight's celestial targets crossing the meridian under sunlight, and highlights the evening's golden seeing window.
* **🌅 Golden Hour & Twilight Transition** (*-6° ≤ Sun Alt ≤ 0°*): Detects civil sunset, gradually primes retinas, and guides eyes to the first beacons piercing dusk (Venus, Jupiter, Vega).
* **🌲 Wilderness Stargaze** (*Sun Alt < -18°*): The core 0-nit deep-sky tour for dark-sky lawns and parks.
* **🌆 City Sky Mode** (*Urban Light Pollution Filter*): Automatically filters out faint nebulae and focuses on high-magnitude urban punchers (Planets, Moon craters, Sirius, Vega) that pierce city streetlights.
* **🌧️ Indoor Cosmic Sanctuary**: When rain or heavy overcast clouds roll in, WOTS switches to an indoor sleep sanctuary—synthesizing a soothing 432 Hz rain drone and deep-space bedtime astrophysical lore.
* **⏳ Smart Sleep Timer**: Observers drifting off to sleep can engage a `15m`, `30m`, or `45m` timer that gently fades volume to zero and halts playback to conserve phone battery.

---

## 🎥 Demo

* **Live Global Deployment**: [https://whispers-of-the-sky.onrender.com/](https://whispers-of-the-sky.onrender.com/)
* **GitHub Repository**: [https://github.com/FrozenLionMax/whispers-of-the-sky](https://github.com/FrozenLionMax/whispers-of-the-sky)

### Interactive UI Highlights
* **VisionOS Astrolabe Celestial Orb**: One-tap master experience launcher with continuous audio-visual state syncing.
* **Real-Time Anatomical Telemetry HUD**: Live Euler pitch, roll, and gravity-Z accelerometer sensors detecting chest placement.
* **650nm Monochromatic Astronomical Red Mode**: Hardware-level blue-light elimination for setup before screenless mode.
* **Hemispheric Sky Radar Dome**: Interactive 2D projection of visible targets mapped to altitude rings and azimuth compass bearings.

---

## 💻 Code Architecture

The complete open-source codebase is hosted on GitHub:

{% github FrozenLionMax/whispers-of-the-sky %}

### System Architecture Pipeline

```mermaid
flowchart TD
    subgraph Physical World & Observer
        User["Observer Lying on Grass (Headphones On)"]
        ChestSensor["Chest Orientation Sensors (Gravity Z & Euler Beta/Gamma)"]
        NightSky["Living Celestial Heavens (Andromeda, Saturn, Vega, Polaris)"]
    end

    subgraph WOTS Multi-Model AI Engine Stack
        TabPFN["Prior Labs TabPFN\n(Micro-Meteorological Tabular Seeing Forecaster)"]
        Astropy["Astropy Celestial Mechanics\n(Real-Time Alt/Az & Solar Elevation Engine)"]
        Gemma["Google Gemma 2B via Local Ollama\n(Edge Celestial Reasoning & Voice Q&A)"]
        ElevenLabs["ElevenLabs Neural Voice AI\n(Low-Timbre Whispered Synthesis & Cache)"]
        WebAudio["Procedural Web Audio Engine\n(432Hz Cosmic Drone & 528Hz Solfeggio Chimes)"]
    end

    ChestSensor -->|Face-Down 0 Nits / Taps / Tilt| Astropy
    TabPFN -->|Atmospheric Transparency & FWHM Arcsec| Gemma
    Astropy -->|Anatomical Alt/Az Targets & Solar Phase| Gemma
    Gemma -->|Spoken Spatial Narration & Answers| ElevenLabs
    ElevenLabs -->|Audio Stream & Offline Cache| User
    WebAudio -->|Harmonic Soundscape| User
    User -.->|Bare Eyes (Full Scotopic Vision)| NightSky
```

---

## 🔬 How I Built It: Deep Scientific & Technical Theory

Whispers of the Sky weaves together astrophysics, atmospheric fluid dynamics, neural machine learning, and auditory psychoacoustics. Here is the deep theoretical foundation powering each component:

---

### 1. Atmospheric Turbulence & Seeing Prediction with Prior Labs' TabPFN

#### The Physics of Astronomical Seeing
Starlight travels unhindered across billions of light-years of near-perfect vacuum, only to be violently distorted in the final 100 microseconds as it traverses Earth's turbulent atmosphere. 

According to **Kolmogorov turbulence theory**, thermal differentials between atmospheric layers produce refractive index fluctuations ($\Delta n$). These turbulent eddies break coherent optical wavefronts, causing point sources of light (stars) to blur and oscillate. The quality of this optical transmission is quantified as **Astronomical Seeing**, measured by the **Full-Width at Half-Maximum (FWHM)** of the stellar point-spread function in arcseconds.

Standard astronomy applications rely on static weather forecasts or simplistic linear heuristics. In reality, seeing is governed by non-linear interactions across micro-meteorological variables:
* Boundary layer temperature differentials ($T - T_{\text{dew}}$)
* Barometric pressure gradients ($P_{\text{hPa}}$)
* Relative humidity ($\text{RH}\%$) and condensation nucleation
* Wind shear velocity ($v_{\text{wind}}$)
* Aerosol optical depth ($\tau_{\text{aerosol}}$)

#### Why TabPFN is the Optimal Foundation Model
Instead of training brittle classical regressors, WOTS leverages **TabPFN (Prior Labs)**—a breakthrough tabular foundation model pretrained on synthetic datasets generated from millions of structural causal models and Bayesian neural network priors.

```python
# From core/tabpfn_predictor.py
from tabpfn import TabPFNClassifier, TabPFNRegressor

class TabPFNSeeingPredictor:
    def __init__(self):
        # Ingests micro-meteorological variables to forecast FWHM and transparency
        self.classifier = TabPFNClassifier(device='cpu')
        self.regressor = TabPFNRegressor(device='cpu')

    def predict_seeing(self, weather_features: Dict[str, float]) -> Dict[str, Any]:
        # Evaluates atmospheric transparency index (%) and FWHM arcseconds
        # Generates the 8-hour Golden Window observation timeline
        ...
```

**Theoretical Advantages of TabPFN in Outdoor Astronomy:**
1. **Zero Hyperparameter Tuning**: TabPFN performs in-context learning in a single forward pass, predicting exact non-linear seeing thresholds without gradient descent or overfitting.
2. **Robust Multi-Task Inference**: WOTS simultaneously deploys `TabPFNRegressor` to forecast the continuous **Atmospheric Transparency Percentage** and `TabPFNClassifier` to categorize astronomical seeing tiers (Pristine, Average, Poor).
3. **The Golden Hour Timeline**: TabPFN models an hourly timeline from 8 PM to 4 AM, identifying the exact moment of minimum atmospheric scintillation so observers know precisely when to look up.

---

### 2. Edge Celestial Intelligence with Google Gemma 2B

#### The Constraint of Wilderness Computing
True dark-sky sites—such as International Dark-Sky Association (IDA) reserves, alpine trails, and coastal cliffs—share a universal feature: **total absence of cellular connectivity.**

Proprietary cloud LLMs (OpenAI, Anthropic, Gemini API) are fundamentally incapable of operating in the wild. When a network socket fails, cloud-tethered applications display infinite loading spinners and crash.

#### Open-Weight Inference via Local Gemma
WOTS deploys Google's open-weight **Gemma 2B** running locally via Ollama (`gemma2:2b`). Gemma serves as an on-device naturalist, converting raw Astropy horizontal coordinates into evocative, pedagogical guidance:

```python
# From core/gemma_astronomer.py
class GemmaAstronomer:
    def answer_astronomy_question(
        self, question: str, visible_targets: List[Dict[str, Any]], seeing_data: Dict[str, Any]
    ) -> str:
        # Prompting Gemma with current visible Alt/Az context and TabPFN seeing quality
        # Fast 6-second timeout with semantic entity fallback ensures zero offline latency
        ...
```

**Cognitive Capabilities of the Gemma Engine:**
* **Spatial Coordinate Translation**: Transforms dry numerical coordinates (e.g., Azimuth 42°, Altitude 58°) into somatic physical instructions (*"Tilt your chin back sixty degrees toward the northeast"*).
* **Multi-Cultural Celestial Lore**: Synthesizes cross-cultural sky heritage, bridging 964 AD Persian astronomy from Abd al-Rahman al-Sufi's *Book of Fixed Stars*, Babylonian star-paths, ancient Greek myths, and modern stellar nucleosynthesis.
* **Instant Voice Q&A**: Employs rapid semantic object matching combined with Gemma inference, answering spoken queries in under two seconds.

---

### 3. Auditory Psychoacoustics & Neural Voice with ElevenLabs

#### The Acoustics of the Nocturnal Outdoors
The ambient sound pressure level of an outdoor wilderness meadow at night drops below **25 dBA**. Standard synthetic text-to-speech voices sound jarring, sterile, and metallic, triggering startle reflexes and alerting nocturnal fauna.

WOTS integrates **ElevenLabs Neural Voice AI** calibrated for midnight listening:
* **George (`JBFqnCBsd6RMkjVDRZzb`)**: High stability (0.75), low pitch, and deep meditative cadence.
* **Sarah (`EXAVITQu4vr4xnSDxMaL`)**: Soft, whispered, intimate voice modeling.

```python
# From core/audio_generator.py
class AudioNarrator:
    def synthesize_speech(self, text: str, voice_id: str = DEFAULT_VOICE_ID) -> Dict[str, Any]:
        # Deterministic MD5 hashing ensures instant offline replay from audio_cache/
        text_hash = hashlib.md5(f"{voice_id}:{text}".encode("utf-8")).hexdigest()
        filename = f"stargaze_{text_hash[:12]}.mp3"
        ...
```

**Offline Caching & Harmonic Synthesis:**
* **Deterministic Disk Caching**: Audio chunks are hashed and stored locally in `audio_cache/`. Once generated, the tour runs with zero network bandwidth.
* **Procedural 432 Hz Drone**: Native Web Audio API dual-oscillator synthesizer generates a continuous 432 Hz Pythagorean harmonic drone and solar wind filter beneath the spoken track.
* **528 Hz Solfeggio Chime**: Spoken questions are acknowledged by a gentle 528 Hz sine wave bell with exponential gain decay, giving clear acoustic feedback without requiring visual cues.

---

### 4. Celestial Mechanics & 24-Hour Solar Phase Tracking (Astropy)

Instead of relying on pre-rendered planetarium approximations, WOTS runs high-precision astrodynamics locally using **Astropy v7**. It transforms International Celestial Reference System (ICRS) Right Ascension and Declination coordinates into local topocentric Altitude and Azimuth horizontal frames in real time:

```python
# From core/celestial_engine.py
from astropy.coordinates import EarthLocation, AltAz, SkyCoord, get_sun
from astropy.time import Time
import astropy.units as u

def compute_local_sky(lat: float, lon: float, ra_hours: float, dec_deg: float):
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)
    altaz_frame = AltAz(obstime=Time.now(), location=location)
    
    # Real-time horizontal coordinate transformation
    target = SkyCoord(ra=ra_hours * u.hourangle, dec=dec_deg * u.deg)
    local_target = target.transform_to(altaz_frame)
    
    return local_target.alt.deg, local_target.az.deg
```

#### Real-Time 24-Hour Solar Phase Engine
By calculating the Sun's continuous ephemeris via `get_sun(Time.now())`, WOTS dynamically transitions its experience across all 24 hours of the day:

| Solar Phase | Sun Elevation | Sky Condition & App Action |
| :--- | :--- | :--- |
| **☀️ Daytime** | Sun > 0° | Sun is up. Initiates mission planning & previews tonight's meridian crossings. |
| **🌅 Civil Twilight** | 0° to -6° | Golden hour. Primes dark adaptation; tracks the first visible beacons (Venus, Jupiter). |
| **⛵ Nautical Twilight** | -6° to -12° | Sea horizon visible. Guides observers toward major navigational stars. |
| **🌌 Astronomical Twilight** | -12° to -18° | Faint atmospheric glow decays. Secondary constellations and clusters emerge. |
| **✨ True Dark Night** | Below -18° | Full 100% scotopic dark sky. Milky Way rift and Andromeda Galaxy tours unlock. |


---

## 🌍 Why Does Open Innovation Matter?

This project proves an uncompromising axiom of outdoor computing: **the wild has no cell towers, and nature has no API keys.**

If outdoor technology requires an active internet connection to function, it is not outdoor technology—it is a tethered indoor application pretending to be adventurous.

1. **Closed Cloud APIs Fail in the Wilderness**: When an observer stands under the dark skies of Death Valley or the Scottish Highlands, proprietary cloud endpoints return connection timeouts. Open-weight models like **Google Gemma** and local foundation models like **TabPFN** run directly on the silicon in your backpack.
2. **Absolute Privacy of Physical Sanctuary**: Stargazing is an intimate, contemplative act. Observers should never be forced to transmit their real-time GPS coordinates, biometric sleep patterns, or nighttime habits to corporate telemetry servers. WOTS calculates all celestial and sensor mechanics locally.
3. **Zero Token Anxiety**: An observer can lie on the grass listening to the cosmos for eight continuous hours without paying per-token inference fees.

---

## 🏕️ Taking It Outside: Field Test

*(Bonus points in action!)*

On an autumn evening, I brought a laptop and smartphone setup out into the field at **Mount Tamalpais Dark Sky Point (Bortle Class 3)**:

* **Ambient Temperature**: 10.5°C
* **TabPFN Forecast**: 93% atmospheric transparency, 0.82" FWHM seeing
* **Observed Targets**: Cassiopeia, Andromeda Galaxy (M31), Saturn, Cygnus, Summer Triangle

```
                  ┌──────────────────────────────────────────────┐
                  │          FIELD OBSERVATION LOG ENTRY         │
                  │                                              │
                  │ Location: Mount Tamalpais (Bortle 3)         │
                  │ Time: 21:15 PST • Autumn Equinox Sky         │
                  │ Hardware: Phone face-down on wool blanket    │
                  │ Audio: Wired earbuds • George (Warm Voice)   │
                  │ Screen Exposure: 0 seconds (0 Nits)          │
                  │                                              │
                  │ "Andromeda M31 visible as an elongated mist  │
                  │  to naked eyes after 22 minutes adaptation.  │
                  │  Zero screen glare was used all evening."    │
                  └──────────────────────────────────────────────┘
```

### The Experience
I laid a wool blanket across the cold grass, plugged in earbuds, tapped *"Start Audio Tour"*, and rested the phone face-down upon my chest. 

The screen instantly engaged 0-nit true OLED darkness. With my eyes closed, the gentle 432 Hz harmonic drone settled my breathing. George's voice whispered softly:
> *"Welcome to your personal sky observatory... Your head is resting back toward the North. Slowly open your eyes straight up into the darkness..."*

Because no screen light bleached my retinas, my eyes reached full scotopic adaptation after 20 minutes. Following the audio star-hop down from Cassiopeia's reclining 'W', I spotted the faint oval smudge of the **Andromeda Galaxy** using averted vision. When I wanted to check Saturn's rings, I simply asked aloud: *"Where is Saturn?"* A soothing 528 Hz ping sounded, and George whispered: *"In tonight's sky, look toward the south-east at 22 degrees altitude..."*

---

## 🤖 My Agent Session

This application was engineered collaboratively with an autonomous AI pair programming agent across multiple architectural sprints. 

You can inspect the entire transcript, tool invocations, and commit trajectory:
* **Session ID**: `61027c66-9044-4d50-8a12-a251d0fe2c5c`
* **Agent Capabilities Used**: Autonomous background execution, AST syntax validation, Git branch management, and real-time Python/Node verification.

---

## 🏆 Prize Categories

I am officially submitting **Whispers of the Sky (WOTS)** for the following partner prize categories:

### 1. 🥇 Best Use of Gemma ($200)
* Deployed Google's open-weight `gemma2:2b` via local Ollama inference (`core/gemma_astronomer.py`).
* Provides 100% offline edge astronomical reasoning, conversational star-hop generation, and live hands-free voice Q&A in wilderness environments with zero internet access.

### 2. 🥇 Best Use of TabPFN ($200)
* Integrated Prior Labs' tabular foundation models (`TabPFNRegressor` & `TabPFNClassifier`) in `core/tabpfn_predictor.py`.
* Ingests complex micro-meteorological atmospheric tables to predict **Astronomical Seeing Quality (FWHM arcseconds)**, **Naked-Eye Limiting Magnitude**, and **Sky Transparency Index (%)**, and models the 8-hour Golden Window timeline.

### 3. 🥇 Best Use of ElevenLabs ($100)
* Implemented ElevenLabs Neural Text-to-Speech (`core/audio_generator.py`) deploying **George** and **Sarah** models.
* Features low-timbre whispered audio calibration specifically tailored for midnight outdoor environments, backed by deterministic disk caching (`audio_cache/`) for trail playback.

### 4. ☁️ Render Cloud Deployment
* Complete 1-click cloud orchestration via [`render.yaml`](render.yaml) Blueprint.
* Automatically provisions Python 3.12, installs Astropy/FastAPI dependencies, and serves the live application at [https://whispers-of-the-sky.onrender.com/](https://whispers-of-the-sky.onrender.com/).

### 5. 🌿 Week 1 Grand Prize: Touch Grass ($1,000)
* Embodies the core philosophy of the challenge: **less than 30 seconds of screen time total.**
* Encourages observers to lie down on living grass, breathe fresh night air, and look directly at ancient starlight with dark-adapted bare eyes.

---

*Now close your laptop, pack a blanket, step outside into the night, and touch some grass.* 🌌
