"""Build a small Mars Trek imagery mosaic for the Jezero demo viewport."""

from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

from PIL import Image

TILE_ROOT = "https://trek.nasa.gov/tiles/Mars/EQ/Mars_Viking_MDIM21_ClrMosaic_global_232m/1.0.0//default/default028mm"
OUTPUT = Path(__file__).resolve().parents[1] / "public" / "data" / "mars-trek-jezero-mosaic.jpg"


def main() -> None:
    """Download only the verified tiles needed for the small Jezero viewport."""

    # One tile avoids visible seams between adjacent low-resolution source tiles.
    # It covers the Jezero latitude band and is fitted to the small demo viewport.
    url = f"{TILE_ROOT}/3/5/3.jpg"
    with urlopen(url, timeout=20) as response:
        crop = Image.open(BytesIO(response.read())).convert("RGB")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    crop.save(OUTPUT, quality=92, optimize=True)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
