// AM.Digital · assistant vocal d'accueil
// Une sphère de pixels or qui respire et pulse au rythme de la voix, avec sous-titres synchronisés.
// La voix utilise la synthèse vocale du navigateur (aucun service externe, aucune donnée envoyée).
(function () {
  'use strict';
  var root = document.getElementById('assistant');
  if (!root) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cv = document.getElementById('orb'), subs = document.getElementById('subs');
  var btn = document.getElementById('ast-play'), stopBtn = document.getElementById('ast-stop');
  var stateEl = document.getElementById('ast-state');
  var bars = [].slice.call(root.querySelectorAll('.wave i'));

  // Salutation selon l'heure du visiteur
  var h = new Date().getHours();
  var greet = h >= 18 || h < 5 ? 'Bonsoir' : 'Bonjour';
  root.querySelectorAll('[data-greet]').forEach(function (el) { el.textContent = greet; });
  var lines = [].slice.call(document.querySelectorAll('#ast-script li')).map(function (li) {
    var show = li.textContent.replace(/\s+/g, ' ').trim();
    var say = (li.dataset.say || show).replace('{salut}', greet);
    return { show: show, say: say };
  });

  // ---------- état partagé avec la sphère ----------
  var energy = 0.12, target = 0.12, pulse = 0, speaking = false;
  var setState = function (t) { if (stateEl) stateEl.textContent = t; };
  var waves = [];
  var bump = function (k) { k = k || 0.6; pulse = Math.min(1, pulse + k); if (speaking && k >= 0.4 && waves.length < 6) waves.push({ r: 0.62, a: 0.7 }); };

  // ---------- sous-titres ----------
  var words = [];
  var showLine = function (text) {
    subs.textContent = '';
    words = text.split(' ').map(function (w, i) {
      var s = document.createElement('span'); s.textContent = w + ' '; subs.appendChild(s);
      if (!reduce) { s.style.opacity = '0'; s.style.transition = 'opacity .35s ease ' + (i * 0.03) + 's'; requestAnimationFrame(function () { s.style.opacity = ''; }); }
      return s;
    });
  };
  var highlight = function (ratio) {
    var n = Math.min(words.length - 1, Math.floor(ratio * words.length));
    words.forEach(function (w, i) { w.classList.toggle('on', i <= n); });
  };

  // ---------- voix ----------
  var synth = window.speechSynthesis, voice = null, idx = 0, demoTimer = null;
  var pickVoice = function () {
    if (!synth) return null;
    var vs = synth.getVoices().filter(function (v) { return /^fr/i.test(v.lang); });
    var by = function (re) { return vs.filter(function (v) { return re.test(v.name); })[0]; };
    return by(/Natural|Neural|Online/i) || vs.filter(function (v) { return /fr-FR/i.test(v.lang) && /Google/i.test(v.name); })[0] || vs.filter(function (v) { return /fr-FR/i.test(v.lang); })[0] || vs[0] || null;
  };
  if (synth) { voice = pickVoice(); if (synth.addEventListener) synth.addEventListener('voiceschanged', function () { voice = pickVoice(); }); }

  var finish = function (label) {
    speaking = false; target = 0.12; setState(label);
    btn.textContent = '↺ Réécouter l\'accueil'; btn.hidden = false; stopBtn.hidden = true;
    try { sessionStorage.setItem('am-assistant', 'vu'); } catch (e) {}
  };

  var speakLine = function () {
    if (idx >= lines.length) { finish('· à votre écoute'); return; }
    var L = lines[idx];
    var u = new SpeechSynthesisUtterance(L.say);
    u.lang = 'fr-FR'; if (voice) u.voice = voice; u.rate = 1; u.pitch = 1;
    var bounded = false;
    u.onstart = function () { speaking = true; target = 0.55; showLine(L.show); highlight(0); bump(0.8); setState('· vous parle'); };
    u.onboundary = function (e) { if (e.name && e.name !== 'word') return; bounded = true; highlight(e.charIndex / L.say.length); bump(0.45); };
    u.onend = function () { highlight(1); target = 0.3; idx++; setTimeout(speakLine, 280); };
    u.onerror = function (e) {
      if (e.error === 'not-allowed') { waitForGesture(); return; }
      if (e.error === 'interrupted' || e.error === 'canceled') return;
      demo();
    };
    synth.speak(u);
    // Si la voix ne donne pas le rythme mot à mot, on fait avancer les sous-titres au temps.
    var t0 = Date.now(), dur = L.say.length * 62;
    (function tick() { if (!speaking || bounded || idx >= lines.length || lines[idx] !== L) return; var r = (Date.now() - t0) / dur; highlight(Math.min(1, r)); if (Math.random() < 0.25) bump(0.3); setTimeout(tick, 120); })();
  };

  // Lecture sans voix (navigateur sans synthèse vocale en français) : sous-titres seuls
  var demo = function () {
    clearTimeout(demoTimer); speaking = true; target = 0.45; setState('· lecture du texte');
    btn.hidden = true; stopBtn.hidden = false;
    (function step() {
      if (idx >= lines.length) { finish('· à votre écoute'); return; }
      var L = lines[idx]; showLine(L.show); var k = 0;
      var iv = setInterval(function () { k++; highlight(k / words.length); bump(0.35); if (k >= words.length) clearInterval(iv); }, 260);
      idx++; demoTimer = setTimeout(step, Math.max(2600, words.length * 300));
    })();
  };

  var start = function () {
    clearTimeout(demoTimer); idx = 0;
    btn.hidden = true; stopBtn.hidden = false;
    if (!synth || !window.SpeechSynthesisUtterance) { demo(); return; }
    synth.cancel(); voice = voice || pickVoice();
    if (!voice && synth.getVoices().length) { demo(); return; }
    speakLine();
  };
  var stop = function () { clearTimeout(demoTimer); if (synth) synth.cancel(); idx = lines.length; finish('· en pause'); };

  // Les navigateurs exigent un premier geste avant de parler : le premier clic, toucher ou touche lance l'accueil.
  var waiting = false, offGesture = null;
  var waitForGesture = function () {
    if (waiting) return; waiting = true; speaking = false; target = 0.18;
    btn.hidden = false; stopBtn.hidden = true; btn.classList.add('call');
    setState('· touchez pour m\'écouter');
    var go = function (e) {
      if (e && e.target && e.target.closest && e.target.closest('a, #ast-stop, #ast-play')) return;
      off(); waiting = false; btn.classList.remove('call'); start();
    };
    var off = function () { ['pointerdown', 'keydown'].forEach(function (t) { document.removeEventListener(t, go, true); }); offGesture = null; };
    offGesture = off;
    ['pointerdown', 'keydown'].forEach(function (t) { document.addEventListener(t, go, true); });
  };

  btn.addEventListener('click', function () { if (offGesture) offGesture(); waiting = false; btn.classList.remove('call'); start(); });
  stopBtn.addEventListener('click', stop);

  // Accueil : première phrase affichée tout de suite, puis tentative de parler
  showLine(lines[0].show); highlight(-1);
  var seen = false; try { seen = sessionStorage.getItem('am-assistant') === 'vu'; } catch (e) {}
  if (seen) { setState('· en ligne'); btn.textContent = '▶ Écouter l\'accueil'; }
  else if (synth && window.SpeechSynthesisUtterance) {
    setTimeout(function () {
      if (navigator.userActivation && !navigator.userActivation.hasBeenActive) { waitForGesture(); return; }
      start();
      setTimeout(function () { if (!synth.speaking && !synth.pending && idx === 0) waitForGesture(); }, 1200);
    }, 900);
  } else { setTimeout(demo, 1200); }

  // ---------- la sphère ----------
  if (!cv || !cv.getContext) return;
  var cx = cv.getContext('2d'), W = 0, H = 0, dpr = 1, N = window.innerWidth < 700 ? 620 : 980, pts = [], mx = 0, my = 0, visible = true;
  for (var i = 0; i < N; i++) {
    var y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = i * 2.399963;
    pts.push([Math.cos(th) * r, y, Math.sin(th) * r, Math.random() * 6.283, Math.random() < 0.08]);
  }
  var size = function () { dpr = Math.min(window.devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0); };
  size(); window.addEventListener('resize', size);
  window.addEventListener('pointermove', function (e) { mx = e.clientX / window.innerWidth - 0.5; my = e.clientY / window.innerHeight - 0.5; });
  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(cv);

  var rays = []; for (var q = 0; q < 120; q++) rays.push([q / 120 * 6.2832 + Math.random() * 0.05, Math.random() * 6.283, 0.4 + Math.random() * 0.9]);
  var draw = function (t) {
    energy += (target - energy) * 0.06; pulse *= 0.9;
    var e = energy + pulse * 0.5, ts = t * 0.001;
    cx.clearRect(0, 0, W, H);
    var R = Math.min(W, H) * 0.33, ox = W / 2, oy = H / 2, core = R * (0.56 + e * 0.04);
    // halo violet profond
    var g = cx.createRadialGradient(ox, oy, core * 0.8, ox, oy, R * 1.9);
    g.addColorStop(0, 'rgba(102,0,74,' + (0.55 + e * 0.25) + ')');
    g.addColorStop(0.45, 'rgba(102,0,74,0.18)');
    g.addColorStop(1, 'rgba(48,0,36,0)');
    cx.fillStyle = g; cx.beginPath(); cx.arc(ox, oy, R * 1.9, 0, 6.2832); cx.fill();
    // couronne d'or et rayons qui vibrent avec la voix
    cx.globalCompositeOperation = 'lighter';
    var c = cx.createRadialGradient(ox, oy, core * 0.92, ox, oy, core * (1.7 + e * 0.9));
    c.addColorStop(0, 'rgba(241,188,24,0.95)');
    c.addColorStop(0.08, 'rgba(241,188,24,' + (0.55 + e * 0.3) + ')');
    c.addColorStop(0.4, 'rgba(199,150,19,' + (0.16 + e * 0.2) + ')');
    c.addColorStop(1, 'rgba(199,150,19,0)');
    cx.fillStyle = c; cx.beginPath(); cx.arc(ox, oy, core * (1.7 + e * 0.9), 0, 6.2832); cx.fill();
    cx.lineCap = 'round';
    for (var q2 = 0; q2 < rays.length; q2++) {
      var ra = rays[q2], ang = ra[0] + ts * 0.05;
      var len = core * (0.25 + ra[2] * (0.35 + e * 1.1) * (0.6 + 0.4 * Math.sin(ts * (2 + e * 6) + ra[1])));
      cx.strokeStyle = 'rgba(241,188,24,' + (0.10 + e * 0.22) + ')'; cx.lineWidth = 1 + ra[2];
      cx.beginPath(); cx.moveTo(ox + Math.cos(ang) * core, oy + Math.sin(ang) * core); cx.lineTo(ox + Math.cos(ang) * (core + len), oy + Math.sin(ang) * (core + len)); cx.stroke();
    }
    // ondes de choc à chaque mot
    for (var wv = waves.length - 1; wv >= 0; wv--) {
      var W8 = waves[wv]; W8.r += 0.018; W8.a *= 0.955;
      cx.strokeStyle = 'rgba(241,188,24,' + W8.a.toFixed(3) + ')'; cx.lineWidth = 2;
      cx.beginPath(); cx.arc(ox, oy, R * W8.r, 0, 6.2832); cx.stroke();
      if (W8.a < 0.02) waves.splice(wv, 1);
    }
    cx.globalCompositeOperation = 'source-over';
    // éclipse : le cœur sombre bordé de lumière
    var k2 = cx.createRadialGradient(ox - core * 0.25, oy - core * 0.3, core * 0.1, ox, oy, core);
    k2.addColorStop(0, '#3c0030'); k2.addColorStop(1, '#300024');
    cx.fillStyle = k2; cx.beginPath(); cx.arc(ox, oy, core, 0, 6.2832); cx.fill();
    cx.strokeStyle = 'rgba(241,188,24,' + (0.75 + e * 0.25) + ')'; cx.lineWidth = 1.5 + e * 2;
    cx.beginPath(); cx.arc(ox, oy, core, 0, 6.2832); cx.stroke();
    // anneaux en orbite
    cx.save(); cx.translate(ox, oy);
    for (var k = 0; k < 2; k++) {
      cx.save(); cx.rotate((k ? -0.5 : 0.35) + t * (k ? -0.00012 : 0.00009) + mx * 0.3);
      cx.strokeStyle = 'rgba(241,188,24,' + (0.18 + e * 0.25) + ')'; cx.lineWidth = 1;
      cx.beginPath(); cx.ellipse(0, 0, R * (1.55 + k * 0.22), R * (0.42 + k * 0.1), 0, 0, 6.2832); cx.stroke();
      var a = t * (k ? 0.0011 : -0.0008);
      cx.fillStyle = '#f1bc18'; cx.fillRect(Math.cos(a) * R * (1.55 + k * 0.22) - 3, Math.sin(a) * R * (0.42 + k * 0.1) - 3, 6, 6);
      cx.restore();
    }
    cx.restore();
    // particules
    var ry = t * 0.00022 + mx * 0.9, rx = 0.35 + my * 0.6, cy = Math.cos(ry), sy = Math.sin(ry), cX = Math.cos(rx), sX = Math.sin(rx);
    cx.globalCompositeOperation = 'lighter';
    for (var j = 0; j < pts.length; j++) {
      var p = pts[j], x = p[0], y2 = p[1], z = p[2];
      var n = Math.sin(3 * x + ts * 1.3) + Math.sin(4 * y2 - ts * 1.1) + Math.sin(5 * z + ts * 0.8 + p[3]);
      var d = 1 + n * (0.05 + e * 0.12) + (p[4] ? e * 0.55 * (0.5 + 0.5 * Math.sin(ts * 9 + p[3])) : 0);
      x *= d; y2 *= d; z *= d;
      var x1 = x * cy + z * sy, z1 = -x * sy + z * cy;
      var y1 = y2 * cX - z1 * sX, z2 = y2 * sX + z1 * cX;
      var f = 3 / (3 - z2), px = ox + x1 * R * f, py = oy + y1 * R * f;
      var depth = (z2 + 1.4) / 2.8;
      // les points cachés derrière l'éclipse ne sont pas dessinés
      if (z2 < 0 && (px - ox) * (px - ox) + (py - oy) * (py - oy) < core * core) continue;
      var s = (p[4] ? 3 : 1.6) + depth * 2.8 + e * 1.4;
      cx.fillStyle = depth > 0.42 ? 'rgba(241,188,24,' + Math.min(1, 0.4 + depth * 0.75) + ')' : 'rgba(217,195,210,' + (0.25 + depth * 0.6) + ')';
      cx.fillRect(px - s / 2, py - s / 2, s, s);
    }
    cx.globalCompositeOperation = 'source-over';
    // onde sonore sous la sphère
    for (var b = 0; b < bars.length; b++) {
      var v = speaking ? 0.25 + Math.abs(Math.sin(ts * 7 + b * 0.9)) * (0.4 + pulse * 0.6) : 0.12 + Math.abs(Math.sin(ts * 1.5 + b * 0.6)) * 0.12;
      bars[b].style.transform = 'scaleY(' + v.toFixed(3) + ')';
    }
  };
  // Sans animation : une image fixe de la sphère, redessinée si la fenêtre change de taille
  if (reduce) { draw(0); window.addEventListener('resize', function () { draw(0); }); setTimeout(function () { draw(0); }, 600); return; }
  (function loop(t) { if (visible) draw(t || 0); requestAnimationFrame(loop); })();
})();
