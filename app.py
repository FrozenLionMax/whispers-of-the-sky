"""
Whispers of the Sky (WOTS) - FastAPI Backend Application.
The Screenless, Audio-First Celestial Companion That Protects Your Night Vision.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json
import os
from pathlib import Path

from core.tabpfn_predictor import TabPFNSeeingPredictor
from core.celestial_engine import CelestialEngine
from core.gemma_astronomer import GemmaAstronomer
from core.audio_generator import AudioNarrator, AUDIO_CACHE_DIR
from core.telemetry import fetch_live_weather_telemetry

# Initialize FastAPI
app = FastAPI(
    title="Whispers of the Sky (WOTS)",
    description="Screenless, Audio-First Celestial Companion Powered by TabPFN, Gemma, and ElevenLabs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
tabpfn_predictor = TabPFNSeeingPredictor()
gemma_astronomer = GemmaAstronomer()
audio_narrator = AudioNarrator()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
FIELD_LOGS_FILE = BASE_DIR / "field_logs.json"

STATIC_DIR.mkdir(exist_ok=True, parents=True)
if not FIELD_LOGS_FILE.exists():
    with open(FIELD_LOGS_FILE, "w") as f:
        json.dump([
            {
                "id": "log_demo_01",
                "timestamp": "2026-10-08T22:30:00Z",
                "location": "Mount Tamalpais Dark Sky Point (Lat: 37.92, Lon: -122.59)",
                "bortle_scale": 3,
                "seeing": "Pristine / Exceptional (FWHM 0.8\")",
                "targets_observed": ["Cassiopeia", "Andromeda Galaxy (M31)", "Saturn"],
                "notes": "100% offline session on grass. Laid on wool blanket with phone face down. Andromeda galaxy was clearly visible as an elongated smudge to the naked eye. Used zero screen light for 45 minutes."
            }
        ], f, indent=2)


# Pydantic Request Models
class SeeingRequest(BaseModel):
    cloud_cover_pct: float = Field(default=8.0, ge=0.0, le=100.0)
    humidity_pct: float = Field(default=40.0, ge=0.0, le=100.0)
    temp_c: float = Field(default=12.0)
    dew_point_diff: float = Field(default=7.0)
    wind_speed_kmh: float = Field(default=7.0, ge=0.0)
    pressure_hpa: float = Field(default=1018.0)
    aerosol_index: float = Field(default=0.04)

class SkyRequest(BaseModel):
    latitude: float = Field(default=37.7749)
    longitude: float = Field(default=-122.4194)
    elevation_m: float = Field(default=50.0)

class TourRequest(BaseModel):
    latitude: float = Field(default=37.7749)
    longitude: float = Field(default=-122.4194)
    duration_minutes: int = Field(default=10, ge=3, le=30)
    conditions: Optional[SeeingRequest] = None

class AskQuestionRequest(BaseModel):
    question: str
    latitude: float = Field(default=37.7749)
    longitude: float = Field(default=-122.4194)

class SynthesizeRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None

class BodyAlignedSkyRequest(BaseModel):
    latitude: float = Field(default=37.7749)
    longitude: float = Field(default=-122.4194)
    head_heading_deg: float = Field(default=0.0)
    voice: Optional[str] = "male"

class FieldLogEntry(BaseModel):
    location: str
    bortle_scale: int
    targets: List[str]
    notes: str


@app.get("/api/status")
async def get_system_status():
    """Returns engine connectivity, model versions, and offline readiness."""
    return {
        "status": "online",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tabpfn": {
            "ready": True,
            "engine": "Prior Labs TabPFN Foundation Model",
            "offline_capable": True
        },
        "gemma": {
            "ready": gemma_astronomer.is_connected,
            "model": gemma_astronomer.model_name,
            "ollama_host": gemma_astronomer.ollama_host,
            "offline_capable": True
        },
        "elevenlabs": {
            "ready": audio_narrator.client is not None,
            "cached_audio_count": len(list(AUDIO_CACHE_DIR.glob("*.mp3"))),
            "fallback": "Browser Web Audio API (zero credentials needed)"
        }
    }


@app.post("/api/seeing-forecast")
async def forecast_seeing(req: SeeingRequest):
    """Predicts atmospheric seeing and transparency using TabPFN."""
    conditions = req.model_dump()
    prediction = tabpfn_predictor.predict_seeing(conditions)
    timeline = tabpfn_predictor.forecast_nightly_timeline(conditions)
    return {
        "prediction": prediction,
        "hourly_timeline": timeline
    }


@app.post("/api/live-telemetry")
async def live_telemetry(req: SkyRequest):
    """Pulls live atmospheric weather telemetry for observer coords and predicts with TabPFN."""
    telemetry = fetch_live_weather_telemetry(req.latitude, req.longitude)
    if not telemetry:
        telemetry = {
            "cloud_cover_pct": 12.0,
            "humidity_pct": 52.0,
            "temp_c": 14.0,
            "dew_point_diff": 5.5,
            "wind_speed_kmh": 8.0,
            "pressure_hpa": 1016.0,
            "aerosol_index": 0.04
        }
    prediction = tabpfn_predictor.predict_seeing(telemetry)
    timeline = tabpfn_predictor.forecast_nightly_timeline(telemetry)
    return {
        "telemetry": telemetry,
        "prediction": prediction,
        "hourly_timeline": timeline
    }


@app.post("/api/visible-sky")
async def get_visible_sky(req: SkyRequest):
    """Computes real-time horizontal coordinates for autumn celestial landmarks."""
    engine = CelestialEngine(lat=req.latitude, lon=req.longitude, elevation_m=req.elevation_m)
    visible_targets = engine.compute_visible_sky()
    return {
        "observer": {"lat": req.latitude, "lon": req.longitude},
        "total_visible": len(visible_targets),
        "targets": visible_targets
    }


@app.post("/api/generate-tour")
async def generate_tour(req: TourRequest):
    """Generates an audio-guided, screenless stargazing tour via Gemma & TabPFN."""
    engine = CelestialEngine(lat=req.latitude, lon=req.longitude)
    visible_targets = engine.compute_visible_sky()

    cond = req.conditions.model_dump() if req.conditions else {
        "cloud_cover_pct": 5.0,
        "humidity_pct": 38.0,
        "temp_c": 11.0,
        "dew_point_diff": 7.5,
        "wind_speed_kmh": 6.0,
        "pressure_hpa": 1019.0,
        "aerosol_index": 0.03
    }
    seeing_data = tabpfn_predictor.predict_seeing(cond)

    tour_script = gemma_astronomer.generate_tour_script(
        visible_targets=visible_targets,
        seeing_data=seeing_data,
        duration_minutes=req.duration_minutes
    )

    # Pre-synthesize chapters if ElevenLabs is active
    for ch in tour_script["chapters"]:
        synth_res = audio_narrator.synthesize_speech(ch["text"])
        ch["audio_url"] = synth_res.get("audio_url")
        ch["audio_provider"] = synth_res.get("provider")

    return {
        "tour": tour_script,
        "seeing": seeing_data,
        "primary_targets": visible_targets[:4]
    }


@app.post("/api/body-aligned-sky")
async def body_aligned_sky_endpoint(req: BodyAlignedSkyRequest):
    """Computes real-time sky targets mapped to observer's anatomy (Head, Feet, Shoulders, Zenith)."""
    engine = CelestialEngine(lat=req.latitude, lon=req.longitude)
    tour = engine.compute_body_aligned_tour(head_heading_deg=req.head_heading_deg)
    return tour


