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
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        toggle.setAttribute("aria-expanded", "false");
        nav.setAttribute("data-open", "false");
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
