#!/usr/bin/env python3
"""
Scrape IRS form metadata (filename + description) from the IRS directory
and save to forms/metadata.json.

Usage: python3 scripts/scrape-metadata.py

Requires: pip install playwright && playwright install chromium
"""

import json
import os
import asyncio
from playwright.async_api import async_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(SCRIPT_DIR, "..")
OUT_FILE = os.path.join(REPO_ROOT, "forms", "metadata.json")
BASE_URL = "https://www.irs.gov/downloads/irs-pdf"
TOTAL_PAGES = 63


async def scrape():
    records = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for pg in range(TOTAL_PAGES):
            print(f"  Scraping page {pg + 1}/{TOTAL_PAGES}...", end="\r")
            await page.goto(f"{BASE_URL}?page={pg}", wait_until="networkidle")

            rows = await page.evaluate("""() => {
                const table = document.querySelectorAll('table')[1];
                if (!table) return [];
                return Array.from(table.querySelectorAll('tr')).map(row => {
                    const contentLinks = row.querySelectorAll('.tablesaw-cell-content a');
                    if (!contentLinks.length) return null;
                    const filename = contentLinks[0].textContent.trim();
                    const cells = row.querySelectorAll('td');
                    if (cells.length < 4) return null;
                    const descContent = cells[3].querySelector('.tablesaw-cell-content');
                    const description = descContent ? descContent.textContent.trim() : '';
                    return { filename, description };
                }).filter(r => r && r.filename.endsWith('.pdf'));
            }""")
            records.extend(rows)

        await browser.close()

    print(f"\nScraped {len(records)} total PDF entries.")
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w") as f:
        json.dump(records, f, indent=2)
    print(f"Saved to {OUT_FILE}")


if __name__ == "__main__":
    asyncio.run(scrape())
