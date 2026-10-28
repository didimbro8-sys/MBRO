// AM.Digital · animations et interactions du portfolio (toutes les pages)
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s) { return document.querySelector(s); };

  // Découpe des grands titres en lettres pour l'animation d'ouverture
  document.querySelectorAll('[data-split]').forEach(function (el) {
    var t = el.textContent; el.textContent = '';
    t.split('').forEach(function (c) {
      var s = document.createElement('span'); s.className = 'ch'; s.textContent = c; el.appendChild(s);
    });
  });

  // Barre de navigation : fond dès qu'on défile
  var nav = $('#nav');
  if (nav) {
    var navBg = function () { nav.classList.toggle('solid', window.scrollY > 40); };
    window.addEventListener('scroll', navBg, { passive: true }); navBg();
  }

  // Pixels or qui s'échappent vers le haut à droite, comme dans le logo
  var cv = $('#pixels');
  if (cv && cv.getContext) {
    var cx = cv.getContext('2d'), W = 0, H = 0, parts = [], mx = 0, my = 0, visible = true;
    var size = function () {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    var spawn = function (p) {
      p = p || {};
      p.s = [10, 18, 18, 34][Math.floor(Math.random() * 4)];
      p.x = W * (0.6 + Math.random() * 0.15); p.y = H * (0.28 + Math.random() * 0.18);
      p.vx = 0.2 + Math.random() * 0.45; p.vy = -(0.3 + Math.random() * 0.5);
      p.life = 0; p.max = 220 + Math.random() * 220; p.c = Math.random() < 0.75 ? '#f1bc18' : '#c79613';
      return p;
    };
    var draw = function (still) {
      cx.clearRect(0, 0, W, H);
      parts.forEach(function (p) {
        if (!still) { p.x += p.vx; p.y += p.vy; p.life++; if (p.life > p.max || p.y < -50 || p.x > W + 50) spawn(p); }
        var k = p.life / p.max, a = still ? 1 : Math.min(1, k * 6) * (1 - k), d = p.s / 18;
        cx.globalAlpha = a; cx.fillStyle = p.c;
        cx.fillRect(p.x + mx * 24 * d, p.y + my * 24 * d, p.s, p.s);
      });
      cx.globalAlpha = 1;
    };
    size(); window.addEventListener('resize', size);
    for (var i = 0; i < 14; i++) { var p = spawn(); p.life = Math.random() * p.max; p.x += p.vx * p.life; p.y += p.vy * p.life; parts.push(p); }
    window.addEventListener('pointermove', function (e) { mx = e.clientX / window.innerWidth - 0.5; my = e.clientY / window.innerHeight - 0.5; });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(cv);
    if (reduce) { parts = parts.slice(0, 7); draw(true); }
    else (function loop() { if (visible) draw(false); requestAnimationFrame(loop); })();
  }

  // Galerie défilante : boutons précédent / suivant
  var gal = $('#gal');
  if (gal) {
    var step = function (dir) { gal.scrollBy({ left: dir * gal.clientWidth * 0.8, behavior: reduce ? 'auto' : 'smooth' }); };
    var prev = $('#gal-prev'), next = $('#gal-next');
    if (prev) prev.addEventListener('click', function () { step(-1); });
    if (next) next.addEventListener('click', function () { step(1); });
  }

  // Agrandissement des visuels (toutes les galeries)
  var lb = $('#lightbox'), lbImg = $('#lightbox-img');
  if (lb && lbImg) {
    document.querySelectorAll('button[data-full]').forEach(function (t) {
      t.addEventListener('click', function () {
        var im = t.querySelector('img'); lbImg.src = t.dataset.full; lbImg.alt = im ? im.alt : '';
        if (lb.showModal) lb.showModal();
      });
    });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
  }

  // Réels : lecture muette au survol, lecture avec le son au clic
  var vbox = $('#vbox'), vboxVideo = $('#vbox-video');
  // Safari (et tous les navigateurs sur iPhone ou iPad) exige une lecture « par morceaux » que l'hébergement
  // ne propose pas : la vidéo resterait noire. Sur ces appareils, le réel ouvre la page des réels Instagram.
  var ua = navigator.userAgent, webkitOnly = /iP(hone|ad|od)/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1) || (/Safari/.test(ua) && !/Chrome|Chromium|CriOS|FxiOS|Edg|OPR|Android/.test(ua));
  if (webkitOnly) {
    document.querySelectorAll('button.reel[data-video]').forEach(function (r) {
      var a = document.createElement('a');
      a.className = r.className; a.href = 'https://www.instagram.com/amdigital204/reels/'; a.target = '_blank'; a.rel = 'noopener';
      a.setAttribute('aria-label', (r.getAttribute('aria-label') || 'Réel') + ', sur Instagram');
      var v = r.querySelector('video'), img = document.createElement('img');
      img.src = v.getAttribute('poster'); img.alt = ''; img.width = 1080; img.height = 1920; img.loading = 'lazy';
      v.replaceWith(img);
      while (r.firstChild) a.appendChild(r.firstChild);
      var small = a.querySelector('.reel-cap small'); if (small) small.textContent += ' · sur Instagram';
      r.replaceWith(a);
    });
  }
  document.querySelectorAll('button.reel[data-video]').forEach(function (r) {
    var v = r.querySelector('video');
    if (!reduce && window.matchMedia('(hover: hover)').matches) {
      r.addEventListener('pointerenter', function () { var p = v.play(); if (p && p.catch) p.catch(function () {}); r.classList.add('playing'); });
      r.addEventListener('pointerleave', function () { v.pause(); r.classList.remove('playing'); });
    }
    r.addEventListener('click', function () {
      if (!vbox || !vbox.showModal) { window.location.href = r.dataset.video; return; }
      v.pause(); vboxVideo.src = r.dataset.video; vboxVideo.poster = v.poster; vbox.showModal();
      var p = vboxVideo.play(); if (p && p.catch) p.catch(function () {});
    });
  });
  if (vbox) {
    vbox.addEventListener('close', function () { vboxVideo.pause(); vboxVideo.removeAttribute('src'); vboxVideo.load(); });
    vbox.addEventListener('click', function (e) { if (e.target === vbox) vbox.close(); });
  }

  // Copier l'adresse e-mail
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var el = document.getElementById(b.dataset.copy), label = b.textContent;
      var done = function () { b.textContent = 'Copié'; setTimeout(function () { b.textContent = label; }, 1600); };
      var select = function () { var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = 'Sélectionné'; };
      if (navigator.clipboard) navigator.clipboard.writeText(el.textContent).then(done, select); else select();
    });
  });

  // Formulaire de contact (Web3Forms)
  var form = $('#contact-form'), status = $('#form-status');
  if (form && status) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      status.className = 'form-status';
      if (!form.checkValidity()) { status.textContent = 'Merci de remplir votre nom, un e-mail valide, un message d\'au moins 20 caractères et de cocher la case.'; status.classList.add('err'); return; }
      if (form.botcheck.checked) return;
      if (form.access_key.value === 'VOTRE_CLE_WEB3FORMS') { status.textContent = 'Le formulaire n\'est pas encore activé. Écrivez-moi sur WhatsApp au +225 01 71 95 45 23.'; status.classList.add('err'); return; }
      var btn = form.querySelector('button[type=submit]'); btn.disabled = true; status.textContent = 'Envoi en cours…';
      fetch(form.action, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d.success) { form.reset(); status.textContent = 'Message envoyé. Je vous réponds sous 24 heures ouvrées.'; status.classList.add('ok'); window.location.href = '/merci/'; }
          else throw new Error();
        })
        .catch(function () { status.textContent = 'L\'envoi n\'a pas abouti. Écrivez-moi sur WhatsApp au +225 01 71 95 45 23.'; status.classList.add('err'); })
        .then(function () { btn.disabled = false; });
    });
  }

  // Liens internes : défilement doux
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var t = document.querySelector(a.getAttribute('href')); if (!t) return;
      e.preventDefault(); t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  // Animations GSAP (seulement si le visiteur n'a pas réduit les animations)
  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  var mm = gsap.matchMedia();
  var has = function (s) { return !!document.querySelector(s); };

  mm.add({ ok: '(prefers-reduced-motion: no-preference)', wide: '(min-width: 900px)', fine: '(hover: hover) and (pointer: fine)' }, function (ctx) {
    var c = ctx.conditions;
    if (!c.ok) return;

    // Ouverture de l'accueil
    if (has('#swoosh')) {
      var sw = $('#swoosh'), L = sw.getTotalLength();
      gsap.set(sw, { strokeDasharray: L, strokeDashoffset: L });
      gsap.timeline({ defaults: { ease: 'expo.out' } })
        .from('.nav', { y: -40, opacity: 0, duration: 1 })
        .from('.orb-wrap', { scale: 0.3, opacity: 0, filter: 'blur(30px)', duration: 2.2, ease: 'expo.out' }, '<')
        .from('h1 .ch', { yPercent: 115, rotate: 8, duration: 1.2, stagger: 0.03 }, '<.2')
        .from('.ast-panel', { y: 40, opacity: 0, duration: 1.2 }, '<.4')
        .from('.status', { y: 20, opacity: 0, duration: 0.8 }, '<.1')
        .from('.role', { y: 30, opacity: 0, duration: 0.9 }, '-=1.2')
        .to(sw, { strokeDashoffset: 0, duration: 1.1, ease: 'power2.inOut' }, '-=.6')
        .from('.intro, .ctas', { y: 24, opacity: 0, duration: 0.9, stagger: 0.1 }, '-=1');
      gsap.to('.hero-text', { yPercent: -14, opacity: 0.4, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
      gsap.to('.orb-wrap', { yPercent: 12, scale: 0.9, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
      gsap.utils.toArray('.reel, .designs li').forEach(function (el, i) {
        gsap.from(el, { y: 70, rotate: i % 2 ? 3 : -3, opacity: 0.15, duration: 1.1, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 92%' } });
      });
    }

    // Ouverture d'une étude de cas
    if (has('.case-hero')) {
      gsap.timeline({ defaults: { ease: 'expo.out' } })
        .from('.nav', { y: -40, opacity: 0, duration: 1 })
        .from('.case-hero h1 .ch', { yPercent: 115, duration: 1.1, stagger: 0.012 }, '<.1')
        .from('.case-hero .crumb, .case-hero .lead, .case-hero .tags', { y: 24, opacity: 0, duration: 0.9, stagger: 0.08 }, '-=.8')
        .from('.cover', { y: 90, rotateX: 18, opacity: 0, duration: 1.4, transformPerspective: 1200 }, '-=.9')
        .from('.fiche > div', { y: 20, opacity: 0, duration: 0.7, stagger: 0.06 }, '-=.9');
      if (has('.cover:not(.portrait-mode)')) gsap.to('.cover:not(.portrait-mode) img', { yPercent: -8, scale: 1.08, ease: 'none', scrollTrigger: { trigger: '.cover', start: 'top bottom', end: 'bottom top', scrub: true } });
      gsap.utils.toArray('.dispositif li').forEach(function (li) {
        gsap.from(li, { x: -40, opacity: 0.15, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: li, start: 'top 88%' } });
      });
      gsap.utils.toArray('.mosaic .shot-btn').forEach(function (b, i) {
        gsap.from(b, { y: 60, rotate: i % 2 ? 2 : -2, opacity: 0.2, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: b, start: 'top 92%' } });
      });
    }

    // Ouverture d'une page Veille ou Journal
    if (has('.page-hero')) {
      var ph = gsap.timeline({ defaults: { ease: 'expo.out' } }).from('.nav', { y: -40, opacity: 0, duration: 1 });
      if (has('.page-hero h1 .ch')) ph.from('.page-hero h1 .ch', { yPercent: 115, duration: 1.1, stagger: 0.01 }, '<.1');
      if (has('.big404')) ph.from('.big404', { scale: 0.6, opacity: 0, duration: 1.4 }, '<');
      ph
        .from('.page-hero .crumb, .page-hero .meta-line, .page-hero .lead', { y: 24, opacity: 0, duration: 0.9, stagger: 0.08 }, '-=.8');
      gsap.utils.toArray('.signal, .ed, .notes li').forEach(function (el) {
        gsap.from(el, { y: 50, opacity: 0.15, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 90%' } });
      });
      if (has('.analyse')) gsap.from('.analyse', { scale: 0.96, opacity: 0.3, duration: 1.1, ease: 'expo.out', scrollTrigger: { trigger: '.analyse', start: 'top 85%' } });
    }

    // Titres de sections
    gsap.utils.toArray('.rv').forEach(function (el) {
      gsap.from(el, { y: 70, opacity: 0.2, duration: 1.1, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 88%' } });
    });

    // Compteurs
    gsap.utils.toArray('[data-count]').forEach(function (el) {
      var end = +el.dataset.count, suf = el.dataset.suffix || '', o = { v: 0 };
      ScrollTrigger.create({ trigger: el, start: 'top 90%', once: true, onEnter: function () {
        gsap.to(o, { v: end, duration: 2.2, ease: 'power3.out', onUpdate: function () { el.textContent = Math.round(o.v).toLocaleString('fr-FR') + suf; } });
      } });
    });

    // Ligne de la méthode
    if (has('#rail')) {
      gsap.fromTo('#rail', { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, ease: 'none', scrollTrigger: { trigger: '#steps', start: 'top 70%', end: 'bottom 60%', scrub: 0.6 } });
      gsap.utils.toArray('.steps .n').forEach(function (n) {
        gsap.from(n, { scale: 0.4, duration: 0.7, ease: 'back.out(2.4)', scrollTrigger: { trigger: n, start: 'top 80%' } });
      });
    }

    // Parcours : la chronologie apparaît
    if (has('.timeline')) gsap.from('.timeline li', { x: -30, opacity: 0.2, stagger: 0.12, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: '.timeline', start: 'top 80%' } });

    // Réalisations à l'horizontale sur grand écran
    if (c.wide && has('#htrack')) {
      var tr = $('#htrack');
      tr.parentNode.classList.add('pinned');
      var dist = function () { return Math.max(0, tr.scrollWidth - document.documentElement.clientWidth + 48); };
      gsap.to(tr, { x: function () { return -dist(); }, ease: 'none', scrollTrigger: { trigger: '#realisations', start: 'top top', end: function () { return '+=' + dist(); }, pin: true, scrub: 1, invalidateOnRefresh: true } });
      gsap.utils.toArray('.card').forEach(function (card, i) {
        gsap.from(card, { rotate: i % 2 ? 4 : -4, y: 40, scrollTrigger: { trigger: '#realisations', start: 'top 80%', end: 'top top', scrub: 1 } });
      });
    }

    // Boutons aimantés et curseur pixel (souris uniquement)
    if (c.fine) {
      document.querySelectorAll('.mag').forEach(function (b) {
        var qx = gsap.quickTo(b, 'x', { duration: 0.4, ease: 'power3' }), qy = gsap.quickTo(b, 'y', { duration: 0.4, ease: 'power3' });
        b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); qx((e.clientX - r.left - r.width / 2) * 0.3); qy((e.clientY - r.top - r.height / 2) * 0.3); });
        b.addEventListener('pointerleave', function () { qx(0); qy(0); });
      });
      var cur = $('#cursor');
      if (cur) {
        var cxq = gsap.quickTo(cur, 'x', { duration: 0.25, ease: 'power3' }), cyq = gsap.quickTo(cur, 'y', { duration: 0.25, ease: 'power3' });
        window.addEventListener('pointermove', function (e) { cxq(e.clientX); cyq(e.clientY); });
        document.querySelectorAll('a, button').forEach(function (a) {
          a.addEventListener('pointerenter', function () { gsap.to(cur, { scale: 3.2, rotate: 45, duration: 0.3 }); });
          a.addEventListener('pointerleave', function () { gsap.to(cur, { scale: 1, rotate: 0, duration: 0.3 }); });
        });
      }
    }

    // Quand l'écran change de taille, on rend le défilement normal aux projets
    return function () { var h = $('.hscroll'); if (h) h.classList.remove('pinned'); };
  });

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
