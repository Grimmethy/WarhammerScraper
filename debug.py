import asyncio
from playwright.async_api import async_playwright

async def debug():
    async with async_playwright() as pw:
        browser = await pw.firefox.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
        )
        await page.goto(
            "https://www.warhammer.com/en-US/shop/age-of-sigmar/grand-alliance-destruction/gloomspite-gitz",
            wait_until="domcontentloaded",
            timeout=60000,
        )
        await page.wait_for_timeout(6000)

        title = await page.title()
        card_count = await page.evaluate(
            "document.querySelectorAll('[data-testid=\"product-list-item\"]').length"
        )
        all_testids = await page.evaluate(
            "[...new Set([...document.querySelectorAll('[data-testid]')].map(e => e.dataset.testid))].slice(0,30)"
        )
        body_snippet = await page.evaluate("document.body.innerText.slice(0, 400)")

        print("Title:", title)
        print("Card count:", card_count)
        print("Test IDs found:", all_testids)
        print("Body snippet:", body_snippet)
        await browser.close()

asyncio.run(debug())
