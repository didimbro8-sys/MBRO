/* AM Studio Vidéo IA — logique principale (sans serveur, sans abonnement). */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const uid = () => Math.random().toString(36).slice(2, 9);

/* ---------- Données de référence ---------- */
const DECORS = [
  { id: 'plateau', name: 'Bureau au Plateau', desc: 'modern glass office interior in Le Plateau business district, Abidjan, lagoon and skyline through the windows' },
  { id: 'maquis', name: 'Maquis animé', desc: 'lively open-air Ivorian maquis restaurant, plastic chairs, string lights, grilled fish and attiéké on the tables' },
  { id: 'cocody', name: 'Villa à Cocody', desc: 'elegant modern villa living room in Cocody, Abidjan, tropical plants, warm wood, large windows' },
  { id: 'treichville', name: 'Marché de Treichville', desc: 'busy colorful market in Treichville, Abidjan, wax fabric stalls, vendors, natural motion' },
  { id: 'yopougon', name: 'Rue de Yopougon', desc: 'vibrant street in Yopougon, Abidjan, small shops, orange woro-woro taxis, people walking' },
  { id: 'bassam', name: 'Plage de Grand-Bassam', desc: 'Grand-Bassam beach, ocean waves, coconut palms, colonial-era facades in the distance' },
  { id: 'lagune', name: 'Lagune Ébrié', desc: 'Ebrie lagoon in Abidjan with a modern cable-stayed bridge and the Plateau skyline' },
  { id: 'studio', name: 'Studio aubergine', desc: 'minimal studio set with a deep aubergine backdrop and a soft gold rim light' }
];
const LOOKS = [
  { id: 'golden', name: 'Lumière dorée de fin de journée', desc: 'warm golden hour sunlight, low sun, long soft shadows, glowing skin highlights' },
  { id: 'nuit', name: 'Nuit urbaine', desc: 'night, warm practical lights and cool blue ambient light, reflections, cinematic contrast' },
  { id: 'doux', name: 'Jour doux', desc: 'soft overcast daylight, even and flattering on dark skin tones' },
  { id: 'pub', name: 'Studio publicitaire', desc: 'three-point studio lighting, soft key light, gold rim light, clean commercial look' },
  { id: 'interieur', name: 'Intérieur chaleureux', desc: 'warm tungsten interior light mixed with window light, cozy atmosphere' }
];
const CAMS = {
  'Plan fixe': 'Static locked-off shot', 'Travelling avant lent': 'Slow dolly-in', 'Travelling latéral': 'Smooth lateral tracking shot',
  'Panoramique': 'Slow pan', "Caméra à l'épaule": 'Handheld camera, natural micro-shake', 'Gros plan visage': 'Close-up on the face, shallow depth of field',
  "Plan large d'ensemble": 'Wide establishing shot', 'Contre-plongée': 'Low-angle shot', 'Drone en approche': 'Aerial drone shot flying in',
  'Orbite autour du sujet': 'Slow orbit around the subject'
};
const TYPES = { spot: 'Spot publicitaire', serie: 'Épisode de série', film: 'Film court' };
const FMTS = ['9:16', '1:1', '16:9'];
const REAL = "Photorealistic, cinematic, shot on a cinema camera with a 35mm lens, natural film grain. Realistic dark skin with visible pores, natural sheen and accurate melanin tones, no waxy or plastic skin. Anatomically correct hands with five fingers. Natural eyes and micro-expressions. Authentic people and places of Côte d'Ivoire.";
const NEG = 'cartoon, anime, 3d render, plastic skin, waxy skin, over-smoothed face, extra fingers, deformed hands, distorted face, text, subtitles, watermark, logo, blurry, oversaturated';
const TOOLS = [
  { id: 'open', name: 'Moteur open source intégré (gratuit)', url: 'https://huggingface.co/spaces', note: 'FLUX.1 Krea crée l’image du plan, Wan 2.2 l’anime en vidéo, directement ici. Clips muets : voix et sons se posent au montage.' },
  { id: 'dreamina', name: 'Dreamina (Seedance)', url: 'https://dreamina.capcut.com', note: 'Le modèle Seedance de ByteDance. Accepte des images de référence : envoyez-y les photos du casting.' },
  { id: 'kling', name: 'Kling AI', url: 'https://klingai.com', note: 'Très bon sur les mouvements humains. Collez le « prompt négatif » dans le champ prévu.' },
  { id: 'flow', name: 'Google Flow (Veo)', url: 'https://labs.google/flow', note: 'Réalisme et son. Les répliques sont écrites pour être dites à voix haute.' },
  { id: 'meta', name: 'Meta AI', url: 'https://www.meta.ai', note: 'Outil gratuit de Meta, utile pour des plans simples ou animer une image.' },
  { id: 'hailuo', name: 'Hailuo (MiniMax)', url: 'https://hailuoai.video', note: 'Bon rendu des visages, plans de 6 secondes.' }
];
const BEATS = {
  spot: [['Accroche', "Plan choc qui arrête le pouce : {cible} dans {lieu}"], ['Situation', "{cible} au quotidien, ambiance {ton}"], ['Produit', '{produit} apparaît, bien mis en valeur, gros plan net'], ['Bénéfice', '{message}'], ['Émotion', 'Réaction vraie, sourire, ambiance {ton}'], ["Appel à l'action", '{cta}']],
  serie: [['Ouverture', 'Plan large qui installe {lieu}'], ['Personnage', 'On découvre le personnage principal, {ton}'], ['Dialogue', 'Échange entre les personnages autour de : {message}'], ['Réaction', 'Gros plan sur la réaction'], ['Tension', 'Un imprévu relance la scène : {objectif}'], ['Chute', 'Fin de scène qui donne envie de voir la suite']],
  film: [['Ouverture', 'Plan large qui installe {lieu}, ambiance {ton}'], ['Héros', 'Le héros en action'], ['Enjeu', '{objectif}'], ['Obstacle', 'Le héros rencontre une difficulté'], ['Tournant', '{message}'], ['Résolution', 'Dernière image forte, {cta}']]
};

/* ---------- Stockage : textes dans le navigateur, médias dans IndexedDB ---------- */
const DB = {
  db: null,
  open() { return new Promise((res, rej) => { const r = indexedDB.open('amstudio', 1); r.onupgradeneeded = () => r.result.createObjectStore('media'); r.onsuccess = () => { DB.db = r.result; res(); }; r.onerror = () => rej(r.error); }); },
  run(mode, fn) { return new Promise((res, rej) => { const t = DB.db.transaction('media', mode); const q = fn(t.objectStore('media')); t.oncomplete = () => res(q && q.result); t.onerror = () => rej(t.error); }); },
  put(id, b) { return DB.run('readwrite', s => s.put(b, id)); },
  get(id) { return DB.run('readonly', s => s.get(id)); },
  del(id) { return DB.run('readwrite', s => s.delete(id)); }
};
const urls = {};
async function mediaURL(id) {
  if (!id) return null; if (urls[id]) return urls[id];
  const b = await DB.get(id).catch(() => null); if (!b) return null;
  return (urls[id] = URL.createObjectURL(b));
}
async function storeBlob(blob, name) {
  const id = 'm' + uid(); await DB.put(id, blob); urls[id] = URL.createObjectURL(blob);
  const t = blob.type || '', type = t.startsWith('video') ? 'video' : t.startsWith('audio') ? 'audio' : 'image';
  S.data.media[id] = { type, name: name || type }; save(); return id;
}
const S = {
  data: null,
  load() { try { S.data = JSON.parse(localStorage.getItem('amstudio') || 'null'); } catch (e) { S.data = null; } if (!S.data) { S.data = { projects: [], characters: [], decors: [], media: {} }; seed(); S.save(); } },
  save() { try { localStorage.setItem('amstudio', JSON.stringify(S.data)); } catch (e) { toast('Sauvegarde impossible : ' + e.message); } }
};
let saveT; function save() { clearTimeout(saveT); saveT = setTimeout(S.save, 250); }
function toast(m) { const t = $('#toast'); t.textContent = m; t.classList.add('on'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('on'), 2600); }
function download(blob, name) { const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 4000); }
const slug = s => String(s || 'video').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '').toLowerCase().slice(0, 40);

