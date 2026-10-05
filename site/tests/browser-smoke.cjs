// Optional real-browser smoke test: requires Playwright, not a site build dependency.
// NODE_PATH=<playwright package directory> node site/tests/browser-smoke.cjs
const { chromium } = require('playwright');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || undefined,
    headless: true,
  });
  const base = process.env.SITE_URL || 'http://localhost:8765/';
  const deadline = Date.parse('2026-10-06T09:00:00Z');
  try {
    for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
      for (const reducedMotion of ['no-preference', 'reduce']) {
        const context = await browser.newContext({ viewport, reducedMotion, timezoneId: 'America/Los_Angeles' });
        const page = await context.newPage();
        const errors = [];
        page.on('pageerror', error => errors.push(error.message));
        await page.route('**/fonts.googleapis.com/**', route => route.abort());
        await page.route('**/fonts.gstatic.com/**', route => route.abort());
        await page.route('**/_vercel/insights/**', route => route.fulfill({ body: '' }));
        await page.clock.install({ time: deadline - 60000 });
        await page.goto(base);
        assert.equal(new URL(page.url()).pathname, new URL(base).pathname);
        await page.clock.runFor(12000);
        assert.match(await page.locator('#tw').textContent(), /^0d 00h 00m \d{2}s$/);
        assert.equal(await page.locator('.bg-video').count(), 1);
        if (reducedMotion === 'reduce') {
          assert.equal(await page.locator('.bg-video').isVisible(), false);
        } else {
          await page.waitForFunction(() => !document.querySelector('video').paused);
          assert.equal(await page.locator('.bg-video').evaluate(el => el.classList.contains('is-playing')), true);
        }
        await page.screenshot({ path: `/tmp/porsurf-countdown-${viewport.width}-${reducedMotion}.png` });
        const navigation = page.waitForURL('**/reveal*');
        await page.clock.setSystemTime(deadline);
        await page.clock.runFor(1100);
        await navigation;
        await page.waitForFunction(() => [...document.querySelectorAll('.pics img')].every(img => img.complete && img.naturalWidth > 0));
        assert.equal(await page.locator('.pics img').count(), 5);
        assert.equal(await page.title(), 'PorSurffi 2027 - El Salvador');
        assert.equal(await page.locator('h1').getAttribute('aria-label'), 'PorSurffi 2027. El Salvador.');
        await page.clock.runFor(8000);
        const currentPhoto = await page.locator('.pics img').evaluateAll(images =>
          images.reduce((best, img, index) => Number(img.style.zIndex) > best.z ? { index, z: Number(img.style.zIndex) } : best, { index: -1, z: 0 }).index);
        assert.equal(currentPhoto, reducedMotion === 'reduce' ? 0 : 1);
        if (reducedMotion === 'reduce') assert.equal(await page.locator('#tw').textContent(), 'PorSurffi 2027 - El Salvador');
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
        assert.deepEqual(errors, []);
        await page.screenshot({ path: `/tmp/porsurf-reveal-${viewport.width}-${reducedMotion}.png` });
        await page.close();

        const late = await context.newPage();
        await late.clock.install({ time: deadline + 60000 });
        await late.goto(base);
        await late.waitForURL('**/reveal*');
        assert.equal(await late.title(), 'PorSurffi 2027 - El Salvador');
        console.log(`PASS ${viewport.width}px / ${reducedMotion}: countdown, noon switch, reveal, late arrival`);
        await context.close();
      }
    }

    const context = await browser.newContext();
    const page = await context.newPage();
    await page.clock.install({ time: deadline - 60000 });
    await page.addInitScript(() => { HTMLMediaElement.prototype.play = () => Promise.reject(new Error('Autoplay blocked')); });
    await page.goto(base);
    assert.equal(await page.locator('.bg-video').evaluate(el => el.classList.contains('is-playing')), false);
    assert.match(await page.locator('.stage').evaluate(el => getComputedStyle(el).backgroundImage), /poster\.jpg/);
    assert.equal(await page.locator('video').evaluate(el => el.paused), true);
    console.log('PASS blocked autoplay: static poster remains visible');
    await context.close();
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
