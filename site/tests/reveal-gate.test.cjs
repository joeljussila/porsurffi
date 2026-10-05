const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');

const script = readFileSync(require('node:path').join(__dirname, '../reveal-gate.js'), 'utf8');
const deadline = Date.parse('2026-10-06T09:00:00Z');

function browser(now, href = 'https://porsurf.com/') {
  let clock = now;
  let nextTimer;
  const redirects = [];
  const documentEvents = {};
  const windowEvents = {};
  const window = {
    location: { href, replace: url => redirects.push(url) },
    addEventListener: (event, fn) => { windowEvents[event] = fn; },
  };
  const document = {
    documentElement: { style: {} },
    addEventListener: (event, fn) => { documentEvents[event] = fn; },
  };
  vm.runInNewContext(script, {
    window, document, URL,
    Date: { parse: Date.parse, now: () => clock },
    setTimeout: (fn, delay) => { nextTimer = { fn, delay }; return 1; },
    clearTimeout: () => { nextTimer = undefined; },
  });
  return {
    window, document, redirects, documentEvents, windowEvents,
    setClock: value => { clock = value; },
    timer: () => nextTimer,
  };
}

test('deadline is October 6 at noon Helsinki, not noon in the visitor timezone', () => {
  for (const timezone of ['Europe/Helsinki', 'UTC', 'America/Los_Angeles', 'Asia/Tokyo']) {
    const previous = process.env.TZ;
    process.env.TZ = timezone;
    try {
      const page = browser(deadline - 1000);
      assert.equal(page.window.PORSURFFI_REVEAL_AT, deadline);
      assert.deepEqual(page.redirects, []);
    } finally {
      if (previous === undefined) delete process.env.TZ;
      else process.env.TZ = previous;
    }
  }
});

test('does not reveal one millisecond early, then switches at the exact boundary', () => {
  const page = browser(deadline - 1);
  assert.deepEqual(page.redirects, []);
  assert.equal(page.timer().delay, 1);
  const tick = page.timer().fn;
  page.setClock(deadline);
  tick();
  assert.deepEqual(page.redirects, ['https://porsurf.com/reveal.html']);
  assert.equal(page.document.documentElement.style.visibility, 'hidden');
  assert.equal(page.timer(), undefined);
});

test('late arrivals go directly to the reveal and cannot start duplicate redirects', () => {
  const page = browser(deadline + 86400000);
  page.window.porsurffiCheckReveal();
  page.windowEvents.pageshow();
  assert.deepEqual(page.redirects, ['https://porsurf.com/reveal.html']);
});

test('suspended tab rechecks the clock when it becomes visible', () => {
  const page = browser(deadline - 60000);
  assert.equal(page.timer().delay, 1000);
  page.setClock(deadline + 60000);
  page.documentEvents.visibilitychange();
  assert.equal(page.redirects.length, 1);
});

test('restored page rechecks the deadline', () => {
  const page = browser(deadline - 60000);
  page.setClock(deadline);
  page.windowEvents.pageshow();
  assert.equal(page.redirects.length, 1);
});

test('nested static hosting and preview query strings resolve the correct reveal URL', () => {
  const page = browser(deadline, 'https://example.com/site/index.html?preview=1#test');
  assert.deepEqual(page.redirects, ['https://example.com/site/reveal.html']);
});

test('deadline remains clock-based if the device clock changes before launch', () => {
  const page = browser(deadline - 500);
  const tick = page.timer().fn;
  page.setClock(deadline - 3600000);
  tick();
  assert.deepEqual(page.redirects, []);
  assert.equal(page.timer().delay, 1000);
});