/* ---------- Modèles ---------- */
function newProject(o = {}) {
  return Object.assign({
    id: 'p' + uid(), title: 'Nouveau projet', client: '', type: 'spot', format: '9:16', created: Date.now(),
    brief: { produit: '', objectif: '', cible: '', message: '', ton: '', lieu: '', cta: '', decor: 'plateau', look: 'golden', duree: 30, chars: [] },
    shots: [], voice: null, voiceText: '', logo: null,
    mont: { subs: true, clipAudio: false, endCard: true, endTitle: '', endSub: 'AM Digital' }
  }, o);
}
function newShot(o = {}) { return Object.assign({ id: 's' + uid(), beat: 'Plan', desc: '', camera: 'Plan fixe', decor: 'plateau', look: 'golden', chars: [], dialogue: '', overlay: '', duration: 5, media: null }, o); }
function autoShots(p) {
  const b = p.brief, list = BEATS[p.type] || BEATS.spot, n = Math.max(2, Math.round((+b.duree || 30) / 5));
  const fill = t => { const s = t.replace(/\{(\w+)\}/g, (_, k) => b[k] || '…'); return s.charAt(0).toUpperCase() + s.slice(1); };
  const cams = ["Plan large d'ensemble", 'Travelling avant lent', 'Gros plan visage', 'Travelling latéral', "Caméra à l'épaule", 'Contre-plongée'];
  return Array.from({ length: n }, (_, i) => {
    const k = n >= list.length ? Math.min(i, list.length - 1) : Math.round(i * (list.length - 1) / (n - 1));
    const [beat, tpl] = n > list.length && i >= list.length - 1 && i < n - 1 ? ['Plan de coupe', 'Détail du lieu ou du produit, {ton}'] : list[k];
    const last = i === n - 1;
    return newShot({ beat: last ? list[list.length - 1][0] : beat, desc: fill(last ? list[list.length - 1][1] : tpl), camera: cams[i % cams.length], decor: b.decor, look: b.look, chars: [...(b.chars || [])], overlay: last && p.type === 'spot' ? (b.cta || '') : '' });
  });
}
function seed() {
  const aya = { id: 'c' + uid(), name: 'Aya', age: '27 ans', desc: 'Ivorian woman, 27 years old, deep brown skin, natural coily hair in a high puff, warm confident smile, slim build', tenue: 'yellow and green wax print dress', voix: 'Voix féminine chaleureuse (ElevenLabs, à choisir)', photos: [] };
  const koffi = { id: 'c' + uid(), name: 'Koffi', age: '34 ans', desc: 'Ivorian man, 34 years old, very dark skin, short fade haircut, neat beard, athletic build, friendly eyes', tenue: 'light blue linen shirt', voix: 'Bass (ElevenLabs)', photos: [] };
  S.data.characters.push(aya, koffi);
  const p = newProject({
    title: 'Bissap Wôrô — spot 30 s', client: 'Concept de démonstration',
    brief: { produit: 'Bissap Wôrô, jus de bissap artisanal en bouteille (marque fictive)', objectif: 'faire connaître la boisson aux jeunes actifs', cible: 'des jeunes actifs abidjanais', message: 'Le goût vrai du bissap, bien frais, à toute heure', ton: 'chaleureuse et solaire', lieu: 'un maquis de Yopougon', cta: 'Demande Bissap Wôrô dans ton maquis', decor: 'maquis', look: 'golden', duree: 30, chars: [aya.id, koffi.id] },
    mont: { subs: true, clipAudio: false, endCard: true, endTitle: 'Bissap Wôrô', endSub: 'Concept de démonstration · AM Digital' }
  });
  p.shots = autoShots(p);
  p.shots[4].dialogue = "Ça, c'est le goût vrai du bissap !";
  p.voiceText = p.shots.map(s => s.dialogue).filter(Boolean).join('\n');
  S.data.projects.push(p);
}
const proj = id => S.data.projects.find(p => p.id === id);
const charById = id => S.data.characters.find(c => c.id === id);
const allDecors = () => DECORS.concat(S.data.decors);
const decorById = id => allDecors().find(d => d.id === id);

