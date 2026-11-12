#!/usr/bin/env python3
"""Query OSM (via Overpass) for amenity=shelter and tourism=wilderness_hut
across the island of Ireland (Republic + Northern Ireland), save the raw
response to data/raw/, and write a human-readable summary.

Uses OSM admin-boundary areas (not a lat/lon bbox) so results are limited to
ROI + NI and don't pick up neighbouring bits of Scotland/Wales/Isle of Man
that a naive bounding box over the island would catch.
"""
import json
import sys
from collections import Counter
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW_OUTPUT_PATH = ROOT / "data" / "raw" / "overpass-ireland.json"
SUMMARY_OUTPUT_PATH = ROOT / "data" / "raw" / "osm-summary.md"

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

QUERY = """
[out:json][timeout:180];
area["ISO3166-1"="IE"][admin_level=2]->.roi;
area["ISO3166-2"="GB-NIR"]->.ni;
(
  nwr["amenity"="shelter"](area.roi);
  nwr["amenity"="shelter"](area.ni);
  nwr["tourism"="wilderness_hut"](area.roi);
  nwr["tourism"="wilderness_hut"](area.ni);
);
out center tags;
"""


HEADERS = {"User-Agent": "TrailHuts-dev/0.1 (https://trailhuts.ie)"}


def fetch(query: str) -> dict:
    response = requests.post(OVERPASS_URL, data={"data": query}, headers=HEADERS, timeout=200)
    response.raise_for_status()
    return response.json()


# shelter_type values that are essentially never a hiking trail shelter
# (bus/tram stop shelters, picnic gazebos, bike parking, etc).
_NOISE_SHELTER_TYPES = {
    "public_transport",
    "gazebo",
    "picnic_shelter",
    "bicycle_parking",
    "smoking",
    "bathing_shelter",
    "changing_rooms",
    "parking",
    "pavilion",
    "pergola",
}

# shelter_type values worth a human look as real trail-shelter candidates.
_CANDIDATE_SHELTER_TYPES = {"lean_to", "basic_hut", "weather_shelter", "dugout", "wildlife_hide"}


def _location(el: dict) -> tuple[float | None, float | None]:
    if "lat" in el:
        return el["lat"], el["lon"]
    center = el.get("center", {})
    return center.get("lat"), center.get("lon")


def summarize(data: dict) -> str:
    elements = data.get("elements", [])
    lines = [
        "# OSM shelter/wilderness_hut summary\n",
        f"Total elements returned by Overpass (amenity=shelter OR tourism=wilderness_hut, "
        f"ROI+NI admin areas): {len(elements)}\n",
        "**Most `amenity=shelter` hits are bus-stop/picnic/gazebo shelters, not trail "
        "shelters** — OSM overloads this tag heavily. The breakdown and candidate list below "
        "filter for that; see `overpass-ireland.json` for the untouched raw response.\n",
    ]

    by_tag = Counter()
    by_shelter_type = Counter()

    for el in elements:
        tags = el.get("tags", {})
        if tags.get("amenity") == "shelter":
            by_tag["amenity=shelter"] += 1
            by_shelter_type[tags.get("shelter_type", "(untagged)")] += 1
        if tags.get("tourism") == "wilderness_hut":
            by_tag["tourism=wilderness_hut"] += 1

    lines.append("## By primary tag\n")
    for tag, count in by_tag.most_common():
        lines.append(f"- `{tag}`: {count}")

    lines.append("\n## `amenity=shelter` by `shelter_type`\n")
    for shelter_type, count in by_shelter_type.most_common():
        flag = " — noise, excluded below" if shelter_type in _NOISE_SHELTER_TYPES else ""
        lines.append(f"- `{shelter_type}`: {count}{flag}")

    # Candidates worth a human look: any wilderness_hut, any real shelter_type
    # hit that's named, or an unnamed lean_to/basic_hut/dugout/wildlife_hide
    # (those shelter_types are rare enough island-wide that even unnamed ones
    # are worth a look). Unnamed weather_shelter/dugout noise is common enough
    # (mostly bare amenity=shelter nodes with no other context — plausibly
    # urban street furniture) that it's reported as a count only, not listed,
    # until we can cross-filter by distance from a trail.
    def is_candidate(el: dict) -> bool:
        tags = el.get("tags", {})
        if tags.get("tourism") == "wilderness_hut":
            return True
        shelter_type = tags.get("shelter_type")
        if shelter_type not in _CANDIDATE_SHELTER_TYPES:
            return False
        if shelter_type in ("lean_to", "basic_hut"):
            return True
        return "name" in tags

    candidates = [el for el in elements if is_candidate(el)]
    unnamed_weather_shelters = sum(
        1
        for el in elements
        if el.get("tags", {}).get("shelter_type") == "weather_shelter" and "name" not in el.get("tags", {})
    )

    lines.append(
        f"\n({unnamed_weather_shelters} additional unnamed `weather_shelter` nodes exist with no "
        "other context — deferred until we can cross-filter by distance from a trail; not listed below.)\n"
    )
    lines.append(f"## Candidates worth reviewing ({len(candidates)})\n")
    lines.append("| name | osm type/id | lat,lon | tag | operator/access |")
    lines.append("|---|---|---|---|---|")
    for el in sorted(candidates, key=lambda e: e.get("tags", {}).get("name") or "zzz"):
        tags = el.get("tags", {})
        name = tags.get("name", "*(unnamed)*")
        lat, lon = _location(el)
        tag = (
            "tourism=wilderness_hut"
            if tags.get("tourism") == "wilderness_hut"
            else f"shelter_type={tags.get('shelter_type')}"
        )
        op_access = ", ".join(filter(None, [tags.get("operator"), tags.get("access")])) or "-"
        lines.append(
            f"| {name} | {el['type']}/{el['id']} | {lat:.5f},{lon:.5f} | {tag} | {op_access} |"
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    print("Querying Overpass API for amenity=shelter / tourism=wilderness_hut in IE + NI...")
    data = fetch(QUERY)

    RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_OUTPUT_PATH.write_text(json.dumps(data, indent=2))
    print(f"Saved raw response to {RAW_OUTPUT_PATH.relative_to(ROOT)}")

    summary = summarize(data)
    SUMMARY_OUTPUT_PATH.write_text(summary)
    print(f"Saved summary to {SUMMARY_OUTPUT_PATH.relative_to(ROOT)}")
    print(f"\n{len(data.get('elements', []))} total elements found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
