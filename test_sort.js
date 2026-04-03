const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);

  // Test sorting by rating
  console.log('Testing Rating sort...');
  await page.click('[data-sort="rating"]');
  await page.waitForTimeout(500);
  let firstRating = await page.$eval('.book-grid .book-card:first-child .rating', el => el.innerText);
  console.log('First rating:', firstRating);

  // Test sorting by year
  console.log('Testing Year sort...');
  await page.click('[data-sort="year"]');
  await page.waitForTimeout(500);
  let firstYearTitle = await page.$eval('.book-grid .book-card:first-child .book-title', el => el.innerText);
  let firstYearMeta = await page.$eval('.book-grid .book-card:first-child .book-meta', el => el.innerText);
  console.log('First year book:', firstYearTitle.replace(/\n/g, ' '), firstYearMeta);

  // Test sorting by title
  console.log('Testing Title sort...');
  await page.click('[data-sort="title"]');
  await page.waitForTimeout(500);
  let firstTitle = await page.$eval('.book-grid .book-card:first-child .book-title', el => el.innerText);
  console.log('First title:', firstTitle.replace(/\n/g, ' '));

  // Test sorting by author
  console.log('Testing Author sort...');
  await page.click('[data-sort="author"]');
  await page.waitForTimeout(500);
  let firstAuthor = await page.$eval('.book-grid .book-card:first-child .book-meta', el => el.innerText);
  console.log('First author:', firstAuthor);

  await browser.close();
})();
