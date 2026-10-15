// AM.Digital — « Le Signal » : un cosmos en 3D dessiné dans le héros.
// Une galaxie d'or tourne autour d'un noyau ; les anneaux d'orbite figurent les publics que la communication doit atteindre.
// Le pointeur (ou le doigt) incline la caméra, le défilement la fait plonger vers le contenu.
// Aucune bibliothèque, aucun appel réseau. Pause automatique hors écran ; image fixe si l'utilisateur préfère réduire les animations.
(function () {
  "use strict";
  var canvas = document.getElementById("cosmos");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d", { alpha: true });
  if (!ctx) return;

  var hero = canvas.closest(".hero") || canvas.parentNode;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var small = window.matchMedia("(max-width: 700px)").matches;
  var DPR = Math.min(window.devicePixelRatio || 1, small ? 1.5 : 1.75);

  var W = 0, H = 0, CX = 0, CY = 0, F = 0;
  var GOLD = [231, 195, 90], GOLD_DEEP = [199, 150, 19], ROSE = [240, 168, 214], WHITE = [255, 247, 251];

  // Sprites lumineux préparés une fois : beaucoup plus rapides qu'un dégradé par point
  function sprite(rgb, size) {
    var c = document.createElement("canvas");
    c.width = c.height = size;
    var g = c.getContext("2d");
    var r = size / 2;
    var grd = g.createRadialGradient(r, r, 0, r, r, r);
    grd.addColorStop(0, "rgba(" + rgb + ",1)");
    grd.addColorStop(0.25, "rgba(" + rgb + ",.55)");
    grd.addColorStop(1, "rgba(" + rgb + ",0)");
    g.fillStyle = grd;
    g.fillRect(0, 0, size, size);
    return c;
  }
  var SP = { gold: sprite(GOLD, 32), deep: sprite(GOLD_DEEP, 32), rose: sprite(ROSE, 32), white: sprite(WHITE, 32) };
  var CORE = sprite([231, 195, 90], 256);

  // Points de la scène : x, y, z, taille, sprite, scintillement
  var pts = [];
  var rnd = mulberry(20260415);
  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function gauss() { return (rnd() + rnd() + rnd() - 1.5) / 1.5; }

  var N_ARM = small ? 650 : 1500, N_FIELD = small ? 260 : 600;
  // Galaxie à deux bras spiraux, aplatie dans le plan x-z
  for (var i = 0; i < N_ARM; i++) {
    var arm = i % 2;
    var t = Math.pow(rnd(), 0.75);
    var radius = 0.12 + t * 1.25;
    var angle = arm * Math.PI + t * 4.4 + gauss() * 0.32;
    var spread = 0.07 + t * 0.11;
    pts.push({
      x: Math.cos(angle) * radius + gauss() * spread,
      y: gauss() * (0.05 + (1 - t) * 0.06),
      z: Math.sin(angle) * radius + gauss() * spread,
      s: 0.6 + rnd() * 1.6 * (1 - t * 0.5),
      sp: t < 0.25 ? SP.white : (rnd() < 0.82 ? SP.gold : SP.rose),
      tw: rnd() * 6.28
    });
  }
  // Champ d'étoiles lointaines, sur une coquille autour de la scène
  for (var j = 0; j < N_FIELD; j++) {
    var u = rnd() * 2 - 1, th = rnd() * 6.28, rr = 2.6 + rnd() * 2.4, q = Math.sqrt(1 - u * u);
    pts.push({ x: q * Math.cos(th) * rr, y: u * rr, z: q * Math.sin(th) * rr, s: 0.4 + rnd() * 0.9, sp: rnd() < 0.7 ? SP.white : SP.rose, tw: rnd() * 6.28, far: 1 });
  }
  // Anneaux d'orbite et leurs satellites
  var rings = [
    { r: 1.55, tilt: 0.42, speed: 0.22, sats: 3 },
    { r: 1.95, tilt: -0.28, speed: -0.15, sats: 2 },
    { r: 2.35, tilt: 0.12, speed: 0.1, sats: 4 }
  ];

  var yaw = 0.6, pitch = 0.42, tYaw = 0, tPitch = 0, pYaw = 0, pPitch = 0;
  var camZ = 3.6, scrollK = 0, time = 0, running = false, visible = true, last = 0;

  function resize() {
    var r = hero.getBoundingClientRect();
    W = Math.max(1, r.width); H = Math.max(1, r.height);
    canvas.width = Math.round(W * DPR); canvas.height = Math.round(H * DPR);
    canvas.style.width = W + "px"; canvas.style.height = H + "px";
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    // Le noyau se place à droite sur grand écran (le texte occupe la gauche), au centre-bas sur mobile
    CX = W > 900 ? W * 0.68 : W * 0.5;
    CY = W > 900 ? H * 0.5 : H * 0.62;
    F = Math.min(W, H) * (W > 900 ? 0.95 : 1.05);
  }

  function frame(now) {
    if (!running) return;
    var dt = Math.min(0.05, (now - (last || now)) / 1000); last = now;
    time += dt;
    draw();
    requestAnimationFrame(frame);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    // Caméra : rotation lente + inclinaison suivant le pointeur, amortie
    pYaw += (tYaw - pYaw) * 0.05; pPitch += (tPitch - pPitch) * 0.05;
    var ry = yaw + time * 0.06 + pYaw, rx = pitch + pPitch + scrollK * 0.5;
    var cy = Math.cos(ry), sy = Math.sin(ry), cx = Math.cos(rx), sx = Math.sin(rx);
    var cz = camZ - scrollK * 2.6;
    var fade = 1 - Math.min(1, scrollK * 1.15);

    // Noyau
    var coreSize = F * 0.62 * (1 + scrollK * 0.8);
    ctx.globalCompositeOperation = "lighter";
    ctx.globalAlpha = 0.55 * fade + 0.15;
    ctx.drawImage(CORE, CX - coreSize / 2, CY - coreSize / 2, coreSize, coreSize);

    // Anneaux (tracés en points pour rester dans le même langage visuel)
    for (var k = 0; k < rings.length; k++) {
      var R = rings[k], ct = Math.cos(R.tilt), st = Math.sin(R.tilt);
      ctx.globalAlpha = 0.28 * fade;
      ctx.fillStyle = "rgb(231,195,90)";
      for (var a = 0; a < 6.283; a += 0.035) {
        var x0 = Math.cos(a) * R.r, z0 = Math.sin(a) * R.r, y0 = z0 * st, z1 = z0 * ct;
        var p = project(x0, y0, z1, cy, sy, cx, sx, cz);
        if (p) ctx.fillRect(p.x, p.y, 1.1, 1.1);
      }
      for (var m = 0; m < R.sats; m++) {
        var aa = time * R.speed + m * (6.283 / R.sats) + k;
        var xs = Math.cos(aa) * R.r, zs = Math.sin(aa) * R.r;
        var ps = project(xs, zs * st, zs * ct, cy, sy, cx, sx, cz);
        if (ps) {
          var sz = 14 * ps.k;
          ctx.globalAlpha = 0.95 * fade;
          ctx.drawImage(SP.gold, ps.x - sz / 2, ps.y - sz / 2, sz, sz);
        }
      }
    }

    // Particules
    for (var i = 0; i < pts.length; i++) {
      var q = pts[i];
      var pr = project(q.x, q.y, q.z, cy, sy, cx, sx, cz);
      if (!pr) continue;
      var tw = 0.65 + 0.35 * Math.sin(time * 1.6 + q.tw);
      var size = q.s * pr.k * (q.far ? 5 : 7.5);
      if (size < 0.4) continue;
      ctx.globalAlpha = Math.min(1, tw * (q.far ? 0.7 : 0.95) * (q.far ? 1 : fade + 0.1));
      ctx.drawImage(q.sp, pr.x - size / 2, pr.y - size / 2, size, size);
    }
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = "source-over";
  }

  function project(x, y, z, cy, sy, cx, sx, cz) {
    var x1 = x * cy - z * sy, z1 = x * sy + z * cy;
    var y1 = y * cx - z1 * sx, z2 = y * sx + z1 * cx;
    var d = cz - z2;
    if (d < 0.15) return null;
    var k = 1 / d;
    return { x: CX + x1 * F * k, y: CY + y1 * F * k, k: k * 1.6 };
  }

  function start() { if (!running && visible && !reduce && !document.hidden) { running = true; last = 0; requestAnimationFrame(frame); } }
  function stop() { running = false; }

  resize();
  draw();
  hero.classList.add("cosmos-ready");
  if (reduce) { window.addEventListener("resize", function () { resize(); draw(); }); return; }

  // Pointeur : incline la caméra (souris et doigt)
  hero.addEventListener("pointermove", function (e) {
    var r = hero.getBoundingClientRect();
    tYaw = ((e.clientX - r.left) / r.width - 0.5) * 0.9;
    tPitch = ((e.clientY - r.top) / r.height - 0.5) * 0.5;
  }, { passive: true });
  hero.addEventListener("pointerleave", function () { tYaw = 0; tPitch = 0; });

  // Défilement : la caméra plonge à travers la galaxie
  window.addEventListener("scroll", function () {
    var h = hero.offsetHeight || 1;
    scrollK = Math.max(0, Math.min(1, window.scrollY / h));
  }, { passive: true });

  var rt;
  window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { resize(); if (!running) draw(); }, 120); });

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) start(); else stop(); }).observe(hero);
  }
  document.addEventListener("visibilitychange", function () { if (document.hidden) stop(); else start(); });
  start();
})();