/* ---------- Prompts ---------- */
function shotPrompt(p, s, tool) {
  const chars = (s.chars || []).map(charById).filter(Boolean), dec = decorById(s.decor), look = LOOKS.find(l => l.id === s.look);
  const ratio = { '9:16': 'vertical 9:16', '1:1': 'square 1:1', '16:9': 'horizontal 16:9' }[p.format];
  let t = `${CAMS[s.camera] || s.camera}. ${s.desc || ''}`.trim().replace(/\.?$/, '.');
  if (chars.length) t += ' Characters: ' + chars.map(c => `${c.name}, ${c.desc}${c.tenue ? ', wearing ' + c.tenue : ''}`).join('; ') + '.';
  if (dec) t += ` Setting: ${dec.desc}.`;
  if (look) t += ` Lighting: ${look.desc}.`;
  t += ` Format: ${ratio}, ${s.duration || 5} seconds. ${REAL}`;
  if (s.dialogue) {
    const who = chars[0] ? chars[0].name : 'The character';
    t += tool === 'flow' ? ` ${who} says in French, with a natural Ivorian accent: "${s.dialogue}"` : ` ${who} speaks in French with a natural Ivorian accent, lips perfectly synced: "${s.dialogue}"`;
  } else t += ' No dialogue.';
  if (tool === 'dreamina' && chars.some(c => c.photos.length)) t += ' Keep exactly the same face, hairstyle and outfit as the reference images.';
  if (tool !== 'kling') t += ` Avoid: ${NEG}.`;
  return t;
}
function imagePrompt(p, s) {
  const chars = (s.chars || []).map(charById).filter(Boolean), dec = decorById(s.decor), look = LOOKS.find(l => l.id === s.look);
  const shape = { '9:16': 'Vertical', '1:1': 'Square', '16:9': 'Horizontal' }[p.format];
  let t = `${shape} cinematic film still. ${s.desc || ''}`.trim().replace(/\.?$/, '.');
  if (chars.length) t += ' ' + chars.map(c => `${c.name}: ${c.desc}${c.tenue ? ', wearing ' + c.tenue : ''}`).join('. ') + '.';
  if (dec) t += ` Setting: ${dec.desc}.`; if (look) t += ` Lighting: ${look.desc}.`;
  return t + ' ' + REAL;
}
const motionPrompt = s => `${CAMS[s.camera] || s.camera}. ${s.desc || ''}. Natural realistic human motion, subtle micro-expressions, cinematic, stable faces and hands.`;
const portraitPrompt = c => `Photorealistic portrait photo of ${c.desc}${c.tenue ? ', wearing ' + c.tenue : ''}. Neutral background, soft daylight, front view and three-quarter view, sharp focus on the eyes, realistic skin texture with pores, 85mm lens. Abidjan, Côte d'Ivoire.`;
function claudeRequest(p) {
  const b = p.brief, n = Math.max(2, Math.round((+b.duree || 30) / 5)), chars = (b.chars || []).map(charById).filter(Boolean);
  return `Tu es réalisateur à Abidjan pour l'agence AM Digital. Découpe ce brief en ${n} plans d'environ 5 secondes pour un(e) ${TYPES[p.type].toLowerCase()} au format ${p.format}.

Brief :
- Sujet / produit : ${b.produit}
- Objectif : ${b.objectif}
- Cible : ${b.cible}
- Message clé : ${b.message}
- Ton : ${b.ton}
- Lieu : ${b.lieu}
- Appel à l'action : ${b.cta}
- Personnages : ${chars.map(c => c.name + ' (' + c.age + ')').join(', ') || 'à proposer'}

Règles : personnes et lieux ivoiriens, rendu réaliste, aucun chiffre ni témoignage inventé, une marque fictive est un « concept de démonstration », répliques courtes en français ivoirien naturel.
Valeurs autorisées — decor : ${allDecors().map(d => d.id).join(', ')} ; look : ${LOOKS.map(l => l.id).join(', ')} ; camera : ${Object.keys(CAMS).join(' | ')} ; chars : ${chars.map(c => c.name).join(', ') || 'aucun'}.

Réponds UNIQUEMENT avec ce JSON, sans texte autour :
{"shots":[{"beat":"","desc":"","camera":"","decor":"","look":"","chars":[""],"dialogue":"","overlay":"","duration":5}]}`;
}
function importClaude(p, txt) {
  const a = txt.indexOf('{'), z = txt.lastIndexOf('}'); if (a < 0) throw new Error('aucun JSON trouvé');
  const j = JSON.parse(txt.slice(a, z + 1)); if (!Array.isArray(j.shots)) throw new Error('liste "shots" absente');
  return j.shots.map(s => newShot({
    beat: s.beat || 'Plan', desc: s.desc || '', camera: CAMS[s.camera] ? s.camera : 'Plan fixe',
    decor: decorById(s.decor) ? s.decor : p.brief.decor, look: LOOKS.some(l => l.id === s.look) ? s.look : p.brief.look,
    chars: (s.chars || []).map(n => S.data.characters.find(c => c.name.toLowerCase() === String(n).toLowerCase())).filter(Boolean).map(c => c.id),
    dialogue: s.dialogue || '', overlay: s.overlay || '', duration: Math.min(15, Math.max(2, +s.duration || 5))
  }));
}

/* ---------- Petits morceaux d'interface ---------- */
const opt = (v, label, cur) => `<option value="${esc(v)}"${String(v) === String(cur) ? ' selected' : ''}>${esc(label)}</option>`;
const sel = (path, list, cur) => `<select data-p="${path}">${list.map(([v, l]) => opt(v, l, cur)).join('')}</select>`;
const fld = (label, path, val, o = {}) => `<label class="${o.wide ? 'wide' : ''}">${label}${o.area ? `<textarea data-p="${path}" rows="${o.rows || 3}" placeholder="${esc(o.ph || '')}">${esc(val)}</textarea>` : `<input data-p="${path}" ${o.num ? 'type="number" min="1" max="15"' : ''} value="${esc(val)}" placeholder="${esc(o.ph || '')}">`}</label>`;
const thumb = (id, cls = '') => `<div class="thumb ${cls}" data-m="${id || ''}">${id ? 'Chargement…' : 'Aucun média'}</div>`;
const ratioCls = f => f === '16:9' ? 'r169' : f === '1:1' ? 'r11' : '';
const ready = p => p.shots.filter(s => s.media).length;
async function hydrate() {
  for (const el of $$('[data-m]')) {
    const id = el.dataset.m; if (!id) continue; const u = await mediaURL(id), m = S.data.media[id];
    if (!u || !m) { el.textContent = 'Média introuvable'; continue; }
    el.innerHTML = m.type === 'video' ? `<video src="${u}" muted loop playsinline controls></video>` : m.type === 'audio' ? `<audio src="${u}" controls></audio>` : `<img src="${u}" alt="${esc(m.name)}">`;
  }
}

/* ---------- Vues ---------- */
const V = {};
V.accueil = () => {
  const P = S.data.projects, shots = P.flatMap(p => p.shots), r = shots.filter(s => s.media).length;
  return `<header class="hero"><div class="eyebrow">AM Digital · atelier interne</div><h1>AM Studio <span>Vidéo IA</span></h1>
  <p>Du brief à la vidéo prête pour Reels, TikTok et YouTube, sans abonnement. On prépare tout ici, on génère les plans dans les outils gratuits avec des prompts déjà optimisés, puis on monte et on exporte ici.</p>
  <div class="row"><button class="btn gold" onclick="A.newProject()">Nouveau projet</button><a class="btn" href="#outils">Voir les outils gratuits</a></div></header>
  <div class="stats"><div class="stat"><b>${P.length}</b><span>Projets</span></div><div class="stat"><b>${S.data.characters.length}</b><span>Personnages au casting</span></div><div class="stat"><b>${r} / ${shots.length}</b><span>Plans prêts</span></div><div class="stat"><b>0 FCFA</b><span>Dépensé</span></div></div>
  <h2>Le parcours</h2><ol class="steps">
  <li><b>Brief</b>Le client, le produit, le ton, la durée.</li><li><b>Storyboard</b>Découpage automatique ou par Claude.</li><li><b>Plans</b>Prompts réalistes à coller dans l'outil gratuit.</li><li><b>Voix</b>ElevenLabs ou enregistrement maison.</li><li><b>Montage</b>Sous-titres, logo, carton final aux couleurs.</li><li><b>Export</b>9:16, 1:1 et 16:9, plus les sous-titres.</li></ol>
  <h2>Projets récents</h2>${P.length ? `<div class="cards">${P.slice().reverse().slice(0, 6).map(projCard).join('')}</div>` : '<div class="empty">Aucun projet. Cliquez sur « Nouveau projet ».</div>'}`;
};
const projCard = p => `<a class="card" href="#projet/${p.id}/brief"><small>${esc(p.client || 'Sans client')} · ${TYPES[p.type]}</small><b>${esc(p.title)}</b><span class="chip ${ready(p) === p.shots.length && p.shots.length ? 'ok' : 'todo'}">${ready(p)} / ${p.shots.length} plans prêts</span><span class="meta">${p.format} · ${p.brief.duree} s</span></a>`;
V.projets = () => `<h1>Projets</h1><div class="row" style="margin:16px 0"><button class="btn gold" onclick="A.newProject()">Nouveau projet</button></div>
  ${S.data.projects.length ? `<div class="cards">${S.data.projects.map(projCard).join('')}</div>` : '<div class="empty">Aucun projet pour l’instant.</div>'}`;

