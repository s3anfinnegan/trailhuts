# TrailHuts

A public, mobile-first web map of trail shelters — lean-tos, bothies, and
emergency shelters — across the island of Ireland (Republic of Ireland and
Northern Ireland). Live at [trailhuts.ie](https://trailhuts.ie) (not yet
deployed).

Inspired by the look and feel of [howffmap.co.uk](https://howffmap.co.uk/)
(the Scottish bothy map) — full-screen map, slim header, search, filters,
layer switcher, locate-me — but with its own name, branding, and codebase.

## Status

Early scaffolding. v1 goal: let a hiker find shelters on a map. No accounts,
GPX export, offline mode, or condition reports yet — see
[the project plan](#) for the full roadmap.

## Shelter types

| Type | Meaning |
|---|---|
| `lean_to` | Open, Adirondack-style, three-sided shelter |
| `bothy` | Enclosed hut or building open to the public |
| `emergency` | Weather shelter / refuge |

## Repo layout

- `data/` — the shelter database: one JSON file per shelter under
  `data/shelters/`, a JSON Schema in `data/schema/`, and raw OSM query
  output in `data/raw/`. **Source of truth**, licensed under
  [ODbL 1.0](./DATA_LICENSE) — see that file for attribution requirements.
- `scripts/` — Python: Overpass queries, Irish Grid/ITM → WGS84 conversion,
  schema validation, and the build step that merges curated shelters into
  the GeoJSON the site consumes.
- `site/` — the map itself: TypeScript + Vite + MapLibre GL JS, tiles from
  [Protomaps'](https://protomaps.com/) hosted API.

## Local development

```sh
# 1. Python scripts: set up the venv, validate data, build the GeoJSON the
#    site reads. Re-run the last step whenever you add/edit a shelter.
cd scripts
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python validate.py
.venv/bin/python build_geojson.py

# 2. Site
cd ../site
npm install
cp .env.example .env.local     # add a free API key from https://protomaps.com/dashboard
npm run dev                    # http://localhost:5173
```

The data build (step 1's last command) is deliberately a separate step from
`npm run dev`/`npm run build`, not chained — if your Node install and your
Python aren't in the same OS environment (e.g. Node on Windows, Python in
WSL), a chained npm script can't shell out to `python3` correctly. Vercel's
own build runs both steps itself (see `vercel.json`), so this only matters
for local dev.

Without a Protomaps API key the map will fail to load (shown via an error on
the splash screen) — the chips/search/filters UI still renders either way.

## Data & attribution

Shelter data is hand-curated and cross-checked against OpenStreetMap. Map
tiles and any OSM-derived shelter candidates require attribution to
[OpenStreetMap contributors](https://www.openstreetmap.org/copyright)
(ODbL). See [DATA_LICENSE](./DATA_LICENSE).

Many shelters sit on Coillte, National Park, or private land, and there is
no general legal right of access in Ireland — always check access
conditions before you go. See the "Before you go" section on the live site.

## License

Code is [MIT](./LICENSE). Data is [ODbL 1.0](./DATA_LICENSE).

## Contributing

Know a shelter that's missing, closed, or out of date? See
[CONTRIBUTING.md](./CONTRIBUTING.md).
