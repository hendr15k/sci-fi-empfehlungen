const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);

  // Test search
  await page.fill('#searchInput', 'asdfqwer');
  await page.waitForTimeout(500);
  let count = await page.$$eval('.book-grid .book-card', els => els.length);
  console.log('Search "asdfqwer" results:', count);

  await page.fill('#searchInput', '');
  await page.waitForTimeout(500);

  // Test filters
  const filters = ['Hard-SF', 'First Contact', 'Cyberpunk', 'Military', 'Klassiker', 'Solarpunk', 'Magischer Realismus', 'Alt-History', 'Soziale SF'];
  for (const f of filters) {
    const selector = `[data-filter="${f}"]`;
    const exists = await page.$(selector);
    if (exists) {
        await page.click(selector);
        await page.waitForTimeout(100);
        let c = await page.$$eval('.book-grid .book-card', els => els.length);
        console.log(`Filter ${f}:`, c);
    } else {
        console.log(`Filter ${f} button not found`);
    }
  }

  await browser.close();
})();
