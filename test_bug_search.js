const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);

  await page.fill('#searchInput', 'asdfqwer');
  await page.waitForTimeout(500);
  let count = await page.$$eval('.book-grid .book-card', els => els.length);
  console.log('Search "asdfqwer" results:', count);

  await page.fill('#searchInput', 'Dune');
  await page.waitForTimeout(500);
  count = await page.$$eval('.book-grid .book-card', els => els.length);
  console.log('Search "Dune" results:', count);

  await page.fill('#searchInput', 'Herbert');
  await page.waitForTimeout(500);
  count = await page.$$eval('.book-grid .book-card', els => els.length);
  console.log('Search "Herbert" results:', count);

  await page.fill('#searchInput', 'Frank');
  await page.waitForTimeout(500);
  count = await page.$$eval('.book-grid .book-card', els => els.length);
  console.log('Search "Frank" results:', count);

  await browser.close();
})();
