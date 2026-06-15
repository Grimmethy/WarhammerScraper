# Trouble Log

Known issues, workarounds, and gotchas encountered during development.

---

## Bot Detection Blocks Headless Scraping

**Problem:** Playwright and plain `requests` are blocked by Warhammer.com's bot detection. Pages either return empty product grids or redirect to a CAPTCHA.

**Fix:** Extract data via JavaScript injection into a live Chrome browser session (see README). The page loads normally in real Chrome; the JS just reads already-rendered DOM nodes.

---

## MCP Output Truncation on Large Arrays

**Problem:** Pulling all products from a faction page in one JS call causes the MCP tool result to be truncated mid-array, producing invalid/incomplete JSON.

**Fix:** Store the full array in a `window` variable first, then pull in slices of ~12 items:

```js
window._data = [...document.querySelectorAll('[data-testid="product-list-item"]')].map(...);
window._data.length;       // confirm total
window._data.slice(0, 12); // pull batch 1
window._data.slice(12, 24); // pull batch 2
// etc.
```

For any entry that still truncates (long filenames), pull individually: `window._data[N]`.

---

## "Show More" Must Be Clicked to Load All Products

**Problem:** Faction pages initially load ~12–24 products. Remaining products only appear after clicking the `[data-testid="button-show-more"]` button, which must be repeated until it disappears.

**Fix:** Click Show More in a loop until the product count stabilizes:

```js
document.querySelector('[data-testid="button-show-more"]')?.click();
document.querySelectorAll('[data-testid="product-list-item"]').length;
```

Large factions (Stormcast Eternals: 54 items) required 3+ rounds of clicks with wait time between each.

---

## URL Query Strings Must Be Stripped

**Problem:** Product card href values include `?queryID=...` tracking parameters. Including these in the xlsx breaks the hyperlinks and pollutes the data.

**Fix:** Strip everything after `?` when extracting slugs:

```js
c.querySelector('[data-testid="product-card-details"]')?.href?.split('/shop/')[1]?.split('?')[0]
```

Same applies to image src URLs — strip after `?`.

---

## MCP Tab Navigation Requires Explicit `navigate` Call

**Problem:** Creating tabs with a URL parameter via `tabs_create_mcp` does not reliably auto-navigate the tab in all sessions. Tabs sometimes open blank.

**Fix:** After creating tabs, explicitly call `navigate` on each tab ID to ensure the page loads.

---

## MCP Tab Group Expires Between Sessions

**Problem:** If a conversation is interrupted and resumed (context compaction), the previous MCP tab group no longer exists, causing all tab IDs to be invalid.

**Fix:** Call `tabs_context_mcp` with `createIfEmpty: true` at the start of each session to create a fresh tab group, then navigate new tabs.

---

## Beasts of Chaos Effectively Retired

**Problem:** The Beasts of Chaos faction page only lists 1 product (Chaos Gargant). This is not a scraping error.

**Cause:** Games Workshop removed Beasts of Chaos from Age of Sigmar 4th edition (2024). The faction page persists but the range has been discontinued.

---

## Image Filenames Are Case-Sensitive

**Problem:** Image filenames extracted from the DOM are mixed-case (e.g., `99120218001_CelestantPrime01.jpg`). The CDN URL is case-sensitive — lowercase versions 404.

**Fix:** Use the filename exactly as extracted from the `img` src attribute. Do not normalize case.
