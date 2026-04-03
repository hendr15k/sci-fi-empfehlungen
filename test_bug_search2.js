const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);

  await page.click('[data-filter="Hard-SF"]');
  await page.waitForTimeout(500);

  await page.fill('#searchInput', 'Dune');
  await page.waitForTimeout(500);
  let count = await page.$$eval('.book-grid .book-card', els => els.length);
  console.log('Search "Dune" with Hard-SF filter results:', count);

  await browser.close();
})();
