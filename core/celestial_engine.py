"""
Celestial Mechanics Engine for Whispers of the Sky (WOTS).
Calculates real-time horizontal coordinates (Altitude/Azimuth), visibility,
and naked-eye star-hopping routes using Astropy and astronomical catalog data.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import math

try:
    from astropy.time import Time
    from astropy.coordinates import EarthLocation, AltAz, SkyCoord
    import astropy.units as u
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False


# Catalog of major October / Autumn sky targets for naked-eye stargazing
CELESTIAL_TARGETS = [
    {
        "id": "cassiopeia",
        "name": "Cassiopeia (The Celestial Queen)",
        "type": "constellation",
        "ra_hours": 1.0,
        "dec_deg": 60.0,
        "magnitude": 2.2,
        "significance": "Distinctive 'W' shape in the northern sky, pointer to the Andromeda Galaxy and North Star.",
        "star_hop": "Look north, about two-thirds up from horizon. Spot the five bright stars forming a reclining 'W'."
    },
    {
        "id": "andromeda_galaxy",
        "name": "Andromeda Galaxy (M31)",
        "type": "deep_sky",
        "ra_hours": 0.71,
        "dec_deg": 41.27,
        "magnitude": 3.44,
        "significance": "Farthest object visible to the naked human eye at 2.5 million light-years away.",
        "star_hop": "From the point of Cassiopeia's 'W', follow the arrow down toward the Great Square of Pegasus. Look for an elongated misty smudge."
    },
    {
        "id": "pegasus",
        "name": "The Great Square of Pegasus",
        "type": "asterism",
        "ra_hours": 23.0,
        "dec_deg": 20.0,
        "magnitude": 2.5,
        "significance": "Dominates the southern autumn sky; ancient marker of clear autumn air.",
        "star_hop": "Face south. Look almost overhead for four bright stars forming an enormous baseball diamond in the darkness."
    },
    {
        "id": "summer_triangle",
        "name": "The Summer Triangle (Deneb, Vega, Altair)",
        "type": "asterism",
        "ra_hours": 20.0,
        "dec_deg": 35.0,
        "magnitude": 0.03,
        "significance": "Three brilliant first-magnitude stars crossing the western sky, framing the Milky Way rift.",
        "star_hop": "Turn west. Look for the piercing sapphire spark of Vega, accompanied by Deneb and Altair."
    },
    {
        "id": "saturn",
        "name": "Saturn (The Ringed Giant)",
        "type": "planet",
        "ra_hours": 23.2,
        "dec_deg": -7.5,
        "magnitude": 0.6,
        "significance": "A steady, golden ember shining unblinking in the constellation Aquarius.",
        "star_hop": "Look southeast, roughly a third up the sky. Look for a steady, non-twinkling warm yellow light."
    },
    {
        "id": "jupiter",
        "name": "Jupiter (The King of Planets)",
        "type": "planet",
        "ra_hours": 4.5,
        "dec_deg": 21.0,
        "magnitude": -2.7,
        "significance": "The brightest object in the midnight autumn sky, outshining all stars.",
        "star_hop": "Rising in the east around mid-evening. An unmistakably brilliant beacon of pure white light."
    },
    {
        "id": "pleiades",
        "name": "The Pleiades / Seven Sisters (M45)",
        "type": "open_cluster",
        "ra_hours": 3.79,
        "dec_deg": 24.1,
        "magnitude": 1.6,
        "significance": "A glittering cluster of young sapphire-blue stars swathed in reflection nebulosity.",
        "star_hop": "Follow the line from Cassiopeia toward the eastern horizon. Looks like a tiny diamond-dipper of shimmering blue sparks."
    },
    {
        "id": "cygnus",
        "name": "Cygnus (The Northern Cross)",
        "type": "constellation",
        "ra_hours": 20.5,
        "dec_deg": 42.0,
        "magnitude": 1.25,
        "significance": "Soaring along the spine of the Milky Way, holding the supergiant star Deneb.",
        "star_hop": "Near the zenith (overhead). Spot the giant celestial cross flying south along the starry dust lane."
    },
    {
        "id": "polaris",
        "name": "Polaris (The North Star)",
        "type": "star",
        "ra_hours": 2.5,
        "dec_deg": 89.26,
        "magnitude": 1.98,
        "significance": "The pivot of the northern sky, remaining motionless as the Earth spins.",
        "star_hop": "Face true north. Its elevation directly equals your latitude above the horizon."
    }
]


def azimuth_to_cardinal(az_deg: float) -> str:
    """Converts azimuth degrees (0-360) to 16-point cardinal compass text."""
    dirs = [
        "North", "North-North-East", "North-East", "East-North-East",
        "East", "East-South-East", "South-East", "South-South-East",
        "South", "South-South-West", "South-West", "West-South-West",
        "West", "West-North-West", "North-West", "North-North-West"
    ]
    idx = round(az_deg / 22.5) % 16
    return dirs[idx]


def elevation_description(alt_deg: float) -> str:
    """Provides natural physical guidance for eye elevation."""
    if alt_deg < 0:
        return "Below horizon"
    elif alt_deg < 15:
        return "Low on the horizon (one fist-width above tree line)"
    elif alt_deg < 35:
        return "Lower sky (two to three fist-widths up)"
    elif alt_deg < 60:
        return "Mid-sky (roughly halfway between horizon and overhead)"
    elif alt_deg < 80:
        return "High in the heavens (tilt head well back)"
    else:
        return "Directly overhead at zenith (straight up)"


class CelestialEngine:
    def __init__(self, lat: float = 37.7749, lon: float = -122.4194, elevation_m: float = 50.0):
        self.lat = lat
        self.lon = lon
        self.elevation_m = elevation_m

    def compute_visible_sky(self, utc_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Computes the real-time altitude and azimuth for celestial targets.
        Filters to targets currently above the horizon (Altitude > 10°).
        """
        if utc_time is None:
            utc_time = datetime.now(timezone.utc)

        visible_objects = []

        if ASTROPY_AVAILABLE:
            try:
                obs_time = Time(utc_time)
                location = EarthLocation(lat=self.lat * u.deg, lon=self.lon * u.deg, height=self.elevation_m * u.m)
                altaz_frame = AltAz(obstime=obs_time, location=location)

                for target in CELESTIAL_TARGETS:
                    coord = SkyCoord(ra=target["ra_hours"] * u.hourangle, dec=target["dec_deg"] * u.deg)
                    target_altaz = coord.transform_to(altaz_frame)

                    alt = float(target_altaz.alt.deg)
                    az = float(target_altaz.az.deg)

                    if alt >= 10.0:  # Visible above tree line / ground clutter
                        cardinal = azimuth_to_cardinal(az)
                        elev_desc = elevation_description(alt)

                        visible_objects.append({
                            **target,
                            "altitude_deg": round(alt, 1),
                            "azimuth_deg": round(az, 1),
                            "cardinal_direction": cardinal,
                            "elevation_description": elev_desc,
                            "is_visible": True,
                        })
            except Exception as e:
                print(f"[CelestialEngine] Astropy compute exception: {e}, using mathematical fallback")
                visible_objects = self._approximate_sky(utc_time)
        else:
            visible_objects = self._approximate_sky(utc_time)

        # Sort by prominence: planets & bright stars first, then high-altitude targets
        visible_objects.sort(key=lambda x: (x["magnitude"], -x["altitude_deg"]))
        return visible_objects

    def _approximate_sky(self, utc_time: datetime) -> List[Dict[str, Any]]:
        """Fallback analytical calculation based on Local Sidereal Time."""
        # Approximate Local Sidereal Time (LST)
        d = (utc_time - datetime(2000, 1, 1, 12, tzinfo=timezone.utc)).total_seconds() / 86400.0
        gmst = (18.697374558 + 24.06570982441908 * d) % 24
        lst = (gmst + self.lon / 15.0) % 24

        visible = []
        for target in CELESTIAL_TARGETS:
            hour_angle = (lst - target["ra_hours"]) * 15.0  # degrees
            ha_rad = math.radians(hour_angle)
            dec_rad = math.radians(target["dec_deg"])
            lat_rad = math.radians(self.lat)

            # Altitude
            sin_alt = math.sin(dec_rad) * math.sin(lat_rad) + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha_rad)
            alt = math.degrees(math.asin(max(-1.0, min(1.0, sin_alt))))

            if alt >= 10.0:
                # Azimuth
                cos_az = (math.sin(dec_rad) - math.sin(alt * math.pi / 180.0) * math.sin(lat_rad)) / (
                    math.cos(alt * math.pi / 180.0) * math.cos(lat_rad) + 1e-9
                )
                az = math.degrees(math.acos(max(-1.0, min(1.0, cos_az))))
                if math.sin(ha_rad) > 0:
                    az = 360.0 - az

                visible.append({
                    **target,
                    "altitude_deg": round(alt, 1),
                    "azimuth_deg": round(az, 1),
                    "cardinal_direction": azimuth_to_cardinal(az),
                    "elevation_description": elevation_description(alt),
                    "is_visible": True,
                })
        return visible


if __name__ == "__main__":
    engine = CelestialEngine(lat=37.7749, lon=-122.4194)
    sky = engine.compute_visible_sky()
    print(f"Visible Celestial Targets ({len(sky)} found):")
    for obj in sky[:5]:
        print(f" - {obj['name']}: {obj['cardinal_direction']}, {obj['altitude_deg']}° alt ({obj['elevation_description']})")
