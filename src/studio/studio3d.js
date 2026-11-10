/* AM Studio Vidéo IA — Studio 3D : décors, silhouettes, modèles GLB, caméra libre, mouvement A→B, export vidéo et image. */
const D3 = { ready: false, active: false, objs: [], sel: -1, A: null, B: null, frame: '9:16', decor: 'rue', light: 'golden' };
const FR3 = { '9:16': [720, 1280], '1:1': [960, 960], '16:9': [1280, 720] };

D3.view = () => `<h1>Studio 3D</h1>
  <p>Composez une scène, placez la caméra où vous voulez, enregistrez un mouvement et exportez-le. La capture peut ensuite servir d'image de départ dans un outil vidéo (« 3D → réaliste ») ou de plan direct dans un projet.</p>
  <div class="d3"><div id="d3c"></div><div class="panel">
  <div class="grid"><label>Décor<select onchange="D3.setDecor(this.value)">${[['rue', 'Rue d’Abidjan'], ['maquis', 'Maquis'], ['salon', 'Salon'], ['studio', 'Studio aubergine']].map(([v, l]) => opt(v, l, D3.decor)).join('')}</select></label>
  <label>Lumière<select onchange="D3.setLight(this.value)">${[['golden', 'Fin de journée'], ['nuit', 'Nuit'], ['studio', 'Studio']].map(([v, l]) => opt(v, l, D3.light)).join('')}</select></label>
  <label>Cadre<select onchange="D3.setFrame(this.value)">${FMTS.map(f => opt(f, f, D3.frame)).join('')}</select></label></div>
  <h3>Personnages et objets</h3>
  <div class="row"><button class="btn sm" onclick="D3.addMannequin()">Ajouter une silhouette</button></div>
  <label>Importer un modèle 3D (.glb : Meshy, Mixamo…)<input type="file" accept=".glb,.gltf" data-file="glb"></label>
  <div id="d3list" class="checks"></div><div id="d3sel"></div>
  <h3>Caméra</h3><p class="meta">Clic gauche : tourner · molette : zoom · clic droit : déplacer.</p>
  <div class="row"><button class="btn sm" onclick="D3.mark('A')">Fixer le départ (A)</button><button class="btn sm" onclick="D3.mark('B')">Fixer l’arrivée (B)</button></div>
  <label>Durée du mouvement (s)<input id="d3dur" type="number" min="1" max="15" value="5"></label>
  <div class="row"><button class="btn" onclick="D3.move()">Jouer A → B</button></div>
  <h3>Exporter</h3>
  <label>Ajouter aussi au projet<select id="d3proj"><option value="">Non, seulement télécharger</option>${S.data.projects.map(p => opt(p.id, p.title, '')).join('')}</select></label>
  <label>Numéro du plan<input id="d3shot" type="number" min="1" value="1"></label>
  <div class="row"><button class="btn gold" onclick="D3.record()">Enregistrer la vidéo A → B</button><button class="btn" onclick="D3.snap()">Capture image</button></div>
  <span class="meta" id="d3stat"></span></div></div>`;

