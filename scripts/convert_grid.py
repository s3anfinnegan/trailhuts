#!/usr/bin/env python3
"""Convert Irish Grid or ITM references to WGS84 lat/lon.

Usage:
    python convert_grid.py irish_grid "T 074 861"
    python convert_grid.py itm 712345 761234

Irish Grid (EPSG:29902) references are the classic "letter + easting +
northing" format used by older OSi maps (e.g. "T 074 861"). ITM (EPSG:2157)
is the modern Irish Transverse Mercator grid, usually given as plain
easting/northing metres.
"""
import re
import sys

from pyproj import Transformer

# The 25 Irish Grid 100km letter squares (no "I"), ordered south-to-north
# so that row_index doubles as the northing band in units of 100km.
_GRID_LETTERS = [
    "VWXYZ",  # northing 0-99km   (southernmost)
    "QRSTU",  # northing 100-199km
    "LMNOP",  # northing 200-299km
    "FGHJK",  # northing 300-399km
    "ABCDE",  # northing 400-499km (northernmost)
]


def irish_grid_letter_to_origin(letter: str) -> tuple[int, int]:
    letter = letter.upper()
    for row_index, row in enumerate(_GRID_LETTERS):
        if letter in row:
            col_index = row.index(letter)
            # Easting/northing of the square's SW corner, in units of 100km.
            easting_100km = col_index
            northing_100km = row_index
            return easting_100km * 100_000, northing_100km * 100_000
    raise ValueError(f"Unknown Irish Grid letter: {letter}")


def parse_irish_grid_ref(ref: str) -> tuple[float, float]:
    """Parse e.g. "T 074 861" into full Irish Grid (EPSG:29902) easting/northing metres."""
    match = re.match(r"^\s*([A-Za-z])\s*(\d+)\s+(\d+)\s*$", ref)
    if not match:
        raise ValueError(
            f"Could not parse Irish Grid reference '{ref}'. "
            'Expected format like "T 074 861".'
        )
    letter, easting_str, northing_str = match.groups()
    if len(easting_str) != len(northing_str):
        raise ValueError(
            f"Easting/northing digit counts differ in '{ref}' "
            f"({easting_str!r} vs {northing_str!r})"
        )
    digits = len(easting_str)
    scale = 10 ** (5 - digits)  # pad to 5-digit (100km square -> 1m resolution)

    origin_easting, origin_northing = irish_grid_letter_to_origin(letter)
    easting = origin_easting + int(easting_str) * scale
    northing = origin_northing + int(northing_str) * scale
    return easting, northing


def irish_grid_to_wgs84(ref: str) -> tuple[float, float]:
    easting, northing = parse_irish_grid_ref(ref)
    transformer = Transformer.from_crs("EPSG:29902", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(easting, northing)
    return lat, lon


def itm_to_wgs84(easting: float, northing: float) -> tuple[float, float]:
    transformer = Transformer.from_crs("EPSG:2157", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(easting, northing)
    return lat, lon


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1

    system = sys.argv[1].lower()
    if system == "irish_grid":
        ref = " ".join(sys.argv[2:])
        lat, lon = irish_grid_to_wgs84(ref)
    elif system == "itm":
        if len(sys.argv) != 4:
            print("itm requires easting and northing as two separate args")
            return 1
        easting, northing = float(sys.argv[2]), float(sys.argv[3])
        lat, lon = itm_to_wgs84(easting, northing)
    else:
        print(f"Unknown grid system '{system}', expected 'irish_grid' or 'itm'")
        return 1

    print(f"lat={lat:.6f} lon={lon:.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