V.projet = (id, tab = 'brief') => {
  const p = proj(id); if (!p) return '<div class="empty">Projet introuvable. <a href="#projets">Retour aux projets</a></div>';
  A.cur = p;
  const tabs = [['brief', 'Brief'], ['storyboard', 'Storyboard'], ['plans', 'Plans & prompts'], ['voix', 'Voix'], ['montage', 'Montage & export']];
  return `<div data-root="p"><div class="eyebrow">${esc(p.client || 'Sans client')} · ${TYPES[p.type]}</div><h1>${esc(p.title)}</h1>
  <nav class="tabs">${tabs.map(([k, l]) => `<a href="#projet/${p.id}/${k}" class="${k === tab ? 'on' : ''}">${l}</a>`).join('')}</nav>${(T[tab] || T.brief)(p)}</div>`;
};
const T = {};
T.brief = p => {
  const b = p.brief;
  return `<div class="grid">
  ${fld('Titre du projet', 'title', p.title)}${fld('Client', 'client', p.client, { ph: 'Nom du client ou « Concept de démonstration »' })}
  <label>Type${sel('type', Object.entries(TYPES), p.type)}</label><label>Format principal${sel('format', FMTS.map(f => [f, f]), p.format)}</label>
  <label>Durée totale${sel('brief.duree', [15, 30, 45, 60, 90, 180].map(d => [d, d + ' secondes']), b.duree)}</label>
  <label>Décor principal${sel('brief.decor', allDecors().map(d => [d.id, d.name]), b.decor)}</label><label>Lumière${sel('brief.look', LOOKS.map(l => [l.id, l.name]), b.look)}</label>
  ${fld('Sujet / produit', 'brief.produit', b.produit, { wide: 1 })}${fld('Objectif', 'brief.objectif', b.objectif)}${fld('Cible', 'brief.cible', b.cible)}
  ${fld('Message clé', 'brief.message', b.message, { wide: 1 })}${fld('Ton', 'brief.ton', b.ton, { ph: 'chaleureux, drôle, premium…' })}${fld('Lieu', 'brief.lieu', b.lieu)}${fld("Appel à l'action", 'brief.cta', b.cta, { wide: 1 })}
  <div class="wide"><label>Personnages du projet</label><div class="checks">${S.data.characters.map(c => `<label class="inline"><input type="checkbox" data-arr="brief.chars" value="${c.id}"${b.chars.includes(c.id) ? ' checked' : ''}>${esc(c.name)}</label>`).join('') || '<span class="meta">Ajoutez des personnages dans Casting.</span>'}</div></div></div>
  <h2>Créer le storyboard</h2>
  <div class="cards"><div class="card"><h3>Découpage automatique</h3><p class="meta">Instantané, à partir des champs ci-dessus. Remplace les plans actuels.</p><button class="btn gold" onclick="A.auto()">Découper en plans</button></div>
  <div class="card"><h3>Découpage par Claude</h3><p class="meta">Plus créatif, gratuit avec votre abonnement Claude : copiez la demande, collez-la dans Claude, puis collez sa réponse ici.</p>
  <button class="btn" onclick="A.copyText(claudeRequest(A.cur),'Demande copiée : collez-la dans Claude')">Copier la demande pour Claude</button>
  <textarea id="cjson" rows="4" placeholder="Collez ici la réponse JSON de Claude"></textarea><button class="btn gold" onclick="A.importC()">Importer la réponse</button></div></div>
  <div class="row" style="margin-top:28px"><button class="btn danger" onclick="A.delProject()">Supprimer ce projet</button></div>`;
};
T.storyboard = p => `<div class="row" style="margin-bottom:14px"><button class="btn gold" onclick="A.addShot()">Ajouter un plan</button><span class="meta">Durée totale : ${p.shots.reduce((a, s) => a + (+s.duration || 0), 0)} s · ${ready(p)} / ${p.shots.length} plans avec image ou vidéo</span></div>
  ${p.shots.length ? `<div class="shots">${p.shots.map((s, i) => `<article class="shot">
  <div class="shot-head"><b><span>Plan ${i + 1}</span> · ${esc(s.beat)}</b><div class="row"><button class="btn sm" onclick="A.mv(${i},-1)" aria-label="Monter">↑</button><button class="btn sm" onclick="A.mv(${i},1)" aria-label="Descendre">↓</button><button class="btn sm danger" onclick="A.delShot(${i})">Supprimer</button></div></div>
  <div>${thumb(s.media, ratioCls(p.format))}<label style="margin-top:8px">Image ou clip du plan<input type="file" accept="image/*,video/*" data-file="shot:${i}"></label></div>
  <div class="grid">${fld('Étape', `shots.${i}.beat`, s.beat)}${fld('Durée (s)', `shots.${i}.duration`, s.duration, { num: 1 })}
  ${fld('Ce qu’on voit', `shots.${i}.desc`, s.desc, { area: 1, wide: 1 })}
  <label>Caméra${sel(`shots.${i}.camera`, Object.keys(CAMS).map(k => [k, k]), s.camera)}</label><label>Décor${sel(`shots.${i}.decor`, allDecors().map(d => [d.id, d.name]), s.decor)}</label><label>Lumière${sel(`shots.${i}.look`, LOOKS.map(l => [l.id, l.name]), s.look)}</label>
  <div class="wide"><label>Personnages</label><div class="checks">${S.data.characters.map(c => `<label class="inline"><input type="checkbox" data-arr="shots.${i}.chars" value="${c.id}"${s.chars.includes(c.id) ? ' checked' : ''}>${esc(c.name)}</label>`).join('')}</div></div>
  ${fld('Réplique (sous-titre)', `shots.${i}.dialogue`, s.dialogue)}${fld('Texte à l’écran', `shots.${i}.overlay`, s.overlay)}</div></article>`).join('')}</div>` : '<div class="empty">Pas encore de plans. Utilisez le découpage dans l’onglet Brief.</div>'}`;
