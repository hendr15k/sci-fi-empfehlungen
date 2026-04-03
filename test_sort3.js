const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);

  console.log('Testing Rating sort...');
  await page.click('[data-sort="rating"]');
  await page.waitForTimeout(500);

  let titles = await page.$$eval('.book-grid .book-card', els => els.slice(0, 10).map(e => e.querySelector('.book-title').innerText.replace(/\n/g, ' ')));
  let ratings = await page.$$eval('.book-grid .book-card', els => els.slice(0, 10).map(e => e.querySelector('.rating').innerText));

  for(let i=0; i<10; i++) {
     console.log(`${titles[i]} - ${ratings[i]}`);
  }

  await browser.close();
})();
