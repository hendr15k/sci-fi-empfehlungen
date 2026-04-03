const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);

  let readCount = await page.$eval('#readCount', el => el.innerText);
  console.log('Initial readCount:', readCount);

  // Click first checkbox
  await page.click('.book-grid .book-card:first-child .read-cb input');
  await page.waitForTimeout(500);

  readCount = await page.$eval('#readCount', el => el.innerText);
  let readPct = await page.$eval('#readPct', el => el.innerText);
  console.log('After clicking 1 checkbox:', readCount, 'Pct:', readPct);

  // Random pick
  await page.click('#randomBtn');
  await page.waitForTimeout(500);

  // Click mark as read in random section
  await page.click('.random-result div:last-child');
  await page.waitForTimeout(500);

  readCount = await page.$eval('#readCount', el => el.innerText);
  console.log('After random mark as read:', readCount);

  // Click reset
  page.on('dialog', async dialog => {
      console.log('Dialog:', dialog.message());
      await dialog.accept();
  });
  await page.click('#resetBtn');
  await page.waitForTimeout(500);

  readCount = await page.$eval('#readCount', el => el.innerText);
  console.log('After reset:', readCount);

  await browser.close();
})();
