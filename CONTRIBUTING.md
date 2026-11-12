# Contributing to TrailHuts

TrailHuts has no backend, accounts, or database — the data lives in this
git repo as JSON files, and every change is reviewed by hand before it goes
live. There's no self-serve "add a shelter" button in v1, by design.

## Reporting a shelter (missing, wrong, or closed)

Two options:

1. **Open an issue** describing the shelter: name, rough location
   (grid reference, lat/lon, or just a description + nearby trail), type
   (`lean_to` / `bothy` / `emergency`), and a source (a trip report, OSM
   link, maintainer's website, etc.) if you have one.
2. **Email** — see the contact link on [trailhuts.ie](https://trailhuts.ie).

If you're comfortable with git/JSON, a pull request is even more useful —
see below.

## Submitting a shelter via pull request

1. Copy the schema at `data/schema/shelter.schema.json` and an existing
   record in `data/shelters/` as a template.
2. Add a new file `data/shelters/<your-shelter-id>.json` (kebab-case id,
   matching the `id` field).
3. Fill in as many fields as you can. At minimum: `id`, `name`, `type`,
   `lat`, `lon`, `status`, and at least one entry in `sources`.
4. If your only source is an Irish Grid or ITM reference (e.g.
   `"T 074 861"`), put it in `grid_ref` / `grid_system` and leave `lat`/`lon`
   for us to fill in via `scripts/convert_grid.py` — or run it yourself.
5. Run `python scripts/validate.py` locally and fix anything it flags.
6. Open a PR. CI runs the same validation; a maintainer reviews and merges.

## What we're verifying before merging

- The shelter actually exists / existed (not a tent pad, not a day shelter
  at a visitor centre, not someone's private cabin).
- Access: is it genuinely open to hikers, or does it need prior
  registration (e.g. Wild Nephin)? Note this in `access_notes`.
- Land ownership/maintainer, if known — helps future contributors verify
  status changes with the right people.

Records with no recent confirmation are marked `status: unverified` and
flagged in the UI rather than rejected — partial information is still
useful, as long as it's honestly labeled.

## Not in scope (for now)

- GPX tracks/routes to shelters.
- Scraped data from Komoot or AllTrails — use them as leads to go verify in
  person or against OSM/official sources, not as a data source to copy from.
- Condition reports / check-ins (planned for a later version, not v1).
