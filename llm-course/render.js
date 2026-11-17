// Render an HTML file to PDF with Chromium (A4 from CSS @page, backgrounds, document outline from headings).
const { chromium } = require('playwright');
(async () => {
  const [, , htmlPath, pdfPath] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + htmlPath, { waitUntil: 'load', timeout: 300000 });
  await page.evaluate(async () => { await document.fonts.ready; });
  // The book was laid out with Chromium shrinking every page to 76.5 % (a wide formula in ch. 34 made it "shrink to fit").
  // Fixing the scale keeps that layout on every machine instead of depending on how wide the widest element renders.
  await page.pdf({ path: pdfPath, preferCSSPageSize: true, printBackground: true, outline: true, tagged: true, scale: 0.765, timeout: 600000 });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
