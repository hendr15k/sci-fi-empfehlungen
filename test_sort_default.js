const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);

  await page.click('[data-sort="rating"]');
  await page.waitForTimeout(500);

  await page.click('[data-sort="default"]');
  await page.waitForTimeout(500);

  let titles = await page.$$eval('.book-grid .book-card', els => els.slice(0, 3).map(e => e.querySelector('.book-title').innerText));
  console.log('After sorting by rating, default sort top 3:', titles.map(t => t.replace(/\n/g, ' ')));

  await browser.close();
})();
