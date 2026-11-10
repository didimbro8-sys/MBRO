/* AM Studio Vidéo IA — moteur de montage : dessine les plans sur un canevas et enregistre la vidéo, dans le navigateur. */
const FORMATS = { '9:16': [1080, 1920], '1:1': [1080, 1080], '16:9': [1920, 1080] };
const AUB = '#1a0014', AUB2 = '#3a0730', GOLD = '#f1bc18';

function wrap(ctx, text, maxW) {
  const words = String(text || '').split(/\s+/), lines = []; let line = '';
  for (const w of words) { const t = line ? line + ' ' + w : w; if (ctx.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t; }
  if (line) lines.push(line); return lines;
}
function cover(ctx, src, sw, sh, W, H, zoom = 1, px = 0) {
  const r = Math.max(W / sw, H / sh) * zoom, w = sw * r, h = sh * r;
  ctx.drawImage(src, (W - w) / 2 + px * W, (H - h) / 2, w, h);
}
function bg(ctx, W, H) { const g = ctx.createLinearGradient(0, 0, W, H); g.addColorStop(0, AUB2); g.addColorStop(1, AUB); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); }

const M = {
  running: false, stopReq: false,
  stop() { M.stopReq = true; },
  async load(p) {
    const items = [];
    for (const s of p.shots) {
      const it = { s, dur: Math.max(1, +s.duration || 5) }, m = s.media && S.data.media[s.media], u = m && await mediaURL(s.media);
      if (u && m.type === 'video') {
        const v = document.createElement('video'); v.src = u; v.loop = false; /* un clip plus court que le plan reste figé sur sa dernière image */ v.playsInline = true; v.muted = !p.mont.clipAudio; v.preload = 'auto';
        await new Promise(r => { v.onloadeddata = r; v.onerror = r; setTimeout(r, 6000); }); it.v = v;
      } else if (u && m.type === 'image') { const i = new Image(); i.src = u; await i.decode().catch(() => {}); it.img = i; }
      items.push(it);
    }
    if (p.mont.endCard) items.push({ end: true, dur: 3 });
    let logo = null; const lu = await mediaURL(p.logo); if (lu) { logo = new Image(); logo.src = lu; await logo.decode().catch(() => { logo = null; }); }
    return { items, logo };
  },
  draw(ctx, W, H, it, lt, idx, p, logo) {
    const u = W / 1080; ctx.globalAlpha = 1; ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
    if (it.end) {
      bg(ctx, W, H); const k = Math.min(1, lt / 0.6); ctx.globalAlpha = k; ctx.textAlign = 'center';
      if (logo) { const lh = 160 * u, lw = logo.naturalWidth / logo.naturalHeight * lh; ctx.drawImage(logo, (W - lw) / 2, H / 2 - lh - 90 * u, lw, lh); }
      ctx.fillStyle = '#fff'; ctx.font = `900 ${84 * u}px Montserrat, sans-serif`;
      wrap(ctx, p.mont.endTitle || p.title, W * .84).forEach((l, i) => ctx.fillText(l, W / 2, H / 2 + i * 96 * u));
      ctx.fillStyle = GOLD; ctx.font = `700 ${38 * u}px Montserrat, sans-serif`; ctx.fillText(p.mont.endSub || '', W / 2, H / 2 + 120 * u);
      ctx.fillRect(W / 2 - 60 * u, H / 2 + 160 * u, 120 * u * k, 6 * u); ctx.globalAlpha = 1; return;
    }
    const s = it.s, k = Math.min(1, lt / it.dur);
    if (it.v && it.v.videoWidth) cover(ctx, it.v, it.v.videoWidth, it.v.videoHeight, W, H);
    else if (it.img && it.img.naturalWidth) cover(ctx, it.img, it.img.naturalWidth, it.img.naturalHeight, W, H, 1.04 + .1 * k, (idx % 2 ? 1 : -1) * .02 * k);
    else { // animatique : carte texte du plan
      bg(ctx, W, H); ctx.textAlign = 'left'; const x = 80 * u;
      ctx.fillStyle = GOLD; ctx.font = `800 ${34 * u}px Montserrat, sans-serif`; ctx.fillText(`PLAN ${idx + 1} · ${(s.beat || '').toUpperCase()}`, x, H * .3);
      ctx.fillStyle = '#fff'; ctx.font = `700 ${52 * u}px Montserrat, sans-serif`;
      wrap(ctx, s.desc, W - 2 * x).slice(0, 7).forEach((l, i) => ctx.fillText(l, x, H * .3 + 90 * u + i * 66 * u));
      ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.font = `600 ${28 * u}px Montserrat, sans-serif`; ctx.fillText(`${s.camera} · clip à générer`, x, H * .3 + 90 * u + 7.6 * 66 * u);
    }
    if (s.overlay) { // texte à l'écran, or
      const a = Math.min(1, Math.max(0, (lt - .3) / .5)); ctx.globalAlpha = a; ctx.textAlign = 'center'; ctx.font = `900 ${64 * u}px Montserrat, sans-serif`;
      const ls = wrap(ctx, s.overlay.toUpperCase(), W * .86), y0 = H * .18;
      ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 18 * u; ctx.fillStyle = GOLD; ls.forEach((l, i) => ctx.fillText(l, W / 2, y0 + i * 74 * u)); ctx.shadowBlur = 0; ctx.globalAlpha = 1;
    }
    if (p.mont.subs && s.dialogue) { // sous-titres
      ctx.font = `700 ${44 * u}px Montserrat, sans-serif`; ctx.textAlign = 'center';
      const ls = wrap(ctx, s.dialogue, W * .8), lh = 58 * u, y = H * (p.format === '16:9' ? .86 : .78) - (ls.length - 1) * lh;
      ls.forEach((l, i) => { const w = ctx.measureText(l).width + 36 * u; ctx.fillStyle = 'rgba(26,0,20,.78)'; ctx.fillRect(W / 2 - w / 2, y + i * lh - 44 * u, w, lh); ctx.fillStyle = '#fff'; ctx.fillText(l, W / 2, y + i * lh); });
    }
    if (logo) { const lh = 70 * u, lw = logo.naturalWidth / logo.naturalHeight * lh; ctx.globalAlpha = .9; ctx.drawImage(logo, W - lw - 40 * u, 40 * u, lw, lh); ctx.globalAlpha = 1; }
    if (lt < .3) { ctx.fillStyle = `rgba(0,0,0,${1 - lt / .3})`; ctx.fillRect(0, 0, W, H); }
  },
  async poster(p, canvas) {
    if (!p || !canvas) return; const [W, H] = FORMATS[p.format]; canvas.width = W; canvas.height = H;
    await document.fonts.load('900 60px Montserrat').catch(() => {});
    const { items, logo } = await M.load(p); const ctx = canvas.getContext('2d');
    if (items[0]) M.draw(ctx, W, H, items[0], 1, 0, p, logo);
  },
  /* Export image par image (WebCodecs + mp4-muxer, open source) : MP4 H.264 exact, plus rapide que le temps réel,
     indépendant de ce qui est affiché à l'écran. Repli sur l'enregistreur temps réel si le navigateur ne le permet pas. */
  async encode(p, canvas, onProgress) {
    const { Muxer, ArrayBufferTarget } = await import('https://cdn.jsdelivr.net/npm/mp4-muxer@5.1.3/+esm');
    const [W, H] = FORMATS[p.format], fps = 30; canvas.width = W; canvas.height = H; const ctx = canvas.getContext('2d');
    let vcfg = null;
    for (const codec of ['avc1.640028', 'avc1.4d0028', 'avc1.640033', 'avc1.42003e']) {
      const c = { codec, width: W, height: H, bitrate: 10e6, framerate: fps };
      if ((await VideoEncoder.isConfigSupported(c).catch(() => ({}))).supported) { vcfg = c; break; }
    }
    if (!vcfg) throw new Error('encodeur H.264 indisponible');
    // voix : décodage puis encodage AAC (ou Opus)
    let pcm = null, acfg = null;
    const vu = await mediaURL(p.voice);
    if (vu && window.AudioEncoder) {
      const buf = await (await fetch(vu)).arrayBuffer(), dec = await new AudioContext().decodeAudioData(buf);
      const delay = Math.max(0, +(p.vox && p.vox.delay) || 0);
      const off = new OfflineAudioContext(2, Math.ceil((dec.duration + delay) * 48000), 48000), src = off.createBufferSource(); src.buffer = dec; src.connect(off.destination); src.start(delay); pcm = await off.startRendering();
      for (const codec of ['mp4a.40.2', 'opus']) { const c = { codec, sampleRate: 48000, numberOfChannels: 2, bitrate: 128000 }; if ((await AudioEncoder.isConfigSupported(c).catch(() => ({}))).supported) { acfg = c; break; } }
    }
    const target = new ArrayBufferTarget();
    const muxer = new Muxer({ target, fastStart: 'in-memory', video: { codec: 'avc', width: W, height: H }, ...(acfg ? { audio: { codec: acfg.codec === 'opus' ? 'opus' : 'aac', sampleRate: 48000, numberOfChannels: 2 } } : {}) });
    let fail = null;
    const ve = new VideoEncoder({ output: (ch, meta) => muxer.addVideoChunk(ch, meta), error: e => fail = e }); ve.configure(vcfg);
    await Promise.all(['900 60px Montserrat', '700 40px Montserrat', '800 30px Montserrat'].map(f => document.fonts.load(f).catch(() => {})));
    const { items, logo } = await M.load(p), total = items.reduce((a, b) => a + b.dur, 0), N = Math.round(total * fps);
    const seek = (v, t) => new Promise(r => { if (Math.abs(v.currentTime - t) < 1e-3) return r(); const h = () => { v.removeEventListener('seeked', h); r(); }; v.addEventListener('seeked', h); v.currentTime = t; setTimeout(r, 3000); });
    for (let n = 0; n < N; n++) {
      if (M.stopReq || fail) break;
      const t = n / fps; let acc = 0, idx = 0; while (idx < items.length - 1 && t >= acc + items[idx].dur) { acc += items[idx].dur; idx++; }
      const it = items[idx], lt = t - acc;
      if (it.v) await seek(it.v, Math.min(lt, Math.max(0, it.v.duration - .04)));
      M.draw(ctx, W, H, it, lt, idx, p, logo);
      const fr = new VideoFrame(canvas, { timestamp: Math.round(n * 1e6 / fps), duration: Math.round(1e6 / fps) });
      ve.encode(fr, { keyFrame: n % 60 === 0 }); fr.close();
      while (ve.encodeQueueSize > 8) await new Promise(r => setTimeout(r, 5));
      if (n % 10 === 0) { onProgress && onProgress(n / N * (acfg ? .95 : 1)); await new Promise(r => setTimeout(r, 0)); }
    }
    await ve.flush(); ve.close();
    if (acfg && pcm && !M.stopReq) {
      const ae = new AudioEncoder({ output: (ch, meta) => muxer.addAudioChunk(ch, meta), error: e => fail = e }); ae.configure(acfg);
      const len = Math.min(pcm.length, Math.round(total * 48000)), L = pcm.getChannelData(0), R = pcm.getChannelData(1), step = 1024;
      for (let i = 0; i < len; i += step) {
        const k = Math.min(step, len - i), d = new Float32Array(k * 2); d.set(L.subarray(i, i + k), 0); d.set(R.subarray(i, i + k), k);
        const ad = new AudioData({ format: 'f32-planar', sampleRate: 48000, numberOfFrames: k, numberOfChannels: 2, timestamp: Math.round(i / 48000 * 1e6), data: d });
        ae.encode(ad); ad.close();
      }
      await ae.flush(); ae.close();
    }
    if (fail) throw fail;
    if (M.stopReq) return null;
    muxer.finalize(); onProgress && onProgress(1);
    return new Blob([target.buffer], { type: 'video/mp4' });
  },
  async play(p, canvas, { record = false, onProgress } = {}) {
    if (M.running) return null;
    if (record && window.VideoEncoder && window.VideoFrame) {
      M.running = true; M.stopReq = false;
      try { return await M.encode(p, canvas, onProgress); }
      catch (e) { console.warn('Export image par image impossible, repli temps réel :', e); toast('Export rapide indisponible (' + e.message + '), export en temps réel'); }
      finally { M.running = false; }
    } if (!p.shots.length && !p.mont.endCard) { toast('Aucun plan à monter'); return null; }
    M.running = true; M.stopReq = false; const stage = canvas.closest('.stage'); if (record && stage) stage.classList.add('live');
    const [W, H] = FORMATS[p.format]; canvas.width = W; canvas.height = H; const ctx = canvas.getContext('2d');
    await Promise.all(['900 60px Montserrat', '700 40px Montserrat', '800 30px Montserrat'].map(f => document.fonts.load(f).catch(() => {})));
    const { items, logo } = await M.load(p);
    const AC = new (window.AudioContext || window.webkitAudioContext)(), dest = AC.createMediaStreamDestination();
    if (p.mont.clipAudio) items.forEach(it => { if (it.v) { const so = AC.createMediaElementSource(it.v); so.connect(dest); so.connect(AC.destination); } });
    let audio = null; const vu = await mediaURL(p.voice);
    if (vu) { audio = new Audio(vu); const so = AC.createMediaElementSource(audio); so.connect(dest); so.connect(AC.destination); }
    const total = items.reduce((a, b) => a + b.dur, 0);
    let rec = null; const chunks = [];
    if (record) {
      const st = canvas.captureStream(30); dest.stream.getAudioTracks().forEach(t => st.addTrack(t));
      const mime = ['video/mp4;codecs=avc1.42E01E,mp4a.40.2', 'video/mp4', 'video/webm;codecs=vp9,opus', 'video/webm;codecs=vp8,opus', 'video/webm'].find(m => window.MediaRecorder && MediaRecorder.isTypeSupported(m));
      if (!mime) { toast('Ce navigateur ne sait pas enregistrer de vidéo : utilisez Chrome ou Edge.'); M.running = false; AC.close(); return null; }
      rec = new MediaRecorder(st, { mimeType: mime, videoBitsPerSecond: 8e6 }); rec.ondataavailable = e => e.data.size && chunks.push(e.data); rec.start(500);
    }
    await AC.resume().catch(() => {}); if (audio) setTimeout(() => M.running && audio.play().catch(() => {}), Math.max(0, +(p.vox && p.vox.delay) || 0) * 1000);
    const t0 = performance.now(); let cur = -1;
    return new Promise(resolve => {
      const finish = () => {
        items.forEach(i => i.v && i.v.pause()); if (audio) audio.pause(); M.running = false; if (stage) stage.classList.remove('live'); onProgress && onProgress(1);
        if (rec) { rec.onstop = () => { AC.close(); resolve(M.stopReq ? null : new Blob(chunks, { type: rec.mimeType })); }; rec.stop(); } else { AC.close(); resolve(null); }
      };
      const frame = () => {
        const t = (performance.now() - t0) / 1000; if (t >= total || M.stopReq) return finish();
        let acc = 0, idx = 0; while (idx < items.length - 1 && t >= acc + items[idx].dur) { acc += items[idx].dur; idx++; }
        const it = items[idx];
        if (idx !== cur) { if (cur >= 0 && items[cur].v) items[cur].v.pause(); if (it.v) { it.v.currentTime = 0; it.v.play().catch(() => {}); } cur = idx; }
        M.draw(ctx, W, H, it, t - acc, idx, p, logo); onProgress && onProgress(t / total);
        requestAnimationFrame(frame);
      };
      requestAnimationFrame(frame);
    });
  },
  srt(p) {
    const f = s => { const ms = Math.round(s * 1000), h = Math.floor(ms / 36e5), m = Math.floor(ms / 6e4) % 60, se = Math.floor(ms / 1000) % 60; return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(se).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`; };
    let t = 0, n = 0; const out = [];
    for (const s of p.shots) { const d = Math.max(1, +s.duration || 5); if (s.dialogue) out.push(`${++n}\n${f(t + .2)} --> ${f(t + d - .1)}\n${s.dialogue}\n`); t += d; }
    return out.join('\n');
  }
};
