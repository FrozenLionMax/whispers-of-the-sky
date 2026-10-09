"""
Whispers of the Sky (WOTS) - Live Meteorological Telemetry Integration.
Fetches real-time atmospheric conditions (Open-Meteo API, zero-key, high precision)
and pipes them directly into Prior Labs' TabPFN tabular foundation model.
"""

import urllib.request
import json
from typing import Dict, Any, Optional

def fetch_live_weather_telemetry(lat: float, lon: float) -> Optional[Dict[str, float]]:
    """
    Pulls live atmospheric metrics for exact coordinates from Open-Meteo's hourly API.
    Returns parameters formatted for TabPFN seeing prediction.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current="
        f"temperature_2m,relative_humidity_2m,dew_point_2m,cloud_cover,surface_pressure,wind_speed_10m"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WhispersOfTheSky/1.0"})
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            data = json.loads(resp.read().decode())
            current = data.get("current", {})
            
            temp = float(current.get("temperature_2m", 12.0))
            dew = float(current.get("dew_point_2m", 6.0))
            dew_diff = max(0.5, temp - dew)
            
            return {
                "cloud_cover_pct": float(current.get("cloud_cover", 10.0)),
                "humidity_pct": float(current.get("relative_humidity_2m", 50.0)),
                "temp_c": temp,
                "dew_point_diff": round(dew_diff, 1),
                "wind_speed_kmh": float(current.get("wind_speed_10m", 8.0)),
                "pressure_hpa": float(current.get("surface_pressure", 1015.0)),
                "aerosol_index": 0.04
            }
    except Exception as e:
        print(f"[Telemetry] Warning fetching live weather: {e}")
        return None
