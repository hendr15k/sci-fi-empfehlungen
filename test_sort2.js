const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);

  // Test sorting by rating
  console.log('Testing Rating sort...');
  await page.click('[data-sort="rating"]');
  await page.waitForTimeout(500);

  // get top 5
  let top5Ratings = await page.$$eval('.book-grid .book-card .rating', els => els.slice(0, 5).map(e => e.innerText));
  console.log('Top 5 ratings:', top5Ratings);

  let bottom5Ratings = await page.$$eval('.book-grid .book-card .rating', els => els.slice(-5).map(e => e.innerText));
  console.log('Bottom 5 ratings:', bottom5Ratings);

  await browser.close();
})();
