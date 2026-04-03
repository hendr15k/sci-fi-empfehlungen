const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);
  const title = await page.title();
  console.log('Title:', title);
  const h1 = await page.$eval('h1', el => el.innerText);
  console.log('H1:', h1);
  await browser.close();
})();