T.plans = p => {
  const tool = TOOLS.find(t => t.id === A.tool) || TOOLS[0];
  return `${tool.id === 'open' ? `<p class="callout">Génération directe et gratuite avec des modèles open source : 1. l'image du plan (FLUX.1 Krea), 2. son animation en vidéo (Wan 2.2). Le quota gratuit de Hugging Face est limité chaque jour : un jeton gratuit (onglet Sauvegarde) l'augmente. Quand il est épuisé, passez sur Dreamina ou Meta AI avec le même prompt.</p>` : ''}<p class="callout"${tool.id === 'open' ? ' hidden' : ''}>1. Choisissez l'outil gratuit. 2. Copiez le prompt du plan et collez-le dans l'outil (avec les photos du casting si l'outil accepte des références). 3. Téléchargez le clip obtenu et importez-le ici. Les offres gratuites changent souvent : vérifiez vos crédits du jour dans chaque outil.</p>
  <div class="row" style="margin-bottom:14px"><label style="min-width:240px">Outil${`<select onchange="A.tool=this.value;A.render()">${TOOLS.map(t => opt(t.id, t.name, tool.id)).join('')}</select>`}</label><a class="btn" href="${tool.url}" target="_blank" rel="noopener">Ouvrir ${esc(tool.name)}</a><span class="meta">${esc(tool.note)}</span></div>
  ${tool.id === 'open' ? `<div class="row" style="margin-bottom:14px"><button class="btn gold" onclick="A.genAll()">Générer tous les plans manquants</button><span class="meta">Chaque plan : environ 1 à 3 minutes. Gardez l’onglet ouvert.</span></div>` : ''}
  <div class="shots">${p.shots.map((s, i) => { const cs = s.chars.map(charById).filter(Boolean); if (tool.id === 'open') return `<article class="shot"><div class="shot-head"><b><span>Plan ${i + 1}</span> · ${esc(s.beat)} · ${s.duration} s</b><span class="chip ${S.data.media[s.media]?.type === 'video' ? 'ok' : 'todo'}">${S.data.media[s.media]?.type === 'video' ? 'Vidéo prête' : s.still ? 'Image prête' : 'À générer'}</span></div>
  <div>${thumb(s.media, ratioCls(p.format))}</div>
  <div style="display:flex;flex-direction:column;gap:10px;min-width:0"><div class="pbox"><span class="meta">Image (FLUX.1 Krea)</span><textarea readonly>${esc(imagePrompt(p, s))}</textarea></div><div class="pbox"><span class="meta">Mouvement (Wan 2.2)</span><textarea readonly style="min-height:50px">${esc(motionPrompt(s))}</textarea></div>
  <div class="grid"><label>Image source<select data-p="shots.${i}.still">${opt(s.still || '', s.still ? 'Image actuelle' : '— aucune —', s.still || '')}${[...new Set(p.shots.map(o => o.still).filter(x => x && x !== s.still))].map(id => opt(id, 'Image du plan ' + (p.shots.findIndex(o => o.still === id) + 1), '')).join('')}</select></label><label>Cadrage AM Motion${sel(`shots.${i}.crop`, (window.AMM ? AMM.CROP_LABELS : [['', 'Image entière']]), s.crop || '')}</label><label>Caméra${sel(`shots.${i}.camera`, Object.keys(CAMS).map(k => [k, k]), s.camera)}</label><label class="inline"><input type="checkbox" data-p="shots.${i}.sharp"${s.sharp ? ' checked' : ''}>Netteté x2 (Swin2SR, +1 min)</label></div>
  <div class="row"><button class="btn" data-gen="${i}" onclick="A.genImage(${i})">1. Générer l’image</button><button class="btn gold" data-gen="${i}" onclick="A.genMotion(${i})">2. Animer avec AM Motion (illimité)</button></div>
  <div class="row"><span class="meta">Options avec quota Hugging Face :</span><button class="btn sm" data-gen="${i}" onclick="A.genVideo(${i})">Animer avec Wan 2.2</button><button class="btn sm" data-gen="${i}" onclick="A.genT2V(${i})">Vidéo directe LTX</button></div>
  <span class="meta" id="st-${i}"></span><label>Ou importer un clip<input type="file" accept="video/*,image/*" data-file="shot:${i}"></label></div></article>`; return `<article class="shot"><div class="shot-head"><b><span>Plan ${i + 1}</span> · ${esc(s.beat)} · ${s.duration} s</b><span class="chip ${s.media ? 'ok' : 'todo'}">${s.media ? 'Prêt' : 'À générer'}</span></div>
  <div>${thumb(s.media, ratioCls(p.format))}<label style="margin-top:8px">Importer le clip généré<input type="file" accept="video/*,image/*" data-file="shot:${i}"></label></div>
  <div style="display:flex;flex-direction:column;gap:10px;min-width:0"><div class="pbox"><textarea readonly>${esc(shotPrompt(p, s, tool.id))}</textarea><div class="row"><button class="btn gold sm" onclick="A.copyBox(this)">Copier le prompt</button></div></div>
  ${tool.id === 'kling' ? `<div class="pbox"><textarea readonly style="min-height:50px">${esc(NEG)}</textarea><div class="row"><button class="btn sm" onclick="A.copyBox(this)">Copier le prompt négatif</button></div></div>` : ''}
  ${cs.length ? `<div><span class="meta">Photos de référence à joindre :</span><div class="pics">${cs.flatMap(c => c.photos).map(id => thumb(id)).join('') || '<span class="meta">aucune photo au casting</span>'}</div></div>` : ''}</div></article>`; }).join('') || '<div class="empty">Aucun plan.</div>'}</div>`;
};
T.voix = p => {
  const v = p.vox || (p.vox = { voice: 'pierre', speed: .95, timbre: .93, pause: .35, delay: .5 });
  const voices = window.VOX ? Object.entries(VOX.VOICES).map(([k, x]) => [k, `${x.label} (${x.lic})`]) : [['pierre', 'Pierre']];
  return `<div class="panel" style="margin-bottom:20px"><h3>Voix off open source · illimitée</h3>
  <p class="meta">Piper (open source) tourne dans votre navigateur : aucune limite, aucun compte. Écrivez une phrase par ligne. « Aya : texte » fait parler Aya avec la voix choisie dans son casting.</p>
  <div class="grid"><label>Voix du narrateur${sel('vox.voice', voices, v.voice)}</label>
  <label>Vitesse<input type="range" min=".75" max="1.2" step=".01" data-p="vox.speed" value="${v.speed}"></label>
  <label>Timbre (plus grave ←)<input type="range" min=".85" max="1.05" step=".01" data-p="vox.timbre" value="${v.timbre}"></label>
  <label>Pause entre phrases (s)<input type="range" min=".1" max="1" step=".05" data-p="vox.pause" value="${v.pause}"></label>
  <label>Début de la voix (s)<input type="range" min="0" max="3" step=".1" data-p="vox.delay" value="${v.delay}"></label>
  <label class="wide">Prononciations (une par ligne : mot = façon de le dire)<textarea data-p="vox.pron" rows="2" placeholder="Wôrô = Wo-ro">${esc(v.pron || '')}</textarea></label></div>
  <div class="row"><button class="btn gold" id="voxbtn" onclick="A.genVoice()">Générer la voix off</button><span class="meta" id="voxst"></span></div></div>
  <div class="mont"><div class="panel"><h3>Texte de la voix off</h3>
  <textarea data-p="voiceText" rows="8" placeholder="Texte lu par la voix off">${esc(p.voiceText)}</textarea>
  <div class="row"><button class="btn" onclick="A.voiceFromShots()">Reprendre les répliques des plans</button><button class="btn" onclick="A.copyText(A.cur.voiceText,'Texte copié')">Copier le texte</button><a class="btn" href="https://elevenlabs.io/app/speech-synthesis" target="_blank" rel="noopener">Ouvrir ElevenLabs</a></div>
  <p class="meta">Autres choix : ElevenLabs (voix Bass) quand le compte est actif, ou une vraie voix enregistrée au micro. Jamais de voix clonée sans accord écrit.</p></div>
  <div class="panel"><h3>Piste voix du projet</h3>${thumb(p.voice)}<label>Importer un fichier audio (MP3, WAV…)<input type="file" accept="audio/*" data-file="voice"></label>
  <div class="row"><button class="btn" id="recbtn" onclick="A.rec()">Enregistrer au micro</button>${p.voice ? '<button class="btn danger" onclick="A.cur.voice=null;save();A.render()">Retirer</button>' : ''}</div></div></div>`;
};
T.montage = p => `<div class="mont"><div class="stage"><canvas id="mcv"></canvas></div>
  <div class="panel"><h3>Réglages</h3>
  <label>Format de sortie${sel('format', FMTS.map(f => [f, f + (f === '9:16' ? ' · Reels / TikTok' : f === '16:9' ? ' · YouTube / TV' : ' · Feed')]), p.format)}</label>
  <label class="inline"><input type="checkbox" data-p="mont.subs"${p.mont.subs ? ' checked' : ''}>Sous-titres incrustés (répliques)</label>
  <label class="inline"><input type="checkbox" data-p="mont.clipAudio"${p.mont.clipAudio ? ' checked' : ''}>Garder le son des clips</label>
  <label class="inline"><input type="checkbox" data-p="mont.endCard"${p.mont.endCard ? ' checked' : ''}>Carton final aux couleurs AM</label>
  ${fld('Titre du carton final', 'mont.endTitle', p.mont.endTitle)}${fld('Sous-titre du carton', 'mont.endSub', p.mont.endSub)}
  <label>Logo (PNG transparent)<input type="file" accept="image/*" data-file="logo"></label>
  <div class="bar"><i id="mbar"></i></div><span class="meta" id="mstat">Les plans sans clip apparaissent en carte texte (animatique).</span>
  <div class="row"><button class="btn" onclick="A.preview()">Aperçu</button><button class="btn gold" onclick="A.exportVid()">Exporter la vidéo</button><button class="btn" onclick="M.stop()">Arrêter</button></div>
  <div class="row"><button class="btn sm" onclick="A.srt()">Sous-titres .srt</button></div>
  <p class="meta">L'export se fait en temps réel : gardez cet onglet ouvert et visible. Musique : ajoutez-la dans TikTok / Instagram, jamais dans le fichier.</p></div></div>`;

