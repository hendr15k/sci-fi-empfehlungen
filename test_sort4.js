const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);

  await page.click('[data-sort="rating"]');
  await page.waitForTimeout(500);

  let data = await page.$$eval('.book-grid .book-card', els => els.map(e => ({
      title: e.querySelector('.book-title').innerText.split('\n')[e.querySelector('.book-title').innerText.split('\n').length - 1].trim().split('🏆')[0].split('📚')[0].split('🇩🇪')[0].trim(),
      rating: e.querySelector('.rating').innerText
  })));

  console.log('Total books sorted:', data.length);

  // Also get the raw books array to compare rating values
  const rawBooks = await page.evaluate(() => books);
  let ratingDiscrepancies = [];
  for (let i = 0; i < data.length - 1; i++) {
     let b1 = rawBooks.find(b => b.title === data[i].title);
     let b2 = rawBooks.find(b => b.title === data[i+1].title);

     if (b1 && b2 && b1.rating < b2.rating) {
         ratingDiscrepancies.push({
             pos: i,
             b1: {title: b1.title, rating: b1.rating, stars: b1.stars},
             b2: {title: b2.title, rating: b2.rating, stars: b2.stars}
         });
     }
  }

  console.log('Rating Discrepancies:', ratingDiscrepancies.length);
  if (ratingDiscrepancies.length > 0) {
      console.log(ratingDiscrepancies[0]);
  }

  await browser.close();
})();
