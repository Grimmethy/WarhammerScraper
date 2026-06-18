// Paste into Chrome DevTools console (or the MCP browser extension) while on a
// Warhammer faction category page. Click "Show More" until all products are visible
// before running. Copy the printed output and paste as the products list inside
// the relevant faction entry in factions.py.
//
// Output format: ["Name", "$Price", "shop-slug", "ImageFilename.jpg"]

(() => {
    const SHOP_BASE = "https://www.warhammer.com/en-US/shop/";
    const IMG_BASE  = "https://www.warhammer.com/app/resources/catalog/product/920x950/";
    const BASE      = "https://www.warhammer.com";

    const cards = document.querySelectorAll('[data-testid="product-list-item"]');
    const results = [];

    for (const card of cards) {
        const nameEl  = card.querySelector('[data-testid="product-card-name"]');
        const priceEl = card.querySelector('[data-testid="product-card-current-price"]');
        const linkEl  = card.querySelector('[data-testid="product-card-details"]');
        const imgEl   = card.querySelector('[data-testid="product-card-image"] img');

        const name  = nameEl  ? nameEl.textContent.trim()  : "";
        const price = priceEl ? priceEl.textContent.trim() : "";

        let slug = "";
        if (linkEl) {
            const href = linkEl.getAttribute("href") || "";
            const url = new URL(href, BASE);
            url.search = "";
            slug = url.toString().replace(SHOP_BASE, "");
        }

        let imageFile = "";
        if (imgEl) {
            const src = imgEl.getAttribute("src") || "";
            const full = src.startsWith("http") ? src : BASE + src;
            imageFile = full.replace(IMG_BASE, "").split("?")[0];
        }

        if (name && slug) {
            results.push([name, price, slug, imageFile]);
        }
    }

    const lines = results.map(([n, p, s, i]) => `    ["${n}", "${p}", "${s}", "${i}"],`);
    console.log(lines.join("\n"));
    return `${results.length} products extracted`;
})();