D3.mount = () => {
  const el = $('#d3c'); if (!el) return;
  if (!window.THREE || !THREE.OrbitControls) { el.innerHTML = '<div class="empty">Le moteur 3D n’a pas pu se charger : une connexion internet est nécessaire au premier lancement.</div>'; return; }
  if (!D3.ready) D3.init();
  el.appendChild(D3.r.domElement); D3.active = true; D3.list(); D3.loop();
};
D3.unmount = () => { D3.active = false; };
D3.init = () => {
  const r = D3.r = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  r.outputEncoding = THREE.sRGBEncoding; r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap;
  r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1;
  D3.scene = new THREE.Scene(); D3.cam = new THREE.PerspectiveCamera(40, 9 / 16, .1, 300);
  D3.cam.position.set(4, 1.7, 7); D3.ctl = new THREE.OrbitControls(D3.cam, r.domElement); D3.ctl.target.set(0, 1.1, 0); D3.ctl.enableDamping = true;
  D3.clock = new THREE.Clock(); D3.mixers = []; D3.decorG = new THREE.Group(); D3.lightG = new THREE.Group(); D3.scene.add(D3.decorG, D3.lightG);
  D3.setFrame(D3.frame); D3.setDecor(D3.decor); D3.setLight(D3.light); D3.addMannequin(0x3a0730, -0.6); D3.addMannequin(0xf1bc18, 0.7);
  D3.ready = true;
};
D3.loop = () => {
  if (!D3.active) return; requestAnimationFrame(D3.loop);
  const dt = D3.clock.getDelta(); D3.mixers.forEach(m => m.update(dt));
  if (D3.anim) D3.anim(); else D3.ctl.update();
  D3.r.render(D3.scene, D3.cam);
};
D3.setFrame = f => { D3.frame = f; const [w, h] = FR3[f]; D3.r.setSize(w, h, false); D3.cam.aspect = w / h; D3.cam.updateProjectionMatrix(); };
const mat = (c, o = {}) => new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: .8 }, o));
function box(w, h, d, c, x, y, z, o) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat(c, o)); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; return m; }
D3.setDecor = name => {
  D3.decor = name; const g = D3.decorG; while (g.children.length) g.remove(g.children[0]);
  const floor = (c, s = 60) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(s, s), mat(c)); m.rotation.x = -Math.PI / 2; m.receiveShadow = true; g.add(m); };
  if (name === 'studio') { floor(0x2a0021); const w = new THREE.Mesh(new THREE.PlaneGeometry(30, 14), mat(0x1a0014)); w.position.set(0, 7, -6); g.add(w); }
  if (name === 'rue') {
    floor(0x3b3b3b); g.add(box(60, .15, 3, 0x9a9a9a, 0, .07, -5), box(60, .15, 3, 0x9a9a9a, 0, .07, 5));
    const cols = [0xe8c07a, 0xd96b4f, 0x7fb3a6, 0xf2e6d0, 0xb3567a, 0xe3a857];
    for (let i = -6; i <= 6; i++) { const h = 4 + ((i * 7 + 13) % 5) * 1.6; g.add(box(3.6, h, 4, cols[(i + 12) % cols.length], i * 4, h / 2, -9)); g.add(box(3.6, h * .8, 4, cols[(i + 15) % cols.length], i * 4, h * .4, 9)); }
    const taxi = new THREE.Group(); taxi.add(box(4, 1, 1.8, 0xff7a1a, 0, .75, 0), box(2.2, .7, 1.7, 0xff7a1a, -.2, 1.55, 0));
    [[-1.3, .85], [1.3, .85], [-1.3, -.85], [1.3, -.85]].forEach(([x, z]) => { const w = new THREE.Mesh(new THREE.CylinderGeometry(.35, .35, .25, 16), mat(0x111111)); w.rotation.x = Math.PI / 2; w.position.set(x, .35, z); taxi.add(w); });
    taxi.position.set(-5, 0, 1.8); g.add(taxi);
  }
  if (name === 'salon') {
    floor(0x7a4a24, 14); g.add(box(14, 4, .2, 0xf2e6d0, 0, 2, -5), box(.2, 4, 10, 0xeadcc4, -6, 2, 0));
    g.add(box(3, .5, 1, 0x3a0730, -2.5, .45, -3.8), box(3, .9, .3, 0x3a0730, -2.5, .9, -4.3), box(1.2, .4, .7, 0x5b3a1e, -2.5, .2, -2.2));
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(.3, .25, .6, 16), mat(0xb0703a)); pot.position.set(2.8, .3, -4); const leaf = new THREE.Mesh(new THREE.ConeGeometry(.7, 2, 12), mat(0x2f6b3a)); leaf.position.set(2.8, 1.6, -4); g.add(pot, leaf);
  }
  if (name === 'maquis') {
    floor(0xa77d4f, 30); const cc = [0xd62828, 0x1d5fbf, 0xf2f2f2];
    for (let i = 0; i < 6; i++) { const x = (i % 3) * 3 - 3, z = Math.floor(i / 3) * 3 - 3; g.add(box(1.2, .08, 1.2, 0xf2f2f2, x, .75, z), box(.1, .75, .1, 0xdddddd, x, .37, z)); [[.9, 0], [-.9, 0]].forEach(([dx]) => g.add(box(.5, .5, .5, cc[(i + (dx > 0 ? 1 : 0)) % 3], x + dx, .25, z))); }
    for (let i = -6; i <= 6; i++) { const b = new THREE.Mesh(new THREE.SphereGeometry(.07, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffd38a })); b.position.set(i * .8, 3 + Math.cos(i / 2) * .2, -5); g.add(b); }
    g.add(box(14, 3.4, .2, 0x8a2f2f, 0, 1.7, -6));
  }
};
D3.setLight = name => {
  D3.light = name; const g = D3.lightG; while (g.children.length) g.remove(g.children[0]);
  const dir = (c, i, x, y, z) => { const l = new THREE.DirectionalLight(c, i); l.position.set(x, y, z); l.castShadow = true; l.shadow.mapSize.set(2048, 2048); Object.assign(l.shadow.camera, { left: -15, right: 15, top: 15, bottom: -15 }); g.add(l); };
  if (name === 'golden') { D3.scene.background = new THREE.Color(0xeaa560); D3.scene.fog = new THREE.Fog(0xeaa560, 20, 70); g.add(new THREE.HemisphereLight(0xffe2b0, 0x3a0730, .6)); dir(0xffaa5e, 2.4, 10, 3.5, 6); }
  if (name === 'nuit') { D3.scene.background = new THREE.Color(0x070818); D3.scene.fog = new THREE.Fog(0x070818, 10, 45); g.add(new THREE.HemisphereLight(0x3a4d80, 0x100010, .35)); dir(0x6d8cff, .4, -6, 8, 4); [[-3, 3, 1], [3, 3, -1]].forEach(([x, y, z]) => { const p = new THREE.PointLight(0xffb050, 1.6, 12); p.position.set(x, y, z); g.add(p); }); }
  if (name === 'studio') { D3.scene.background = new THREE.Color(0x1a0014); D3.scene.fog = null; g.add(new THREE.HemisphereLight(0xffffff, 0x2a0021, .55)); dir(0xffffff, 1.6, 4, 6, 6); dir(0xf1bc18, 1.4, -4, 4, -5); }
};
D3.addMannequin = (color = 0x2b2b2b, x = (Math.random() - .5) * 3) => {
  const g = new THREE.Group(), m = mat(color, { roughness: .6 }), skin = mat(0x4a2c1d, { roughness: .5 });
  const cyl = (r, h, y, ox = 0, mm = m) => { const c = new THREE.Mesh(new THREE.CylinderGeometry(r, r * .9, h, 16), mm); c.position.set(ox, y, 0); c.castShadow = true; g.add(c); };
  cyl(.2, .7, 1.15); cyl(.08, .82, .41, -.1); cyl(.08, .82, .41, .1); cyl(.06, .65, 1.15, -.28, skin); cyl(.06, .65, 1.15, .28, skin); cyl(.06, .12, 1.55, 0, skin);
  const h = new THREE.Mesh(new THREE.SphereGeometry(.12, 20, 20), skin); h.position.y = 1.68; h.scale.set(1, 1.15, 1); h.castShadow = true; g.add(h);
  g.position.x = x; D3.scene.add(g); D3.objs.push({ name: 'Silhouette ' + (D3.objs.length + 1), o: g }); D3.sel = D3.objs.length - 1; D3.list();
};
D3.importGLB = f => {
  if (!THREE.GLTFLoader) return toast('Chargeur 3D indisponible');
  f.arrayBuffer().then(buf => new THREE.GLTFLoader().parse(buf, '', gltf => {
    const o = gltf.scene, bb = new THREE.Box3().setFromObject(o), h = bb.max.y - bb.min.y || 1, k = 1.75 / h;
    o.scale.setScalar(k); o.position.y = -bb.min.y * k; o.traverse(n => { if (n.isMesh) { n.castShadow = n.receiveShadow = true; } });
    const wrap = new THREE.Group(); wrap.add(o); D3.scene.add(wrap);
    if (gltf.animations.length) { const mx = new THREE.AnimationMixer(o); mx.clipAction(gltf.animations[0]).play(); D3.mixers.push(mx); }
    D3.objs.push({ name: f.name.replace(/\.(glb|gltf)$/i, ''), o: wrap }); D3.sel = D3.objs.length - 1; D3.list(); toast('Modèle 3D importé' + (gltf.animations.length ? ' avec son animation' : ''));
  }, e => toast('Fichier 3D illisible : ' + (e.message || e))));
};
D3.list = () => {
  const l = $('#d3list'); if (!l) return;
  l.innerHTML = D3.objs.map((x, i) => `<button class="btn sm${i === D3.sel ? ' gold' : ''}" onclick="D3.sel=${i};D3.list()">${esc(x.name)}</button>`).join('');
  const o = D3.objs[D3.sel], s = $('#d3sel'); if (!s) return;
  s.innerHTML = o ? `<div class="grid">${[['x', 'Gauche ↔ droite', -8, 8, o.o.position.x], ['z', 'Avant ↔ arrière', -8, 8, o.o.position.z], ['r', 'Rotation', -180, 180, Math.round(o.o.rotation.y * 180 / Math.PI)]].map(([k, lab, a, b, v]) => `<label>${lab}<input type="range" min="${a}" max="${b}" step="${k === 'r' ? 1 : .1}" value="${v}" oninput="D3.tf('${k}',this.value)"></label>`).join('')}</div><button class="btn sm danger" onclick="D3.del()">Retirer</button>` : '';
};
D3.tf = (k, v) => { const o = D3.objs[D3.sel]; if (!o) return; if (k === 'r') o.o.rotation.y = v * Math.PI / 180; else o.o.position[k] = +v; };
D3.del = () => { const o = D3.objs[D3.sel]; if (!o) return; D3.scene.remove(o.o); D3.objs.splice(D3.sel, 1); D3.sel = D3.objs.length - 1; D3.list(); };
D3.mark = k => { D3[k] = { p: D3.cam.position.clone(), t: D3.ctl.target.clone() }; toast(`Point ${k} enregistré`); };
D3.move = () => new Promise(res => {
  if (!D3.A || !D3.B) { toast('Fixez d’abord le départ (A) et l’arrivée (B)'); return res(false); }
  const dur = Math.min(15, Math.max(1, +($('#d3dur') || {}).value || 5)) * 1000, t0 = performance.now(), ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
  D3.ctl.enabled = false;
  D3.anim = () => { const k = Math.min(1, (performance.now() - t0) / dur), e = ease(k); D3.cam.position.lerpVectors(D3.A.p, D3.B.p, e); D3.ctl.target.lerpVectors(D3.A.t, D3.B.t, e); D3.cam.lookAt(D3.ctl.target); if (k >= 1) { D3.anim = null; D3.ctl.enabled = true; res(true); } };
});
D3.target = () => { const pid = ($('#d3proj') || {}).value; return pid ? [pid, Math.max(1, +$('#d3shot').value || 1) - 1] : null; };
D3.record = async () => {
  if (!D3.A || !D3.B) return toast('Fixez d’abord le départ (A) et l’arrivée (B)');
  const mime = ['video/mp4', 'video/webm;codecs=vp9', 'video/webm'].find(m => MediaRecorder.isTypeSupported(m)); if (!mime) return toast('Enregistrement vidéo non pris en charge : utilisez Chrome ou Edge');
  const st = D3.r.domElement.captureStream(30), rec = new MediaRecorder(st, { mimeType: mime, videoBitsPerSecond: 8e6 }), ch = [];
  rec.ondataavailable = e => e.data.size && ch.push(e.data); $('#d3stat').textContent = 'Enregistrement…';
  const done = new Promise(r => rec.onstop = r); rec.start(250); await D3.move(); rec.stop(); await done;
  const blob = new Blob(ch, { type: mime }), ext = mime.includes('mp4') ? 'mp4' : 'webm';
  download(blob, `scene-3d-${D3.frame.replace(':', 'x')}.${ext}`); const t = D3.target(); if (t) await A.attach(t[0], t[1], blob, 'scène 3D');
  $('#d3stat').textContent = 'Vidéo 3D exportée.';
};
D3.snap = () => D3.r.domElement.toBlob(async b => { download(b, `capture-3d-${D3.frame.replace(':', 'x')}.png`); const t = D3.target(); if (t) await A.attach(t[0], t[1], b, 'capture 3D'); }, 'image/png');
