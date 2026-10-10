"""
Celestial Mechanics & Anatomical Sky Alignment Engine for Whispers of the Sky (WOTS).
Calculates real-time horizontal coordinates (Altitude/Azimuth), visibility,
and observer body-aligned sky tours (Head, Feet, Shoulders, Zenith)
with rich historical lore, mythology, and astrophysics.
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


# Catalog of major sky targets for naked-eye stargazing with rich historical lore
CELESTIAL_TARGETS = [
    {
        "id": "cassiopeia",
        "name": "Cassiopeia (The Celestial Queen)",
        "type": "constellation",
        "ra_hours": 1.0,
        "dec_deg": 60.0,
        "magnitude": 2.2,
        "significance": "Distinctive 'W' shape in the northern sky, pointer to the Andromeda Galaxy and North Star.",
        "star_hop": "Look north, about two-thirds up from horizon. Spot the five bright stars forming a reclining 'W'.",
        "history_lore": "In ancient Greek mythology, Queen Cassiopeia's boast of incomparable beauty angered the sea god Poseidon, chaining her to circle eternally around the celestial pole upside down. In ancient Arabic astronomy, these five stars were known as 'Al-Kaff al-Khadib'—the hand stained with henna. Its central star, Gamma Cassiopeiae, spins so rapidly at over 400 kilometers per second that it bulges at the equator and hurls glowing rings of hydrogen into deep space."
    },
    {
        "id": "andromeda_galaxy",
        "name": "Andromeda Galaxy (M31)",
        "type": "deep_sky",
        "ra_hours": 0.71,
        "dec_deg": 41.27,
        "magnitude": 3.44,
        "significance": "Farthest object visible to the naked human eye at 2.5 million light-years away.",
        "star_hop": "From the point of Cassiopeia's 'W', follow the arrow down toward the Great Square of Pegasus. Look for an elongated misty smudge.",
        "history_lore": "The faint misty oval you see is an island universe containing over one trillion suns. Its photons began their journey across the intergalactic void 2.5 million years ago, when early hominids like Australopithecus first walked on the African savanna. First cataloged in 964 AD by Persian astronomer Abd al-Rahman al-Sufi as the 'little cloud', it is the only object visible to your unaided eye beyond our own Milky Way galaxy."
    },
    {
        "id": "pegasus",
        "name": "The Great Square of Pegasus",
        "type": "asterism",
        "ra_hours": 23.0,
        "dec_deg": 20.0,
        "magnitude": 2.5,
        "significance": "Dominates the southern autumn sky; ancient marker of clear autumn air.",
        "star_hop": "Look for four bright stars forming an enormous baseball diamond in the darkness.",
        "history_lore": "In classical antiquity, these stars formed the winged horse of Bellerophon who sprang from Medusa's neck. In Chinese astronomy, this square formed the Black Tortoise of the North and the imperial resting palace. The darkness inside the square was used by ancient desert navigators to test visual acuity—counting more than six faint stars inside the diamond meant exceptional, crystal-clear atmospheric transparency."
    },
    {
        "id": "summer_triangle",
        "name": "The Summer Triangle (Deneb, Vega, Altair)",
        "type": "asterism",
        "ra_hours": 20.0,
        "dec_deg": 35.0,
        "magnitude": 0.03,
        "significance": "Three brilliant first-magnitude stars framing the Milky Way rift.",
        "star_hop": "Turn west. Look for the piercing sapphire spark of Vega, accompanied by Deneb and Altair.",
        "history_lore": "Vega shines with piercing sapphire brilliance—12,000 years ago it served as humanity's northern pole star, and will do so again in the year 13,727. Deneb is a colossal white supergiant over 200,000 times more luminous than our Sun. Between them lies the Great Rift of the Milky Way, where Chinese folklore saw the silver celestial river separating the Weaver Girl Vega from the Cowherd Altair, allowed to cross only once a year on a bridge of magpies."
    },
    {
        "id": "saturn",
        "name": "Saturn (The Ringed Giant)",
        "type": "planet",
        "ra_hours": 23.2,
        "dec_deg": -7.5,
        "magnitude": 0.6,
        "significance": "A steady, golden ember shining unblinking in the constellation Aquarius.",
        "star_hop": "Look southeast, roughly a third up the sky. Look for a steady, non-twinkling warm yellow light.",
        "history_lore": "Saturn shines with a serene, unblinking golden light—planets do not twinkle like stars because their angular diameter is wide enough to resist atmospheric distortion. Named for the Roman god of agriculture and time, it takes 29.5 Earth years to complete one orbit around the Sun. Its shimmering rings are composed of billions of chunks of ice and rock, remnants of a shattered ancient moon orbiting just 1.4 billion kilometers away."
    },
    {
        "id": "jupiter",
        "name": "Jupiter (The King of Planets)",
        "type": "planet",
        "ra_hours": 4.5,
        "dec_deg": 21.0,
        "magnitude": -2.7,
        "significance": "The brightest object in the midnight autumn sky, outshining all stars.",
        "star_hop": "An unmistakably brilliant, steady white beacon of pure light.",
        "history_lore": "Jupiter outshines every star in the night sky. In 1610, Galileo Galilei aimed his handcrafted telescope at this beacon and discovered four tiny points of light orbiting it—the Galilean moons Io, Europa, Ganymede, and Callisto—shattering the thousand-year geocentric dogma that all celestial bodies orbit the Earth. Jupiter is an immense gas giant containing more mass than all other planets in our solar system combined, acting as a gravitational guardian that shields Earth from wandering comets."
    },
    {
        "id": "pleiades",
        "name": "The Pleiades / Seven Sisters (M45)",
        "type": "open_cluster",
        "ra_hours": 3.79,
        "dec_deg": 24.1,
        "magnitude": 1.6,
        "significance": "A glittering cluster of young sapphire-blue stars swathed in reflection nebulosity.",
        "star_hop": "Follow the line from Cassiopeia toward the eastern horizon. Looks like a tiny diamond-dipper of shimmering blue sparks.",
        "history_lore": "This dazzling cluster of young sapphire-blue stars was born just 100 million years ago, when dinosaurs still walked the Earth. Revered across nearly every human civilization: In Maori tradition, their appearance marks 'Matariki', the dawn of the New Year; in Japan, they are 'Subaru', meaning unity and gathering; in Greek lore, they were the seven daughters of Atlas pursued by Orion across the celestial vault."
    },
    {
        "id": "cygnus",
        "name": "Cygnus (The Northern Cross)",
        "type": "constellation",
        "ra_hours": 20.5,
        "dec_deg": 42.0,
        "magnitude": 1.25,
        "significance": "Soaring along the spine of the Milky Way, holding the supergiant star Deneb.",
        "star_hop": "Near the zenith (overhead). Spot the giant celestial cross flying south along the starry dust lane.",
        "history_lore": "Soaring along the luminous spine of our home galaxy, Cygnus represents the celestial swan of Orpheus or Zeus. At the swan's head rests Albireo—one of the most breathtaking binary star systems in the sky, pairing a golden topaz giant with an electric sapphire companion. Deep in Cygnus lies Cygnus X-1, the very first astronomical black hole ever confirmed by astrophysicists in 1971."
    },
    {
        "id": "polaris",
        "name": "Polaris (The North Star)",
        "type": "star",
        "ra_hours": 2.5,
        "dec_deg": 89.26,
        "magnitude": 1.98,
        "significance": "The pivot of the northern sky, remaining motionless as the Earth spins.",
        "star_hop": "Face true north. Its elevation directly equals your latitude above the horizon.",
        "history_lore": "Polaris is the motionless anchor of the northern hemisphere. Because Earth's rotational axis points almost directly at it, the entire cosmos appears to spin around this solitary spark as the planet rotates beneath your spine. For three millennia, Phoenician navigators, Silk Road traders, and freedom seekers along the Underground Railroad looked to this reliable star to find true north in total darkness."
    },
    {
        "id": "orion",
        "name": "Orion (The Celestial Hunter)",
        "type": "constellation",
        "ra_hours": 5.55,
        "dec_deg": 5.0,
        "magnitude": 0.4,
        "significance": "The most magnificent constellation in the night sky, featuring Betelgeuse and Rigel.",
        "star_hop": "Look toward the east-southeast for three evenly spaced bright stars forming an unmistakable belt.",
        "history_lore": "Orion is humanity's oldest recognized celestial figure—a 32,000-year-old mammoth ivory carving found in Germany depicts this exact arrangement. In Egyptian mythology, Orion was Osiris, god of rebirth and the underworld. At his right shoulder glows Betelgeuse, an aging red supergiant so vast that if placed in our solar system, it would swallow the orbit of Mars. At his left foot burns Rigel, a brilliant blue supergiant radiating the light of 120,000 suns."
    },
    {
        "id": "taurus",
        "name": "Taurus & Aldebaran (The Eye of the Bull)",
        "type": "constellation",
        "ra_hours": 4.6,
        "dec_deg": 16.5,
        "magnitude": 0.85,
        "significance": "Ancient zodiac constellation housing the glowing red eye Aldebaran and the Crab Nebula.",
        "star_hop": "Follow Orion's belt upward to the right until you meet the fiery orange beacon of Aldebaran.",
        "history_lore": "Aldebaran, from the Arabic 'Al-Dabaran' meaning 'The Follower' because it pursues the Pleiades across the night sky, is a fiery orange giant star 65 light-years away. Taurus was depicted in the 17,000-year-old cave paintings of Lascaux in France. Behind Aldebaran lies the Crab Nebula, the glowing cosmic shrapnel of a supernova witnessed and recorded by Chinese and Arab astronomers in the summer of 1054 AD."
    },
    {
        "id": "ursa_major",
        "name": "Ursa Major (The Big Dipper / Great Bear)",
        "type": "constellation",
        "ra_hours": 11.0,
        "dec_deg": 55.0,
        "magnitude": 1.8,
        "significance": "The seven pointer stars of the northern sky; ancient clock and navigator.",
        "star_hop": "Look north near the horizon. The two outer stars of the spoon bowl point directly to Polaris.",
        "history_lore": "Known to indigenous North American tribes as the Celestial Bear pursued by hunters, to ancient Greeks as the nymph Callisto, and to Celtic Britons as King Arthur's Chariot. Its two front stars, Merak and Dubhe, are the 'Pointers'—drawing an arrow straight through empty space into Polaris. The second star in the handle, Mizar, forms a naked-eye double star with Alcor that ancient Arabian warriors and Roman legions used as an eye test before battle."
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


def angle_difference(a1: float, a2: float) -> float:
    """Computes the shortest angular difference in degrees between two azimuths."""
    return abs((a1 - a2 + 180.0) % 360.0 - 180.0)


class CelestialEngine:
    def __init__(self, lat: float = 37.7749, lon: float = -122.4194, elevation_m: float = 50.0):
        self.lat = lat
        self.lon = lon
        self.elevation_m = elevation_m

    def compute_visible_sky(self, utc_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Computes the real-time altitude and azimuth for celestial targets.
        Filters to targets currently above the horizon (Altitude > 8°).
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

                    if alt >= 8.0:
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
                print(f"[CelestialEngine] Astropy compute note: {e}, using mathematical model")
                visible_objects = self._approximate_sky(utc_time)
        else:
            visible_objects = self._approximate_sky(utc_time)

        # Sort by visual prominence
        visible_objects.sort(key=lambda x: (x["magnitude"], -x["altitude_deg"]))
        return visible_objects

    def _approximate_sky(self, utc_time: datetime) -> List[Dict[str, Any]]:
        """High-precision analytical calculation based on Local Sidereal Time."""
        d = (utc_time - datetime(2000, 1, 1, 12, tzinfo=timezone.utc)).total_seconds() / 86400.0
        gmst = (18.697374558 + 24.06570982441908 * d) % 24
        lst = (gmst + self.lon / 15.0) % 24

        visible = []
        for target in CELESTIAL_TARGETS:
            hour_angle = (lst - target["ra_hours"]) * 15.0
            ha_rad = math.radians(hour_angle)
            dec_rad = math.radians(target["dec_deg"])
            lat_rad = math.radians(self.lat)

            # Altitude
            sin_alt = math.sin(dec_rad) * math.sin(lat_rad) + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha_rad)
            alt = math.degrees(math.asin(max(-1.0, min(1.0, sin_alt))))

            if alt >= 8.0:
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

    def compute_body_aligned_tour(
        self,
        head_heading_deg: float = 0.0,
        utc_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Maps celestial objects to the physical anatomy of an observer lying on their back:
        - Top of phone points toward Head / Crown (head_heading_deg)
        - Bottom of phone points toward Feet ((head_heading_deg + 180) % 360)
        - Left side points toward Left Shoulder ((head_heading_deg + 90) % 360)
        - Right side points toward Right Shoulder ((head_heading_deg + 270) % 360)
        - Zenith points directly above the chest and eyes (Altitude > 65°)
        """
        visible = self.compute_visible_sky(utc_time)
        if not visible:
            return {"error": "No celestial objects currently visible above horizon"}

        head_deg = head_heading_deg % 360.0
        feet_deg = (head_deg + 180.0) % 360.0
        left_deg = (head_deg + 90.0) % 360.0
        right_deg = (head_deg + 270.0) % 360.0

        used_ids = set()

        # 1. Zenith: Highest altitude target overhead
        zenith_candidates = sorted(visible, key=lambda x: -x["altitude_deg"])
        zenith_target = zenith_candidates[0]
        used_ids.add(zenith_target["id"])

        def pick_best(target_deg: float, pool: List[Dict[str, Any]]) -> Dict[str, Any]:
            available = [t for t in pool if t["id"] not in used_ids]
            if not available:
                available = pool
            # Rank by proximity to angle and visibility
            best = min(available, key=lambda t: angle_difference(t["azimuth_deg"], target_deg))
            used_ids.add(best["id"])
            return best

        head_target = pick_best(head_deg, visible)
        feet_target = pick_best(feet_deg, visible)
        left_target = pick_best(left_deg, visible)
        right_target = pick_best(right_deg, visible)

        head_cardinal = azimuth_to_cardinal(head_deg)
        feet_cardinal = azimuth_to_cardinal(feet_deg)
        left_cardinal = azimuth_to_cardinal(left_deg)
        right_cardinal = azimuth_to_cardinal(right_deg)

        # Build personalized spoken narration
        script_paragraphs = [
            # Grounding & posture
            (
                f"Welcome to your personal sky observatory. Your phone is resting face-down upon your chest. "
                f"Your head is resting back toward the {head_cardinal}, your feet stretching forward toward the {feet_cardinal}. "
                f"Close your eyes for three slow, grounding breaths of cool night air. "
                f"Your screen is in complete darkness at zero nits. Over the next twenty minutes, "
                f"your eyes will adapt, growing thousands of times more sensitive to the faint light of the universe."
            ),
            # Zenith (chest)
            (
                f"Now gently open your eyes straight up into the darkness. "
                f"Directly above your chest, at the zenith of the heavens, you are looking toward {zenith_target['name']}. "
                f"{zenith_target['elevation_description']}. "
                f"{zenith_target['history_lore']}"
            ),
            # Head (crown)
            (
                f"Now cast your gaze backward, past the crown of your head toward the {head_cardinal} horizon. "
                f"There rests {head_target['name']}. {head_target['elevation_description']}. "
                f"{head_target['history_lore']}"
            ),
            # Feet (toes)
            (
                f"Now let your eyes sweep downward toward your feet, gazing toward the {feet_cardinal}. "
                f"Rising above your toes is {feet_target['name']}. {feet_target['elevation_description']}. "
                f"{feet_target['history_lore']}"
            ),
            # Left & Right Shoulders
            (
                f"Tilt your awareness to your left, above your left shoulder toward the {left_cardinal}. "
                f"There shines {left_target['name']}. {left_target['history_lore']} "
                f"And turning toward your right shoulder toward the {right_cardinal}, you can trace {right_target['name']}. "
                f"{right_target['history_lore']}"
            ),
            # Stillness & contemplation
            (
                f"Rest here in complete stillness. There is nothing to look at on any screen. "
                f"The solid earth beneath your spine rotates steadily into the dawn, carrying you along a river of stars. "
                f"Breathe, listen, and let the whispers of the sky settle gently over your night."
            )
        ]

        full_script = "\n\n".join(script_paragraphs)

        return {
            "orientation": {
                "head_heading_deg": round(head_deg, 1),
                "head_cardinal": head_cardinal,
                "feet_cardinal": feet_cardinal,
                "left_cardinal": left_cardinal,
                "right_cardinal": right_cardinal
            },
            "body_targets": {
                "zenith": {
                    "body_region": "Directly Overhead (Chest & Eyes)",
                    "target": zenith_target
                },
                "head": {
                    "body_region": f"Past Crown of Head ({head_cardinal})",
                    "target": head_target
                },
                "feet": {
                    "body_region": f"Down Past Feet ({feet_cardinal})",
                    "target": feet_target
                },
                "left_shoulder": {
                    "body_region": f"Above Left Shoulder ({left_cardinal})",
                    "target": left_target
                },
                "right_shoulder": {
                    "body_region": f"Above Right Shoulder ({right_cardinal})",
                    "target": right_target
                }
            },
            "script_paragraphs": script_paragraphs,
            "full_script": full_script
        }


if __name__ == "__main__":
    engine = CelestialEngine(lat=37.7749, lon=-122.4194)
    tour = engine.compute_body_aligned_tour(head_heading_deg=0.0)
    print("Observer Head Facing:", tour["orientation"]["head_cardinal"])
    print("Zenith Target:", tour["body_targets"]["zenith"]["target"]["name"])
    print("Head Target:", tour["body_targets"]["head"]["target"]["name"])
    print("Feet Target:", tour["body_targets"]["feet"]["target"]["name"])
    print("Left Target:", tour["body_targets"]["left_shoulder"]["target"]["name"])
    print("Right Target:", tour["body_targets"]["right_shoulder"]["target"]["name"])
    print("\nSample Spoken Chapter 2:\n", tour["script_paragraphs"][1][:200], "...")
