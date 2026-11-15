"""Validation helpers for CRISM ENVI products before mineral integration."""

from dataclasses import dataclass
from math import cos, pi
from pathlib import Path
import re

MARS_RADIUS_M = 3394839.813316312
JEZERO_BBOX = (77.0, 18.2, 77.8, 18.8)  # west, south, east, north


@dataclass(frozen=True)
class CrismFootprint:
    """Approximate geographic footprint derived from an ENVI header."""

    west: float
    south: float
    east: float
    north: float

    @property
    def overlaps_jezero(self) -> bool:
        """Return whether this product intersects the Cairn Jezero working area."""

        west, south, east, north = JEZERO_BBOX
        return not (self.east < west or self.west > east or self.north < south or self.south > north)


@dataclass(frozen=True)
class CrismProduct:
    """Validated metadata needed before selecting mineral evidence."""

    product_id: str
    header_path: str
    samples: int
    lines: int
    bands: int
    footprint: CrismFootprint


def _number(pattern: str, text: str, name: str) -> float:
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        raise ValueError(f"CRISM header is missing {name}")
    return float(match.group(1))


def read_crism_product(header_path: str | Path) -> CrismProduct:
    """Read an ENVI header and reject malformed or non-geographic products."""

    path = Path(header_path)
    text = path.read_text(encoding="utf-8", errors="replace")
    samples = int(_number(r"samples\s*=\s*(\d+)", text, "samples"))
    lines = int(_number(r"lines\s*=\s*(\d+)", text, "lines"))
    bands = int(_number(r"bands\s*=\s*(\d+)", text, "bands"))
    map_info = re.search(r"map info\s*=\s*\{([^}]*)\}", text, re.IGNORECASE | re.DOTALL)
    if not map_info:
        raise ValueError("CRISM header is missing map info")

    values = [item.strip() for item in map_info.group(1).split(",")]
    if len(values) < 8:
        raise ValueError("CRISM map info is incomplete")
    origin_x = float(values[3])
    origin_y = float(values[4])
    pixel_x = float(values[5])
    pixel_y = float(values[6])
    standard_parallel = float(re.search(r"lat(\d+(?:\.\d+)?)", values[7], re.IGNORECASE).group(1))
    x_extent = samples * pixel_x
    y_extent = lines * pixel_y
    scale_x = MARS_RADIUS_M * cos(standard_parallel * pi / 180)
    west = origin_x / scale_x * 180 / pi
    east = (origin_x + x_extent) / scale_x * 180 / pi
    north = standard_parallel + (origin_y - origin_y) / MARS_RADIUS_M * 180 / pi
    south = standard_parallel + (origin_y - y_extent - origin_y) / MARS_RADIUS_M * 180 / pi

    product_id = path.stem
    return CrismProduct(product_id, str(path), samples, lines, bands, CrismFootprint(west, south, east, north))