V.casting = () => `<h1>Casting</h1><p>Chaque fiche garde le même visage, la même tenue et la même voix d'un plan à l'autre. Décrivez le physique en anglais pour de meilleurs résultats et ajoutez 3 à 6 photos de référence (générées ou réelles avec autorisation écrite).</p>
  <div class="row" style="margin:14px 0"><button class="btn gold" onclick="A.addChar()">Ajouter un personnage</button></div>
  <div class="cards">${S.data.characters.map(c => `<div class="card" data-root="c:${c.id}">
  <div class="grid">${fld('Nom', 'name', c.name)}${fld('Âge', 'age', c.age)}</div>${fld('Physique (anglais conseillé)', 'desc', c.desc, { area: 1 })}${fld('Tenue', 'tenue', c.tenue)}${fld('Voix (notes)', 'voix', c.voix)}<label>Voix open source${sel('vox', [['', 'Celle du narrateur']].concat(window.VOX ? Object.entries(VOX.VOICES).map(([k, x]) => [k, x.label]) : []), c.vox || '')}</label>
  <div class="pics">${c.photos.map(id => thumb(id)).join('')}</div><label>Ajouter des photos<input type="file" accept="image/*" multiple data-file="char:${c.id}"></label>
  <div class="row"><button class="btn sm" onclick="A.copyText(portraitPrompt(charById('${c.id}')),'Prompt de portrait copié')">Copier un prompt de portrait</button><button class="btn sm danger" onclick="A.delChar('${c.id}')">Supprimer</button></div></div>`).join('')}</div>`;
V.decors = () => `<h1>Décors &amp; lumières</h1><p>Ces descriptions sont ajoutées automatiquement aux prompts de chaque plan.</p>
  <h2>Décors d'Abidjan</h2><div class="scroll"><table><thead><tr><th>Décor</th><th>Description envoyée au modèle</th></tr></thead><tbody>${DECORS.map(d => `<tr><td><b>${esc(d.name)}</b></td><td class="meta">${esc(d.desc)}</td></tr>`).join('')}</tbody></table></div>
  <h2>Vos décors</h2><div class="row" style="margin-bottom:12px"><button class="btn gold" onclick="A.addDecor()">Ajouter un décor</button></div>
  <div class="cards">${S.data.decors.map(d => `<div class="card" data-root="d:${d.id}">${fld('Nom', 'name', d.name)}${fld('Description (anglais conseillé)', 'desc', d.desc, { area: 1 })}<button class="btn sm danger" onclick="A.delDecor('${d.id}')">Supprimer</button></div>`).join('') || '<div class="empty">Aucun décor personnalisé.</div>'}</div>
  <h2>Lumières</h2><div class="scroll"><table><tbody>${LOOKS.map(l => `<tr><td><b>${esc(l.name)}</b></td><td class="meta">${esc(l.desc)}</td></tr>`).join('')}</tbody></table></div>`;
V.outils = () => `<h1>Outils gratuits</h1><p>Le logiciel prépare les prompts ; la génération se fait dans ces outils avec leurs crédits gratuits. Les offres changent souvent : vérifiez-les dans chaque outil avant de promettre un délai à un client.</p>
  <div class="scroll"><table><thead><tr><th>Outil</th><th>Usage conseillé</th><th></th></tr></thead><tbody>${TOOLS.map(t => `<tr><td><b>${esc(t.name)}</b></td><td>${esc(t.note)}</td><td><a class="btn sm" href="${t.url}" target="_blank" rel="noopener">Ouvrir</a></td></tr>`).join('')}
  <tr><td><b>ElevenLabs</b></td><td>Seul outil de voix IA autorisé par l'agence.</td><td><a class="btn sm" href="https://elevenlabs.io" target="_blank" rel="noopener">Ouvrir</a></td></tr>
  <tr><td><b>Meshy · Mixamo</b></td><td>Personnages 3D et animations à importer dans le Studio 3D (fichiers GLB).</td><td><a class="btn sm" href="https://www.meshy.ai" target="_blank" rel="noopener">Meshy</a> <a class="btn sm" href="https://www.mixamo.com" target="_blank" rel="noopener">Mixamo</a></td></tr></tbody></table></div>
  <h2>Briques open source intégrées</h2><p>Sélectionnées sur GitHub le 10/11/2026 : utilisables directement dans le navigateur, sans rien installer, licences compatibles avec un usage commercial.</p>
  <div class="scroll"><table><thead><tr><th>Dépôt GitHub</th><th>Rôle dans AM Studio</th><th>Licence</th></tr></thead><tbody>${[
    ['huggingface/transformers.js', 'Moteur d’IA dans le navigateur (profondeur, netteté)', 'Apache 2.0'],
    ['DepthAnything/Depth-Anything-V2', 'Relief de l’image pour AM Motion (modèle Small)', 'Apache 2.0'],
    ['mv-lab/swin2sr', 'Netteté x2 des gros plans', 'Apache 2.0'],
    ['rhasspy/piper + diffusionstudio/vits-web', 'Voix off française hors ligne (Pierre, Gilles, Siwis, Jessica)', 'MIT · voix CC-BY / CC-BY-SA / CC0'],
    ['Vanilagy/mp4-muxer', 'Export MP4 H.264 image par image', 'MIT'],
    ['mrdoob/three.js', 'AM Motion et Studio 3D', 'MIT'],
    ['gradio-app/gradio (client)', 'Accès aux modèles hébergés : FLUX.1 Krea, Wan 2.2, LTX-Video', 'Apache 2.0'],
    ['Wan-Video/Wan2.2 · Lightricks/LTX-Video', 'Vidéo IA avec vrais gestes (quota Hugging Face)', 'Apache 2.0']
  ].map(([r, u, l]) => `<tr><td><a href="https://github.com/${r.split(' ')[0]}" target="_blank" rel="noopener">${esc(r)}</a></td><td>${esc(u)}</td><td class="meta">${esc(l)}</td></tr>`).join('')}</tbody></table></div>
  <p class="meta">Mentions à garder dans les crédits d'un projet client qui utilise une voix CC-BY : « Voix : Piper, jeu de données SIWIS / UPMC ».</p>
  <h2>Règles à respecter</h2><ul><li>Aucun visage ni voix d'une personne réelle sans autorisation écrite.</li><li>Ne jamais faire dire à une vraie personne ce qu'elle n'a pas dit.</li><li>Pas d'imitation de film, de marque ou de personnage existant.</li><li>Signaler « contenu généré par IA » sur Meta et TikTok pour les vidéos réalistes.</li><li>Marque fictive : toujours « concept de démonstration ».</li></ul>`;
