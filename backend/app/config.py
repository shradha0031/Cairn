"""Central assumptions for the demo.

These values are adjustable placeholders, not official NASA values.
"""

from pydantic import BaseModel, ConfigDict


class Assumptions(BaseModel):
    """Operational assumptions used by later terrain and safety calculations."""

    model_config = ConfigDict(frozen=True)

    site_name: str = "Jezero Crater"
    suit_oxygen_duration_minutes: float = 480.0
    oxygen_consumption_rate_per_minute: float = 1.0
    safety_margin: float = 0.20
    walking_speed_kmh: float = 4.0
    slope_speed_penalty: float = 0.08
    maximum_walkable_slope_degrees: float = 25.0
    equipment_load_factor: float = 0.85
    return_threshold_minutes: float = 15.0


ASSUMPTIONS = Assumptions()
