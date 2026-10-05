// Confirmed by Viljami on 2026-10-06: noon, not midnight, in Helsinki.
// Helsinki uses EEST (UTC+3) on this date. This instant is timezone-independent.
window.PORSURFFI_REVEAL_AT = Date.parse('2026-10-06T12:00:00+03:00');

(function () {
  var timer;
  var revealing = false;

  function checkReveal() {
    clearTimeout(timer);
    if (revealing) return;
    var remaining = window.PORSURFFI_REVEAL_AT - Date.now();
    if (remaining <= 0) {
      revealing = true;
      // Avoid flashing the countdown for visitors arriving after the deadline.
      document.documentElement.style.visibility = 'hidden';
      window.location.replace(new URL('reveal.html', window.location.href).href);
      return;
    }
    // Independent of the typewriter loop; recheck the clock at least each second.
    timer = setTimeout(checkReveal, Math.min(remaining, 1000));
  }

  window.porsurffiCheckReveal = checkReveal;
  document.addEventListener('visibilitychange', checkReveal);
  window.addEventListener('pageshow', checkReveal);
  checkReveal();
})();
