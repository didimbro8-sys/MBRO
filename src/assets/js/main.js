// AM.Digital — scripts du portfolio. Aucun script tiers, aucune donnée stockée.
(function () {
  "use strict";

  // Menu mobile
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.setAttribute("data-open", String(!open));
      document.body.classList.toggle("menu-open", !open);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") { toggle.click(); toggle.focus(); }
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        toggle.setAttribute("aria-expanded", "false");
        nav.setAttribute("data-open", "false");
        document.body.classList.remove("menu-open");
      }
    });
  }

  // Année courante
  var y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());

  // E-mail assemblé au chargement : les robots qui lisent le HTML brut ne le voient pas
  var slot = document.getElementById("email-slot");
  if (slot && slot.dataset.u && slot.dataset.d) {
    var addr = slot.dataset.u + "@" + slot.dataset.d;
    slot.textContent = "";
    var a = document.createElement("a");
    a.href = "mailto:" + addr;
    a.textContent = addr;
    slot.appendChild(a);
    var btn = document.createElement("button");
    btn.type = "button"; btn.className = "copy"; btn.textContent = "Copier";
    btn.addEventListener("click", function () {
      var done = function () { btn.textContent = "Copié"; setTimeout(function () { btn.textContent = "Copier"; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(addr).then(done, function () { selectText(a); });
      } else { selectText(a); }
    });
    slot.appendChild(btn);
  }
  function selectText(el) {
    var r = document.createRange(); r.selectNodeContents(el);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }

  // Visionneuse : agrandir une création de la galerie
  var dlg = document.getElementById("visionneuse");
  if (dlg && typeof dlg.showModal === "function") {
    var vImg = document.getElementById("visionneuse-img");
    var vLeg = document.getElementById("visionneuse-legende");
    document.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest(".zoom") : null;
      if (b) {
        vImg.src = b.getAttribute("data-src");
        vImg.alt = b.getAttribute("data-legende") || "";
        vLeg.textContent = b.getAttribute("data-legende") || "";
        dlg.showModal();
      } else if (e.target === dlg) {
        dlg.close();
      }
    });
  }

  // Formulaire de contact
  var form = document.getElementById("contact-form");
  var status = document.getElementById("form-status");
  if (!form || !status) return;
  var lastSend = 0;
  var loadedAt = Date.now();

  function say(msg, state) { status.textContent = msg; status.setAttribute("data-state", state || ""); }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Piège à robots : un humain ne coche jamais cette case invisible
    if (form.botcheck && form.botcheck.checked) return;
    // Un robot remplit et envoie en moins de 3 secondes ; un humain, jamais
    if (Date.now() - loadedAt < 3000) { say("Prenez quelques secondes pour relire votre message, puis renvoyez-le.", "error"); return; }

    // Anti-rafale : un envoi toutes les 30 secondes
    if (Date.now() - lastSend < 30000) { say("Votre message vient d'être envoyé. Patientez quelques secondes avant d'en renvoyer un.", "error"); return; }

    if (!form.checkValidity()) {
      var bad = form.querySelector(":invalid");
      say("Vérifiez le champ « " + (bad && bad.labels && bad.labels[0] ? bad.labels[0].textContent.trim() : "requis") + " » : il est vide ou incomplet.", "error");
      if (bad) bad.focus();
      return;
    }

    var key = form.access_key ? form.access_key.value : "";
    if (!key || key.indexOf("VOTRE_CLE") === 0) {
      say("Le formulaire n'est pas encore activé. Écrivez-moi sur WhatsApp au +225 01 71 95 45 23.", "error");
      return;
    }

    var data = new FormData(form);
    data.delete("redirect");
    say("Envoi en cours…");
    fetch(form.action, { method: "POST", headers: { Accept: "application/json" }, body: data })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j.success, j: j }; }); })
      .then(function (res) {
        if (res.ok) { lastSend = Date.now(); form.reset(); say("Message envoyé. Je vous réponds sous 24 heures ouvrées.", "ok"); }
        else { say("L'envoi a échoué. Réessayez ou écrivez-moi sur WhatsApp.", "error"); }
      })
      .catch(function () { say("Connexion impossible. Vérifiez votre réseau ou écrivez-moi sur WhatsApp.", "error"); });
  });
})();

