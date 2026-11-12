# TrailHuts <-> OSM tag mapping

Provisional — to be confirmed once `scripts/overpass_query.py` shows us how
these are actually tagged in the wild on the island of Ireland. The goal is
to be able to round-trip a confirmed TrailHuts record back into an OSM
edit/upload.

| TrailHuts `type` | OSM tags |
|---|---|
| `lean_to` | `amenity=shelter` + `shelter_type=lean_to` |
| `bothy` | `tourism=wilderness_hut` (enclosed, usually unlocked, overnight stays expected) — or `amenity=shelter` + `shelter_type=basic_hut` for a more day-use/no-overnight enclosed hut. Which one depends on the specific shelter; check against OSM's wiki definitions before tagging. |
| `emergency` | `amenity=shelter` + `shelter_type=weather_shelter` (exact value TBD against real-world Overpass results — could also be `shelter_type=public_transport` miscategorized, or untagged `shelter_type`, in existing OSM data) |

Other fields we track that aren't 1:1 with a single OSM tag:

- `enclosed` → roughly implied by the tag choice above, but we store it
  explicitly since OSM tagging in this area is inconsistent.
- `fireplace` → OSM `fireplace=yes/no` on the same node/way.
- `capacity` → OSM `capacity=<number>`.
- `owner_or_maintainer` → OSM `operator=*`.
- `access_notes` → no clean OSM equivalent; closest is `access=*` (e.g.
  `access=permit`) plus free text, which loses nuance — keep our
  `access_notes` as the richer source and only set a coarse `access=*` when
  contributing back.

This file will be revised once we've looked at real Overpass results for
amenity=shelter / tourism=wilderness_hut across Ireland.
