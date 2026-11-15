"""Generate the synthetic terrain fixture used by the local demo."""

from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from app.terrain import create_synthetic_elevation


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "sample_elevation.tif"


def main() -> None:
    """Write a deterministic, local-only GeoTIFF for development and tests."""

    elevation = create_synthetic_elevation()
    transform = from_origin(0.0, 0.0, 10.0, 10.0)
    with rasterio.open(
        OUTPUT_PATH,
        "w",
        driver="GTiff",
        height=elevation.shape[0],
        width=elevation.shape[1],
        count=1,
        dtype=elevation.dtype,
        crs=None,
        transform=transform,
    ) as dataset:
        dataset.write(elevation, 1)

    print(f"Wrote synthetic terrain fixture: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
