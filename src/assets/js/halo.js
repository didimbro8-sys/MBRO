// Halo du portrait : dégradé vivant prune et or, qui suit doucement le pointeur. Aucune dépendance.
(function () {
  "use strict";
  var cv = document.getElementById("halo");
  if (!cv || !cv.getContext) return;
  var ctx = cv.getContext("2d");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var w = 0, h = 0, dpr = Math.min(window.devicePixelRatio || 1, 2), run = true, raf = 0;
  var px = 0.5, py = 0.5, tx = 0.5, ty = 0.5;
  var blobs = [
    { c: [231, 180, 30], r: 0.62, sx: 0.31, sy: 0.23, ph: 0.0, a: 0.95 },
    { c: [211, 120, 22], r: 0.55, sx: 0.19, sy: 0.27, ph: 2.1, a: 0.75 },
    { c: [155, 29, 127], r: 0.7, sx: 0.23, sy: 0.17, ph: 4.0, a: 0.9 },
    { c: [107, 10, 87], r: 0.8, sx: 0.13, sy: 0.21, ph: 1.2, a: 1 }
  ];
  function size() {
    var b = cv.getBoundingClientRect();
    w = Math.max(1, Math.round(b.width * dpr)); h = Math.max(1, Math.round(b.height * dpr));
    cv.width = w; cv.height = h;
  }
  function draw(t) {
    px += (tx - px) * 0.04; py += (ty - py) * 0.04;
    ctx.globalCompositeOperation = "source-over";
    ctx.fillStyle = "#46043a"; ctx.fillRect(0, 0, w, h);
    for (var i = blobs.length - 1; i >= 0; i--) {
      var b = blobs[i], k = t * 0.00022;
      var x = w * (0.5 + Math.sin(k * (1 + b.sx) + b.ph) * 0.32 + (px - 0.5) * (0.35 - i * 0.06));
      var y = h * (0.5 + Math.cos(k * (1 + b.sy) + b.ph * 1.3) * 0.32 + (py - 0.5) * (0.35 - i * 0.06));
      var r = Math.max(w, h) * b.r;
      var g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, "rgba(" + b.c.join(",") + "," + b.a + ")");
      g.addColorStop(1, "rgba(" + b.c.join(",") + ",0)");
      ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    }
  }
  function loop(t) { draw(t); if (run && !reduce) raf = requestAnimationFrame(loop); }
  size(); draw(4000);
  window.addEventListener("resize", function () { size(); draw(performance.now()); });
  window.addEventListener("pointermove", function (e) { tx = e.clientX / window.innerWidth; ty = e.clientY / window.innerHeight; }, { passive: true });
  if (reduce) return;
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (en) {
      run = en[0].isIntersecting;
      cancelAnimationFrame(raf);
      if (run) raf = requestAnimationFrame(loop);
    }).observe(cv);
  } else { raf = requestAnimationFrame(loop); }
  document.addEventListener("visibilitychange", function () {
    cancelAnimationFrame(raf);
    if (!document.hidden && run) raf = requestAnimationFrame(loop);
  });
})();
