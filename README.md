# WarhammerScraper

A Python tool that builds per-faction product catalog spreadsheets for Warhammer Age of Sigmar miniatures. Each `.xlsx` file contains item names, prices, clickable store URLs, embedded 100×100 thumbnails, and full image URLs — one row per product.

## Output

```
data/
├── Destruction/   gloomspite_gitz, orruk_warclans, ogor_mawtribes, sons_of_behemat
├── Death/         flesh_eater_courts, nighthaunt, ossiarch_bonereapers, soulblight_gravelords
├── Order/         cities_of_sigmar, daughters_of_khaine, fyreslayers, idoneth_deepkin,
│                  kharadron_overlords, lumineth_realm_lords, seraphon, stormcast_eternals, sylvaneth
└── Chaos/         beasts_of_chaos, blades_of_khorne, disciples_of_tzeentch, hedonites_of_slaanesh,
                   maggotkin_of_nurgle, skaven, slaves_to_darkness
```

Product images are downloaded to `data/images/` (gitignored — ~250MB, re-generated on build).

## Structure

| File | Purpose |
|---|---|
| `factions.py` | Data registry — all faction product lists |
| `build.py` | Generic builder — downloads images, creates thumbnails, writes xlsx |
| `scraper.py` | Legacy per-faction scraper (superseded by build.py) |

## Usage

```bash
# Build one faction
python build.py stormcast_eternals

# Build multiple
python build.py skaven slaves_to_darkness blades_of_khorne

# Build all
python build.py --all

# List available factions
python build.py --list
```

## Setup

```bash
pip install -r requirements.txt
```

## How Product Data Is Collected

Warhammer.com uses bot detection that blocks headless scrapers (Playwright, requests). Product data is extracted manually via JavaScript injection into a live Chrome browser session using the Claude MCP browser tool:

```js
// Run in browser console on a faction page after clicking "Show More"
window._data = [...document.querySelectorAll('[data-testid="product-list-item"]')].map(c => ([
  c.querySelector('[data-testid="product-card-name"]')?.innerText,
  c.querySelector('[data-testid="product-card-current-price"]')?.innerText,
  c.querySelector('[data-testid="product-card-details"]')?.href?.split('/shop/')[1]?.split('?')[0],
  c.querySelector('[data-testid="product-card-image"] img')?.src?.split('/920x950/')[1]?.split('?')[0]
]));
window._data.length; // confirm count, then pull in slices: window._data.slice(0,12), etc.
```

Results are pasted into `factions.py` under the appropriate alliance key.

## Adding a New Faction

1. Navigate to the faction page on warhammer.com
2. Click "Show More" until all products are loaded
3. Run the JS extraction above in the browser console
4. Pull data in slices of ~12 to avoid truncation
5. Add an entry to `factions.py`:

```python
"faction_key": {
    "title": "Display Name",
    "output": "data/Alliance/faction_key.xlsx",
    "products": [
        ["Item Name", "$price", "url-slug", "image_filename.jpg"],
        ...
    ],
},
```

6. Run `python build.py faction_key`
