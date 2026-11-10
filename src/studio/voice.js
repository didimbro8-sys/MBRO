/* AM Voix — voix off open source, 100 % dans le navigateur, gratuite et illimitée.
   Synthèse : Piper (rhasspy/piper, MIT) — modèles français ouverts, exécutés avec onnxruntime-web.
   Phonèmes : espeak-ng compilé en WebAssembly (paquet @diffusionstudio/vits-web, MIT).
   Traitement « voix d'annonceur » : timbre, chaleur, présence, compression, normalisation (Web Audio). */
const VOX = {
  BASE: 'https://huggingface.co/diffusionstudio/piper-voices/resolve/main/',
  PIPER: 'https://cdn.jsdelivr.net/npm/@diffusionstudio/vits-web@1.0.3/dist/piper-DeOu3H9E.js',
  PHON: 'https://cdn.jsdelivr.net/npm/@diffusionstudio/piper-wasm@1.0.0/build/piper_phonemize',
  ORT: 'https://cdnjs.cloudflare.com/ajax/libs/onnxruntime-web/1.18.0/',
  VOICES: {
    pierre: { f: 'fr/fr_FR/upmc/medium/fr_FR-upmc-medium', sid: 'pierre', label: 'Pierre · homme posé', lic: 'CC-BY-SA 4.0', timbre: .93 },
    gilles: { f: 'fr/fr_FR/gilles/low/fr_FR-gilles-low', label: 'Gilles · homme', lic: 'CC0', timbre: .95 },
    siwis: { f: 'fr/fr_FR/siwis/medium/fr_FR-siwis-medium', label: 'Siwis · femme claire', lic: 'CC-BY 4.0', timbre: 1 },
    jessica: { f: 'fr/fr_FR/upmc/medium/fr_FR-upmc-medium', sid: 'jessica', label: 'Jessica · femme', lic: 'CC-BY-SA 4.0', timbre: 1 }
  },
  sessions: {},
  async fetchCached(url, kind) {
    let r = null;
    try { const c = await caches.open('amstudio-voix'); r = await c.match(url); if (!r) { r = await fetch(url); if (r.ok) await c.put(url, r.clone()); } }
    catch (e) { r = await fetch(url); }
    if (!r.ok) throw new Error('téléchargement de la voix impossible (' + r.status + ')');
    return kind === 'json' ? r.json() : r.arrayBuffer();
  },
  async ort() {
    if (window.ort) return window.ort;
    await new Promise((res, rej) => { const s = document.createElement('script'); s.src = VOX.ORT + 'ort.min.js'; s.onload = res; s.onerror = () => rej(new Error('moteur de voix non chargé (internet requis)')); document.head.appendChild(s); });
    ort.env.wasm.wasmPaths = VOX.ORT; ort.env.wasm.numThreads = 1; return ort;
  },
  async load(id) {
    if (VOX.sessions[id]) return VOX.sessions[id];
    const v = VOX.VOICES[id] || VOX.VOICES.pierre, O = await VOX.ort();
    const cfg = await VOX.fetchCached(VOX.BASE + v.f + '.onnx.json', 'json');
    const sess = await O.InferenceSession.create(await VOX.fetchCached(VOX.BASE + v.f + '.onnx'));
    return (VOX.sessions[id] = { sess, cfg, sid: v.sid != null ? (cfg.speaker_id_map || {})[v.sid] ?? 0 : null });
  },
  async phonemes(text, lang) {
    const m = await import(VOX.PIPER);
    return new Promise(async (res, rej) => {
      const t = setTimeout(() => rej(new Error('phonèmes : délai dépassé')), 30000);
      const mod = await m.createPiperPhonemize({ print: l => { clearTimeout(t); try { res(JSON.parse(l).phoneme_ids); } catch (e) { rej(e); } }, printErr: () => {}, locateFile: f => f.endsWith('.wasm') ? VOX.PHON + '.wasm' : f.endsWith('.data') ? VOX.PHON + '.data' : f });
      mod.callMain(['-l', lang, '--input', JSON.stringify([{ text }]), '--espeak_data', '/espeak-ng-data']);
    });
  },
  async line(text, id, speed = 1) {
    const { sess, cfg, sid } = await VOX.load(id), O = window.ort;
    const ids = await VOX.phonemes(text, cfg.espeak.voice), inf = cfg.inference || {};
    const feeds = {
      input: new O.Tensor('int64', BigInt64Array.from(ids.map(BigInt)), [1, ids.length]),
      input_lengths: new O.Tensor('int64', BigInt64Array.from([BigInt(ids.length)]), [1]),
      scales: new O.Tensor('float32', Float32Array.from([inf.noise_scale ?? .667, (inf.length_scale ?? 1) / speed, inf.noise_w ?? .8]), [3])
    };
    if (sid != null) feeds.sid = new O.Tensor('int64', BigInt64Array.from([BigInt(sid)]), [1]);
    const out = await sess.run(feeds);
    return { data: out.output.data, rate: cfg.audio.sample_rate };
  },
  /* script : une ligne par phrase. « Aya : texte » utilise la voix du personnage Aya (casting), sinon la voix du narrateur. */
  async speak(script, o = {}) {
    const lines = String(script || '').split(/\n+/).map(s => s.trim()).filter(Boolean); if (!lines.length) throw new Error('texte vide');
    const parts = []; let rate = 22050;
    for (const [k, raw] of lines.entries()) {
      const m = raw.match(/^([^:]{1,24})\s*:\s*(.+)$/), who = m && (o.cast || {})[m[1].trim().toLowerCase()], id = who || o.voice || 'pierre', text = m && who ? m[2] : raw;
      o.status && o.status(`Voix : phrase ${k + 1} / ${lines.length}`);
      let said = text; for (const [w, s] of Object.entries(o.pron || {})) said = said.split(w).join(s); // prononciations (noms de marque…)
      const r = await VOX.line(said, id, o.speed || 1); rate = r.rate; parts.push({ data: r.data, timbre: o.timbre || VOX.VOICES[id]?.timbre || 1 });
    }
    const gap = Math.round(rate * (o.pause ?? .35));
    // chaque phrase est traitée (timbre + chaîne « annonceur ») puis assemblée
    const out = [];
    for (const p of parts) out.push(await VOX.process(p.data, rate, p.timbre), new Float32Array(gap));
    const len = out.reduce((a, b) => a + b.length, 0), all = new Float32Array(len); let off = 0; for (const a of out) { all.set(a, off); off += a.length; }
    let peak = 0; for (const s of all) peak = Math.max(peak, Math.abs(s)); const g = peak ? .89 / peak : 1; for (let i = 0; i < len; i++) all[i] *= g;
    return VOX.wav(all, rate);
  },
  async process(data, rate, timbre) {
    const n = Math.ceil(data.length / timbre) + rate * .05, ctx = new OfflineAudioContext(1, n, rate), buf = ctx.createBuffer(1, data.length, rate); buf.copyToChannel(data, 0);
    const src = ctx.createBufferSource(); src.buffer = buf; src.playbackRate.value = timbre;
    const hp = ctx.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 70;
    const warm = ctx.createBiquadFilter(); warm.type = 'lowshelf'; warm.frequency.value = 160; warm.gain.value = 4;
    const pres = ctx.createBiquadFilter(); pres.type = 'peaking'; pres.frequency.value = 3200; pres.Q.value = .9; pres.gain.value = 3;
    const air = ctx.createBiquadFilter(); air.type = 'highshelf'; air.frequency.value = 9000; air.gain.value = 2;
    const comp = ctx.createDynamicsCompressor(); comp.threshold.value = -22; comp.ratio.value = 3.5; comp.attack.value = .004; comp.release.value = .18; comp.knee.value = 8;
    src.connect(hp).connect(warm).connect(pres).connect(air).connect(comp).connect(ctx.destination); src.start();
    return (await ctx.startRendering()).getChannelData(0);
  },
  wav(f, rate) {
    const b = new ArrayBuffer(44 + f.length * 2), v = new DataView(b), w = (o, s) => [...s].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)));
    w(0, 'RIFF'); v.setUint32(4, 36 + f.length * 2, true); w(8, 'WAVE'); w(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
    v.setUint32(24, rate, true); v.setUint32(28, rate * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); w(36, 'data'); v.setUint32(40, f.length * 2, true);
    for (let i = 0; i < f.length; i++) v.setInt16(44 + i * 2, Math.max(-1, Math.min(1, f[i])) * 32767, true);
    return new Blob([b], { type: 'audio/wav' });
  }
};