// ---------- Mise en scène : rideau, pointeur, titres, défilements ----------
(function () {
  "use strict";
  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  root.classList.add("js");
  if (fine && !reduce) root.classList.add("fine");
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  // Titres découpés en lettres : chaque lettre arrive à son tour
  document.querySelectorAll(".split .ch").forEach(function (c) { c.style.setProperty("--i", c.getAttribute("data-i") || 0); });

  // Rideau : retombe quand on quitte la page par un lien interne, puis se relève sur la page suivante
  if (!reduce) {
    document.addEventListener("click", function (e) {
      var a = e.target.closest ? e.target.closest("a[href]") : null;
      if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if (a.target && a.target !== "_self") return;
      if (a.hasAttribute("download")) return;
      var url;
      try { url = new URL(a.href, location.href); } catch (err) { return; }
      if (url.origin !== location.origin || !/^https?:$/.test(url.protocol)) return;
      if (/\.(pdf|jpe?g|png|webp|mp4|xml|txt)$/i.test(url.pathname)) return;
      if (url.pathname === location.pathname && url.search === location.search) return; // ancre de la même page
      e.preventDefault();
      root.classList.add("is-leaving");
      setTimeout(function () { location.href = url.href; }, 620);
    });
    window.addEventListener("pageshow", function (e) { if (e.persisted) root.classList.remove("is-leaving"); });
  }

  // En-tête : fond qui apparaît au défilement, se cache en descendant, revient en remontant
  var header = document.getElementById("site-header");
  var lastY = window.scrollY, ticking = false;
  var stepsEl = document.querySelector(".methode .steps");
  var words = [];
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var y = window.scrollY;
      if (header) {
        header.classList.toggle("scrolled", y > 30);
        var menuOpen = document.body.classList.contains("menu-open");
        if (!menuOpen && y > lastY + 4 && y > window.innerHeight * 0.6) header.classList.add("hidden");
        if (y < lastY - 4 || menuOpen) header.classList.remove("hidden");
      }
      lastY = y;
      steps(); paintWords();
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  document.addEventListener("focusin", function () { if (header) header.classList.remove("hidden"); });

  // Méthode : la ligne d'or progresse avec la lecture
  function steps() {
    if (!stepsEl) return;
    var r = stepsEl.getBoundingClientRect(), vh = window.innerHeight;
    var p = clamp((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0, 1);
    stepsEl.style.setProperty("--p", reduce ? 1 : p.toFixed(3));
    var lis = stepsEl.children, n = lis.length;
    for (var i = 0; i < n; i++) lis[i].classList.toggle("lit", reduce || p >= (i + 0.5) / n);
  }

  // Grands paragraphes : les mots s'allument au fil de la lecture
  function splitWords(el) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function (t) {
      var parts = t.nodeValue.split(/(\s+)/), frag = document.createDocumentFragment();
      parts.forEach(function (p) {
        if (!p) return;
        if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
        var s = document.createElement("span"); s.className = "wd"; s.textContent = p; frag.appendChild(s);
      });
      t.parentNode.replaceChild(frag, t);
    });
    return Array.prototype.slice.call(el.querySelectorAll(".wd"));
  }
  if (!reduce) document.querySelectorAll(".words").forEach(function (el) { words.push({ el: el, w: splitWords(el) }); });
  function paintWords() {
    var vh = window.innerHeight;
    words.forEach(function (o) {
      var r = o.el.getBoundingClientRect();
      var p = clamp((vh * 0.9 - r.top) / (r.height + vh * 0.2), 0, 1), n = o.w.length;
      for (var i = 0; i < n; i++) o.w[i].style.setProperty("--o", (0.16 + 0.84 * clamp(p * n * 1.15 - i, 0, 1)).toFixed(2));
    });
  }
  onScroll();

  // Apparitions au défilement
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    document.querySelectorAll(".lift-on, .divider").forEach(function (el) {
      var sib = el.parentNode ? Array.prototype.indexOf.call(el.parentNode.children, el) : 0;
      if (el.classList.contains("lift-on")) el.style.setProperty("--k", Math.min(sib, 6));
      io.observe(el);
    });
  } else {
    document.querySelectorAll(".lift-on, .divider").forEach(function (el) { el.classList.add("in"); });
  }

  // Chiffres qui défilent jusqu'à leur valeur
  var counts = document.querySelectorAll(".count");
  if (counts.length && "IntersectionObserver" in window && !reduce) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (!en.isIntersecting) return; cio.unobserve(en.target); countUp(en.target); });
    }, { threshold: 0.6 });
    counts.forEach(function (el) {
      if (el.querySelector(".todo")) return;
      var m = el.textContent.trim().match(/^([^\d]*)(\d[\d\s  ]*)(.*)$/);
      if (!m) return;
      el.dataset.pre = m[1]; el.dataset.num = m[2].replace(/\D/g, ""); el.dataset.post = m[3]; el.dataset.final = el.textContent;
      cio.observe(el);
    });
  }
  function countUp(el) {
    var target = parseInt(el.dataset.num, 10), t0 = performance.now(), dur = 1700, fmt = new Intl.NumberFormat("fr-FR");
    (function step(now) {
      var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(2, -10 * k);
      el.textContent = el.dataset.pre + fmt.format(Math.round(target * (k === 1 ? 1 : e))) + el.dataset.post;
      if (k < 1) requestAnimationFrame(step); else el.textContent = el.dataset.final;
    })(t0);
  }

  // Pointeur : un point d'or, et un disque qui grossit sur les éléments importants
  var ptr = document.querySelector(".pointer");
  var preview = document.querySelector(".mq-preview");
  var previewImg = preview ? preview.querySelector("img") : null;
  if (ptr && fine && !reduce) {
    var mx = -200, my = -200, rx = -200, ry = -200, vx = 0, label = ptr.querySelector(".pointer-text");
    window.addEventListener("pointermove", function (e) { vx = e.clientX - mx; mx = e.clientX; my = e.clientY; }, { passive: true });
    window.addEventListener("pointerdown", function () { ptr.classList.add("is-down"); });
    window.addEventListener("pointerup", function () { ptr.classList.remove("is-down"); });
    document.addEventListener("pointerover", function (e) {
      var t = e.target.closest ? e.target.closest("[data-cursor]") : null;
      if (t) { label.textContent = t.getAttribute("data-cursor"); ptr.classList.add("is-on"); }
      var row = e.target.closest ? e.target.closest(".mq-row") : null;
      if (row && preview && row.dataset.cover) { if (previewImg.getAttribute("src") !== row.dataset.cover) previewImg.src = row.dataset.cover; preview.classList.add("on"); }
    });
    document.addEventListener("pointerout", function (e) {
      var t = e.target.closest ? e.target.closest("[data-cursor]") : null;
      if (t && !(e.relatedTarget && t.contains(e.relatedTarget))) ptr.classList.remove("is-on");
      var row = e.target.closest ? e.target.closest(".mq-row") : null;
      if (row && preview && !(e.relatedTarget && row.contains(e.relatedTarget))) preview.classList.remove("on");
    });
    (function follow() {
      rx += (mx - rx) * 0.16; ry += (my - ry) * 0.16;
      ptr.style.setProperty("--x", mx + "px"); ptr.style.setProperty("--y", my + "px");
      ptr.style.setProperty("--rx", rx.toFixed(1) + "px"); ptr.style.setProperty("--ry", ry.toFixed(1) + "px");
      if (preview) {
        preview.style.setProperty("--x", rx.toFixed(1) + "px"); preview.style.setProperty("--y", ry.toFixed(1) + "px");
        vx *= 0.9; preview.style.setProperty("--r", clamp(vx * 0.6, -12, 12).toFixed(1) + "deg");
      }
      requestAnimationFrame(follow);
    })();
  }

  // Inclinaison 3D et boutons aimantés
  if (fine && !reduce) {
    document.querySelectorAll(".tilt").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = "perspective(900px) rotateY(" + (x * 10).toFixed(2) + "deg) rotateX(" + (-y * 8).toFixed(2) + "deg)";
      });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });
    document.querySelectorAll(".magnet").forEach(function (b) {
      b.addEventListener("pointermove", function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = "translate(" + ((e.clientX - r.left - r.width / 2) * 0.22).toFixed(1) + "px," + ((e.clientY - r.top - r.height / 2) * 0.3).toFixed(1) + "px)";
      });
      b.addEventListener("pointerleave", function () { b.style.transform = ""; });
    });
    var lx = document.querySelector(".lost-x svg");
    if (lx) window.addEventListener("pointermove", function (e) {
      lx.style.setProperty("--ty", ((e.clientX / window.innerWidth - 0.5) * 50).toFixed(1) + "deg");
      lx.style.setProperty("--tx", ((0.5 - e.clientY / window.innerHeight) * 40).toFixed(1) + "deg");
    }, { passive: true });
  }

  // Rail des créations : boutons, glisser à la souris
  var rail = document.querySelector(".rail");
  if (rail) {
    document.querySelectorAll(".rail-btn").forEach(function (b) {
      b.addEventListener("click", function () {
        var item = rail.querySelector(".rail-item"), w = item ? item.getBoundingClientRect().width + 20 : 300;
        rail.scrollBy({ left: w * Number(b.dataset.dir) * (window.innerWidth > 900 ? 2 : 1), behavior: reduce ? "auto" : "smooth" });
      });
    });
    var down = false, sx = 0, sl = 0, moved = 0;
    rail.addEventListener("pointerdown", function (e) { if (e.pointerType !== "mouse") return; down = true; moved = 0; sx = e.clientX; sl = rail.scrollLeft; rail.classList.add("dragging"); });
    window.addEventListener("pointermove", function (e) { if (!down) return; moved = Math.abs(e.clientX - sx); rail.scrollLeft = sl - (e.clientX - sx); });
    window.addEventListener("pointerup", function () { down = false; rail.classList.remove("dragging"); });
    rail.addEventListener("click", function (e) { if (moved > 6) { e.preventDefault(); e.stopPropagation(); moved = 0; } }, true);
  }
})();

