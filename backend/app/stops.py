"""Synthetic science and emergency stops for the Jezero demo."""

from dataclasses import dataclass

GridPoint = tuple[int, int]


@dataclass(frozen=True)
class Stop:
    """A labelled map stop with optional, verified photo metadata."""

    stop_id: str
    name: str
    stop_type: str
    point: GridPoint
    safety_rating: str
    description: str
    photo_url: str | None = None
    photo_status: str = "pending verification"


SCIENCE_STOPS = (
    Stop(
        "delta-deposit",
        "Delta deposit",
        "science",
        (54, 88),
        "blue",
        "Layered sedimentary terrain and a candidate ancient river delta.",
        "https://mars.nasa.gov/mars2020-raw-images/pub/ods/surface/sol/02024/ids/edr/browse/zcam/ZL0_2024_0846622583_145EBY_N0930000ZCAM10058_1100LMJ02_320.jpg",
        "NASA Perseverance preview; not georegistered to this synthetic stop",
    ),
    Stop(
        "river-channel",
        "Ancient river channel",
        "science",
        (62, 100),
        "green",
        "A smoother channel approach suitable for careful sampling.",
    ),
    Stop(
        "layered-outcrop",
        "Layered rock outcrop",
        "science",
        (48, 70),
        "blue",
        "Exposed rock layers with a moderate footing caution.",
    ),
)

EMERGENCY_STOPS = (
    Stop("habitat", "Habitat", "emergency", (41, 55), "green", "Primary return point.", photo_status="not applicable"),
    Stop("delta-shelter", "Delta shelter", "emergency", (55, 80), "green", "Synthetic shelter waypoint.", photo_status="not applicable"),
    Stop("rover-cache", "Rover cache", "emergency", (64, 96), "blue", "Synthetic rover support waypoint.", photo_status="not applicable"),
)

ALL_STOPS = SCIENCE_STOPS + EMERGENCY_STOPS
