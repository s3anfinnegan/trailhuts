#!/usr/bin/env python3
"""Merge data/shelters/*.json into a single GeoJSON FeatureCollection for the site.

Output: site/public/data/shelters.geojson (gitignored build artifact — run
this as part of `npm run build` / `npm run dev`, don't commit the result).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELTERS_DIR = ROOT / "data" / "shelters"
OUTPUT_PATH = ROOT / "site" / "public" / "data" / "shelters.geojson"

# Properties carried through to the GeoJSON Feature as-is; lat/lon become
# the Point geometry instead of being duplicated into properties.
PASSTHROUGH_FIELDS = [
    "id",
    "name",
    "type",
    "county",
    "region",
    "enclosed",
    "fireplace",
    "capacity",
    "owner_or_maintainer",
    "status",
    "last_verified",
    "access_notes",
    "sources",
    "photo",
    "notes",
]


def shelter_to_feature(record: dict) -> dict:
    properties = {field: record[field] for field in PASSTHROUGH_FIELDS if field in record}
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [record["lon"], record["lat"]],
        },
        "properties": properties,
    }


def main() -> int:
    shelter_files = sorted(SHELTERS_DIR.glob("*.json"))
    features = [shelter_to_feature(json.loads(p.read_text())) for p in shelter_files]

    feature_collection = {"type": "FeatureCollection", "features": features}

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(feature_collection, indent=2))
    print(f"Wrote {len(features)} shelter(s) to {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
