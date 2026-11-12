#!/usr/bin/env python3
"""Validate every data/shelters/*.json record against data/schema/shelter.schema.json."""
import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "data" / "schema" / "shelter.schema.json"
SHELTERS_DIR = ROOT / "data" / "shelters"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft7Validator(schema)

    shelter_files = sorted(SHELTERS_DIR.glob("*.json"))
    if not shelter_files:
        print(f"No shelter files found in {SHELTERS_DIR}")
        return 0

    error_count = 0
    seen_ids = {}

    for path in shelter_files:
        try:
            record = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            print(f"{path.name}: invalid JSON ({e})")
            error_count += 1
            continue

        for error in sorted(validator.iter_errors(record), key=str):
            print(f"{path.name}: {error.message} (at {'/'.join(map(str, error.path)) or '<root>'})")
            error_count += 1

        record_id = record.get("id")
        if record_id != path.stem:
            print(f"{path.name}: id '{record_id}' does not match filename '{path.stem}'")
            error_count += 1
        if record_id in seen_ids:
            print(f"{path.name}: duplicate id '{record_id}' (also in {seen_ids[record_id]})")
            error_count += 1
        elif record_id:
            seen_ids[record_id] = path.name

    if error_count:
        print(f"\n{error_count} error(s) across {len(shelter_files)} file(s).")
        return 1

    print(f"OK: {len(shelter_files)} shelter record(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