V.reglages = () => `<h1>Sauvegarde</h1><p>Les projets sont gardés dans ce navigateur, sur cet ordinateur. Faites une sauvegarde régulière (textes, prompts et réglages ; les vidéos restent dans vos dossiers).</p>
  <div class="row" style="margin:16px 0"><button class="btn gold" onclick="A.backup()">Télécharger la sauvegarde</button><label>Restaurer une sauvegarde<input type="file" accept="application/json,.json" data-file="backup"></label></div>
  <p class="meta">Utilisez toujours le même navigateur (Chrome ou Edge conseillés) pour retrouver vos projets.</p>
  <h2>Moteur open source</h2><p>Images : FLUX.1 Krea [dev]. Vidéos : Wan 2.2 (image → vidéo) et LTX-Video (texte → vidéo). Ces modèles ouverts tournent gratuitement sur Hugging Face. Sans compte, le quota quotidien est limité ; avec un compte Hugging Face gratuit et un jeton de lecture, il est plus large.</p>
  <div class="row"><label style="min-width:320px">Jeton Hugging Face (facultatif, gardé sur cet ordinateur)<input type="password" id="hftok" autocomplete="off" placeholder="hf_…" value="${esc((() => { try { return localStorage.getItem('amstudio-hf') || ''; } catch (e) { return ''; } })())}"></label><button class="btn" onclick="try{localStorage.setItem('amstudio-hf',$('#hftok').value.trim());toast('Jeton enregistré, rechargez la page')}catch(e){}">Enregistrer</button><a class="btn" href="https://huggingface.co/settings/tokens" target="_blank" rel="noopener">Créer un jeton</a></div>`;
V.studio3d = () => D3.view();

/* ---------- Actions ---------- */
const A = {
  cur: null, tool: 'open',
  async engine() {
    for (let k = 0; k < 40 && !(window.OS && (OS.image || OS.error)); k++) await new Promise(r => setTimeout(r, 250));
    if (!window.OS || OS.error) throw new Error((window.OS && OS.error) || 'moteur open source indisponible');
  },
  async runGen(i, label, job) {
    const p = A.cur, st = $('#st-' + i), btns = $$(`[data-gen="${i}"]`), t0 = Date.now();
    btns.forEach(b => b.disabled = true); if (st) st.dataset.m = '';
    const tick = setInterval(() => st && (st.textContent = `${st.dataset.m || label}… ${Math.round((Date.now() - t0) / 1000)} s`), 1000);
    try { if (!/AM Motion/.test(label)) await A.engine(); await job(p, p.shots[i]); S.save(); toast(`Plan ${i + 1} : ${label.toLowerCase()} terminé`); return true; }
    catch (e) { toast(`Plan ${i + 1} : ${e.message}`); if (st) st.textContent = 'Échec : ' + e.message; return false; }
    finally { clearInterval(tick); btns.forEach(b => b.disabled = false); if (A.cur === p && location.hash.endsWith('/plans') && !A._all) A.render(); }
  },
  genImage(i) {
    return A.runGen(i, 'Image en cours', async (p, s) => {
      let b;
      try { b = await OS.image(imagePrompt(p, s), p.format); }
      catch (e) { throw new Error(e.message + ' En attendant : réutilisez l’image d’un autre plan (menu « Image source ») ou importez une image de Meta AI, Dreamina ou Canva.'); }
      s.still = await storeBlob(b, 'image FLUX.1 Krea'); if (S.data.media[s.media]?.type !== 'video') s.media = s.still;
    });
  },
  async genMotion(i) {
    const s0 = A.cur.shots[i], src = s0.still || (S.data.media[s0.media]?.type === 'image' ? s0.media : null);
    if (!src && !(await A.genImage(i))) return false;
    return A.runGen(i, 'AM Motion : tournage', async (p, s) => {
      const st = $('#st-' + i), mount = $$('.shot')[i]?.querySelector('.thumb');
      const blob = await AMM.render(await DB.get(s.still || s.media), { secs: +s.duration || 5, format: p.format, camera: s.camera, look: s.look, crop: s.crop, sharpen: !!s.sharp, mount, status: m => st && (st.dataset.m = m) });
      s.media = await storeBlob(blob, 'vidéo AM Motion');
    });
  },
  async genVideo(i) {
    const s = A.cur.shots[i]; if (!s.still && !(await A.genImage(i))) return false;
    return A.runGen(i, 'Vidéo en cours', async (p, s) => { s.media = await storeBlob(await OS.animate(await DB.get(s.still), motionPrompt(s), +s.duration || 5), 'vidéo Wan 2.2'); });
  },
  genT2V(i) { return A.runGen(i, 'Vidéo directe en cours', async (p, s) => { s.media = await storeBlob(await OS.t2v(shotPrompt(p, s, 'open'), p.format, +s.duration || 5), 'vidéo LTX'); }); },
  async genAll() {
    A._all = true; const p = A.cur;
    for (let i = 0; i < p.shots.length; i++) { if (S.data.media[p.shots[i].media]?.type === 'video') continue; if (!(await A.genMotion(i))) break; }
    A._all = false; A.render();
  },
  render() {
    const [v, id, tab] = (location.hash.slice(1) || 'accueil').split('/');
    if (v !== 'studio3d' && window.D3) D3.unmount();
    $$('#side nav a').forEach(a => a.classList.toggle('on', a.dataset.nav === v || (v === 'projet' && a.dataset.nav === 'projets')));
    A.cur = null;
    $('#view').innerHTML = v === 'projet' ? V.projet(id, tab) : (V[v] || V.accueil)();
    hydrate(); if (v === 'studio3d') D3.mount(); if (v === 'projet' && tab === 'montage') M.poster(A.cur, $('#mcv'));
  },
  newProject() { const p = newProject(); S.data.projects.push(p); S.save(); location.hash = `projet/${p.id}/brief`; },
  delProject() { if (!confirm('Supprimer ce projet ?')) return; S.data.projects = S.data.projects.filter(p => p !== A.cur); S.save(); location.hash = 'projets'; },
  auto() { const p = A.cur; if (p.shots.some(s => s.media) && !confirm('Remplacer les plans actuels (et leurs clips) ?')) return; p.shots = autoShots(p); S.save(); toast(p.shots.length + ' plans créés'); location.hash = `projet/${p.id}/storyboard`; },
  importC() { try { const sh = importClaude(A.cur, $('#cjson').value); A.cur.shots = sh; S.save(); toast(sh.length + ' plans importés'); location.hash = `projet/${A.cur.id}/storyboard`; } catch (e) { toast('Réponse illisible : ' + e.message); } },
  addShot() { const b = A.cur.brief; A.cur.shots.push(newShot({ decor: b.decor, look: b.look, chars: [...b.chars] })); S.save(); A.render(); },
  delShot(i) { A.cur.shots.splice(i, 1); S.save(); A.render(); },
  mv(i, d) { const s = A.cur.shots, j = i + d; if (j < 0 || j >= s.length) return; [s[i], s[j]] = [s[j], s[i]]; S.save(); A.render(); },
  async genVoice() {
    const p = A.cur, v = p.vox, st = $('#voxst'), b = $('#voxbtn'); b.disabled = true; const t0 = Date.now();
    const cast = {}; S.data.characters.forEach(c => { if (c.vox) cast[c.name.toLowerCase()] = c.vox; });
    try {
      const pron = {}; String(v.pron || '').split('\n').forEach(l => { const [a, b] = l.split('='); if (a && b && a.trim()) pron[a.trim()] = b.trim(); });
      const blob = await VOX.speak(p.voiceText, { pron, voice: v.voice, speed: +v.speed, timbre: +v.timbre, pause: +v.pause, cast, status: m => st.textContent = m + '…' });
      p.voice = await storeBlob(blob, 'voix Piper'); S.save(); toast(`Voix off prête (${Math.round((Date.now() - t0) / 1000)} s)`); A.render();
    } catch (e) { st.textContent = 'Échec : ' + e.message; b.disabled = false; }
  },
  voiceFromShots() { A.cur.voiceText = A.cur.shots.map(s => s.dialogue).filter(Boolean).join('\n'); S.save(); A.render(); },
  addChar() { S.data.characters.push({ id: 'c' + uid(), name: 'Nouveau personnage', age: '', desc: 'Ivorian ', tenue: '', voix: '', photos: [] }); S.save(); A.render(); },
  delChar(id) { if (!confirm('Supprimer ce personnage ?')) return; S.data.characters = S.data.characters.filter(c => c.id !== id); S.save(); A.render(); },
  addDecor() { S.data.decors.push({ id: 'd' + uid(), name: 'Nouveau décor', desc: '' }); S.save(); A.render(); },
  delDecor(id) { S.data.decors = S.data.decors.filter(d => d.id !== id); S.save(); A.render(); },
  async copyText(t, msg = 'Copié') { try { await navigator.clipboard.writeText(t); toast(msg); } catch (e) { const ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); toast(msg); } },
  copyBox(btn) { A.copyText(btn.closest('.pbox').querySelector('textarea').value, 'Prompt copié'); },
  async rec() {
    const b = $('#recbtn');
    if (A._rec) { A._rec.stop(); return; }
    try {
      const st = await navigator.mediaDevices.getUserMedia({ audio: true }), r = new MediaRecorder(st), ch = [];
      r.ondataavailable = e => ch.push(e.data);
      r.onstop = async () => { st.getTracks().forEach(t => t.stop()); A._rec = null; const p = A.cur; p.voice = await storeBlob(new Blob(ch, { type: r.mimeType || 'audio/webm' }), 'voix-micro'); S.save(); toast('Voix enregistrée'); A.render(); };
      r.start(); A._rec = r; b.textContent = 'Arrêter l’enregistrement';
    } catch (e) { toast('Micro indisponible : ' + e.message); }
  },
  async preview() { const st = $('#mstat'); st.textContent = 'Lecture…'; await M.play(A.cur, $('#mcv'), { onProgress: k => $('#mbar').style.width = (k * 100) + '%' }); st.textContent = 'Aperçu terminé.'; },
  async exportVid() {
    const p = A.cur, st = $('#mstat'); st.textContent = 'Export en cours, ne changez pas d’onglet…';
    const blob = await M.play(p, $('#mcv'), { record: true, onProgress: k => $('#mbar').style.width = (k * 100) + '%' });
    if (!blob) { st.textContent = 'Export interrompu.'; return; }
    const ext = blob.type.includes('mp4') ? 'mp4' : 'webm';
    download(blob, `${slug(p.title)}-${p.format.replace(':', 'x')}.${ext}`);
    st.textContent = `Vidéo exportée (${ext.toUpperCase()}, ${(blob.size / 1e6).toFixed(1)} Mo).` + (ext === 'webm' ? ' Si une plateforme refuse le WebM, convertissez-le avec ffmpeg.' : '');
  },
  srt() { download(new Blob([M.srt(A.cur)], { type: 'text/plain' }), slug(A.cur.title) + '.srt'); },
  backup() { download(new Blob([JSON.stringify(S.data, null, 1)], { type: 'application/json' }), 'am-studio-sauvegarde-' + new Date().toISOString().slice(0, 10) + '.json'); },
  async attach(pid, idx, blob, name) { const p = proj(pid); if (!p || !p.shots[idx]) return toast('Plan introuvable'); p.shots[idx].media = await storeBlob(blob, name); S.save(); toast(`Ajouté au plan ${idx + 1} de « ${p.title} »`); }
};