// ---------- Assistant ----------
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var box = document.getElementById("assistant");
  if (!box) return;
  var toggle = box.querySelector(".assistant-toggle");
  var panel = box.querySelector(".assistant-panel");
  var log = box.querySelector(".assistant-log");
  var chips = box.querySelector(".assistant-chips");
  var form = box.querySelector(".assistant-form");
  var input = form.querySelector("input");
  var tpls = Array.prototype.slice.call(box.querySelectorAll("template[data-q]"));
  var fallback = box.querySelector("template[data-fallback]");
  var asked = {};

  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function open(state) {
    toggle.setAttribute("aria-expanded", String(state));
    panel.hidden = !state;
    box.classList.toggle("open", state);
    if (state) setTimeout(function () { input.focus(); }, 60);
  }
  toggle.addEventListener("click", function () { open(panel.hidden); });
  box.querySelector(".assistant-close").addEventListener("click", function () { open(false); toggle.focus(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) { open(false); toggle.focus(); } });

  function renderChips() {
    chips.textContent = "";
    tpls.forEach(function (t, i) {
      if (asked[i]) return;
      var b = document.createElement("button");
      b.type = "button"; b.className = "chip-q"; b.textContent = t.dataset.q;
      b.addEventListener("click", function () { ask(t.dataset.q, i); });
      chips.appendChild(b);
    });
  }
  function bubble(cls, node) {
    var d = document.createElement("div");
    d.className = "msg " + cls;
    if (typeof node === "string") { var p = document.createElement("p"); p.textContent = node; d.appendChild(p); }
    else d.appendChild(node);
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
    return d;
  }
  function fillMail(root) {
    root.querySelectorAll(".mail-js").forEach(function (s) {
      var a = document.createElement("a"), addr = s.dataset.u + "@" + s.dataset.d;
      a.href = "mailto:" + addr; a.textContent = addr; s.textContent = ""; s.appendChild(a);
    });
  }
  function match(q) {
    var n = norm(q), best = -1, score = 0;
    tpls.forEach(function (t, i) {
      var s = 0;
      t.dataset.k.split(",").forEach(function (k) { if (k && n.indexOf(norm(k)) !== -1) s += k.length > 4 ? 2 : 1; });
      if (s > score) { score = s; best = i; }
    });
    return best;
  }
  function ask(q, idx) {
    bubble("me", q);
    if (idx === undefined) idx = match(q);
    if (idx >= 0) asked[idx] = true;
    renderChips();
    var typing = bubble("bot typing", document.createElement("span"));
    typing.firstChild.className = "dots";
    setTimeout(function () {
      typing.remove();
      var frag = (idx >= 0 ? tpls[idx] : fallback).content.cloneNode(true);
      fillMail(frag);
      bubble("bot", frag);
    }, reduce ? 0 : 650);
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = input.value.trim();
    if (!q) return;
    input.value = "";
    ask(q);
  });
  renderChips();
})();