@app.post("/api/synthesize-audio")
async def synthesize_speech_endpoint(req: SynthesizeRequest):
    """Synthesizes text into speech or delegates to browser speech API."""
    res = audio_narrator.synthesize_speech(req.text, voice_id=req.voice_id or "JBFqnCBsd6RMkjVDRZzb")
    return res


@app.post("/api/ask-astronomer")
async def ask_astronomer_endpoint(req: AskQuestionRequest):
    """Provides a quick 2-sentence conversational astronomy answer for voice interaction."""
    engine = CelestialEngine(lat=req.latitude, lon=req.longitude)
    visible_targets = engine.compute_visible_sky()
    seeing_data = tabpfn_predictor.predict_seeing({"cloud_cover_pct": 10.0, "humidity_pct": 45.0})

    answer = gemma_astronomer.answer_astronomy_question(
        question=req.question,
        visible_targets=visible_targets,
        seeing_data=seeing_data
    )

    # Synthesize answer audio
    audio_res = audio_narrator.synthesize_speech(answer)

    return {
        "question": req.question,
        "answer": answer,
        "audio_url": audio_res.get("audio_url"),
        "audio_provider": audio_res.get("provider")
    }


@app.get("/api/field-logs")
async def get_field_logs():
    """Returns past outdoor field test sessions."""
    if FIELD_LOGS_FILE.exists():
        with open(FIELD_LOGS_FILE, "r") as f:
            return json.load(f)
    return []


@app.post("/api/log-field-test")
async def save_field_log(entry: FieldLogEntry):
    """Logs an outdoor stargazing session to disk."""
    logs = []
    if FIELD_LOGS_FILE.exists():
        with open(FIELD_LOGS_FILE, "r") as f:
            try:
                logs = json.load(f)
            except Exception:
                logs = []

    new_log = {
        "id": f"log_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": entry.location,
        "bortle_scale": entry.bortle_scale,
        "targets_observed": entry.targets,
        "notes": entry.notes
    }
    logs.insert(0, new_log)

    with open(FIELD_LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    return {"success": True, "log": new_log}


@app.get("/audio/{filename}")
async def serve_cached_audio(filename: str):
    """Serves synthesized MP3 audio tracks."""
    path = AUDIO_CACHE_DIR / filename
    if path.exists():
        return FileResponse(path, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio track not found")


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serves the main single-page application."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h1>Whispers of the Sky (WOTS) is starting up...</h1>")


# Mount static assets
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