/* ---------- Liaison des champs ---------- */
function rootObj(el) {
  const r = el.closest('[data-root]'); const k = r ? r.dataset.root : 'p';
  if (k === 'p') return A.cur; if (k.startsWith('c:')) return charById(k.slice(2)); if (k.startsWith('d:')) return S.data.decors.find(d => d.id === k.slice(2));
}
function setPath(o, path, v) { const ks = path.split('.'); const last = ks.pop(); for (const k of ks) o = o[k]; o[last] = v; }
function getPath(o, path) { return path.split('.').reduce((a, k) => a && a[k], o); }
function onField(e) {
  const el = e.target, o = el.dataset.p || el.dataset.arr ? rootObj(el) : null; if (!o) return;
  if (el.dataset.arr) { const arr = getPath(o, el.dataset.arr); const i = arr.indexOf(el.value); if (el.checked && i < 0) arr.push(el.value); if (!el.checked && i >= 0) arr.splice(i, 1); }
  else setPath(o, el.dataset.p, el.type === 'checkbox' ? el.checked : el.type === 'number' ? Math.max(1, Math.min(15, +el.value || 5)) : el.value);
  save();
  if (e.type === 'change' && el.tagName === 'SELECT' && el.dataset.p === 'format' && $('#mcv')) M.poster(A.cur, $('#mcv'));
}
document.addEventListener('input', e => { if (e.target.type !== 'checkbox' && e.target.type !== 'file') onField(e); });
document.addEventListener('change', async e => {
  const el = e.target;
  if (el.type === 'checkbox') return onField(e);
  if (el.tagName === 'SELECT') return onField(e);
  if (el.type !== 'file' || !el.dataset.file || !el.files.length) return;
  const [kind, arg] = el.dataset.file.split(':'), f = el.files[0];
  try {
    if (kind === 'shot') { A.cur.shots[+arg].media = await storeBlob(f, f.name); toast('Média ajouté au plan ' + (+arg + 1)); }
    else if (kind === 'voice') { A.cur.voice = await storeBlob(f, f.name); toast('Piste voix ajoutée'); }
    else if (kind === 'logo') { A.cur.logo = await storeBlob(f, f.name); toast('Logo ajouté'); }
    else if (kind === 'char') { const c = charById(arg); for (const x of el.files) c.photos.push(await storeBlob(x, x.name)); toast('Photos ajoutées'); }
    else if (kind === 'backup') { const d = JSON.parse(await f.text()); if (!d.projects) throw new Error('fichier non reconnu'); S.data = d; toast('Sauvegarde restaurée'); }
    else if (kind === 'glb') { return D3.importGLB(f); }
    S.save(); A.render();
  } catch (err) { toast('Erreur : ' + err.message); }
});
window.addEventListener('hashchange', A.render);
window.addEventListener('load', async () => {
  try { await DB.open(); } catch (e) { toast('Stockage des médias indisponible : ' + e.message); }
  S.load(); A.render();
});
