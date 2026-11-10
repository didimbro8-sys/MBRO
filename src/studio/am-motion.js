/* AM Motion — moteur maison AM Digital, 100 % local et illimité.
   Transforme une photo réaliste en plan de cinéma animé :
   1. estimation de la profondeur dans le navigateur (Depth Anything V2 Small, open source, via transformers.js) ;
   2. relief 3D de la photo, parcouru par une vraie caméra (travelling, orbite, grue, épaule…) : parallaxe réelle ;
   3. effets de tournage : grain, vignettage, scintillement des lumières, poussières dorées, étalonnage chaud.
   Aucun serveur, aucun quota : seul le premier lancement télécharge le modèle (~27 Mo, gardé en cache). */
const AMM = {
  pipe: null,
  RES: { '9:16': [720, 1280], '1:1': [960, 960], '16:9': [1280, 720] },
  MOVES: {
    'Plan fixe': 'breath', 'Travelling avant lent': 'dolly', 'Travelling latéral': 'lateral', 'Panoramique': 'lateral',
    "Caméra à l'épaule": 'handheld', 'Gros plan visage': 'dolly', "Plan large d'ensemble": 'lateral', 'Contre-plongée': 'crane',
    'Drone en approche': 'dollyFast', 'Orbite autour du sujet': 'orbit'
  },
  CROPS: { gauche: [0, .18, .62, .62], droite: [.38, .22, .62, .62], centre: [.2, .2, .6, .6], bas: [.12, .52, .5, .48], haut: [.15, 0, .6, .6] },
  CROP_LABELS: [['', 'Image entière'], ['gauche', 'Gros plan à gauche'], ['droite', 'Gros plan à droite'], ['centre', 'Centre serré'], ['bas', 'Détail en bas'], ['haut', 'Haut de l’image']],
  async loadDepth(status) {
    if (AMM.pipe) return AMM.pipe;
    status && status('Chargement du modèle de profondeur (une seule fois)…');
    const T = await import('https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.5.1/dist/transformers.min.js');
    T.env.allowLocalModels = false;
    AMM.pipe = await T.pipeline('depth-estimation', 'onnx-community/depth-anything-v2-small', { dtype: 'q8' });
    return AMM.pipe;
  },
  async depth(img, status) {
    const pipe = await AMM.loadDepth(status); status && status('Analyse du relief de l’image…');
    const src = document.createElement('canvas'); src.width = img.naturalWidth; src.height = img.naturalHeight; src.getContext('2d').drawImage(img, 0, 0);
    const out = await pipe(src.toDataURL('image/jpeg', .92));
    const d = out.depth.toCanvas ? out.depth.toCanvas() : null; if (!d) throw new Error('profondeur illisible');
    const c = document.createElement('canvas'); c.width = 512; c.height = Math.round(512 * img.naturalHeight / img.naturalWidth);
    const x = c.getContext('2d'); x.filter = 'blur(3px)'; x.drawImage(d, 0, 0, c.width, c.height); return c;
  },
  async render(blob, o = {}) {
    if (!window.THREE) throw new Error('moteur 3D non chargé (connexion internet au premier lancement)');
    const st = o.status || (() => {}), secs = Math.max(2, Math.min(15, +o.secs || 5)), [W, H] = AMM.RES[o.format] || AMM.RES['9:16'];
    let img = new Image(); img.src = URL.createObjectURL(blob); await img.decode();
    const cr = AMM.CROPS[o.crop];
    if (cr) { // recadrage : plusieurs plans tournés dans une même image
      const [fx, fy, fw, fh] = cr, c = document.createElement('canvas'); c.width = Math.round(img.naturalWidth * fw); c.height = Math.round(img.naturalHeight * fh);
      c.getContext('2d').drawImage(img, img.naturalWidth * fx, img.naturalHeight * fy, c.width, c.height, 0, 0, c.width, c.height);
      const im2 = new Image(); im2.src = c.toDataURL('image/jpeg', .95); await im2.decode(); URL.revokeObjectURL(img.src); img = im2;
    }
    if (o.sharpen) { // netteté x2 : Swin2SR (open source, Apache 2.0), utile pour les gros plans recadrés
      st('Netteté x2 (Swin2SR)…');
      const T = await import('https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.5.1/dist/transformers.min.js');
      AMM.sr = AMM.sr || await T.pipeline('image-to-image', 'Xenova/swin2SR-lightweight-x2-64');
      const c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight; c.getContext('2d').drawImage(img, 0, 0);
      const up = (await AMM.sr(c.toDataURL('image/png'))).toCanvas(), t = document.createElement('canvas'); t.width = img.naturalWidth * 2; t.height = img.naturalHeight * 2;
      t.getContext('2d').drawImage(up, 0, 0, t.width, t.height, 0, 0, t.width, t.height);
      const im3 = new Image(); im3.src = t.toDataURL('image/jpeg', .95); await im3.decode(); img = im3;
    }
    const depthCv = await AMM.depth(img, st);
    st('Tournage du plan…');
    const r = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true }); r.setPixelRatio(1); r.setSize(W, H, false);
    // Aperçu flottant toujours visible : Chrome n'enregistre pas un canevas hors de l'écran.
    const live = document.createElement('div'); live.id = 'amm-live'; live.style.aspectRatio = W + '/' + H; live.innerHTML = '<b>AM Motion · tournage</b>'; live.prepend(r.domElement); document.body.appendChild(live);
    const scene = new THREE.Scene(), fov = 35, cam = new THREE.PerspectiveCamera(fov, W / H, .01, 100);
    const ia = img.naturalWidth / img.naturalHeight, PH = 2, PW = PH * ia, margin = 1.14;
    const vh = Math.min(PH, PW / (W / H)) / margin, vw = vh * W / H, D = vh / (2 * Math.tan(fov * Math.PI / 360));
    const tex = new THREE.Texture(img); tex.needsUpdate = true; tex.minFilter = THREE.LinearFilter;
    const dtex = new THREE.CanvasTexture(depthCv); dtex.minFilter = THREE.LinearFilter;
    const look = o.look || 'golden', warm = look === 'golden' ? .55 : look === 'interieur' ? .35 : look === 'nuit' ? -.2 : .15;
    const U = { uTex: { value: tex }, uDepth: { value: dtex }, uAmp: { value: D * .2 }, uTime: { value: 0 }, uRes: { value: new THREE.Vector2(W, H) },
      uGrain: { value: .045 }, uVig: { value: .55 }, uFlick: { value: o.flicker === false ? 0 : 1 }, uWarm: { value: warm } };
    const mat = new THREE.ShaderMaterial({
      uniforms: U,
      vertexShader: `uniform sampler2D uDepth;uniform float uAmp;varying vec2 vUv;
        void main(){vUv=uv;float d=texture2D(uDepth,uv).r;vec3 p=position;p.z+=(d-.5)*uAmp;gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);}`,
      fragmentShader: `uniform sampler2D uTex;uniform float uTime,uGrain,uVig,uFlick,uWarm;uniform vec2 uRes;varying vec2 vUv;
        float rnd(vec2 c){return fract(sin(dot(c,vec2(12.9898,78.233)))*43758.5453);}
        void main(){vec3 c=texture2D(uTex,vUv).rgb;float l=dot(c,vec3(.299,.587,.114));
          c*=1.+uFlick*smoothstep(.72,1.,l)*.07*sin(uTime*11.+vUv.x*37.+vUv.y*23.)*sin(uTime*6.7+vUv.y*19.);
          c=uWarm>0.?mix(c,c*vec3(1.06,1.,.9),uWarm):mix(c,c*vec3(.92,.97,1.08),-uWarm);
          c=mix(vec3(l),c,1.06);vec2 q=gl_FragCoord.xy/uRes-.5;c*=1.-uVig*dot(q,q)*1.4;
          c+=(rnd(gl_FragCoord.xy+fract(uTime)*91.)-.5)*uGrain;gl_FragColor=vec4(c,1.);}`
    });
    const seg = 256, plane = new THREE.Mesh(new THREE.PlaneGeometry(PW, PH, seg, Math.round(seg / ia)), mat); scene.add(plane);
    // poussières / bokeh dorés en suspension devant l'image
    let dust = null;
    if (o.dust !== false) {
      const n = 70, pos = new Float32Array(n * 3), sp = document.createElement('canvas'); sp.width = sp.height = 64;
      const g = sp.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,220,150,1)'); gr.addColorStop(1, 'rgba(255,200,120,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
      for (let i = 0; i < n; i++) { pos[i * 3] = (Math.random() - .5) * vw * 1.2; pos[i * 3 + 1] = (Math.random() - .5) * vh * 1.2; pos[i * 3 + 2] = D * (.05 + Math.random() * .35); }
      const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      dust = new THREE.Points(geo, new THREE.PointsMaterial({ size: vh * .012, map: new THREE.CanvasTexture(sp), transparent: true, opacity: look === 'nuit' ? .5 : .35, depthWrite: false, blending: THREE.AdditiveBlending }));
      scene.add(dust);
    }
    const move = AMM.MOVES[o.camera] || o.move || 'dolly', ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
    const place = (k, t) => {
      const e = ease(k); let x = 0, y = 0, z = D, tx = 0, ty = 0;
      if (move === 'dolly') z = D * (1 - .1 * e);
      else if (move === 'dollyFast') z = D * (1 - .16 * e);
      else if (move === 'lateral') { x = vw * .055 * (2 * e - 1); tx = x * .4; }
      else if (move === 'orbit') { const a = (e - .5) * .14; x = D * Math.sin(a); z = D * Math.cos(a); }
      else if (move === 'crane') { y = vh * .05 * (2 * e - 1); ty = y * .4; z = D * (1 - .04 * e); }
      else if (move === 'handheld') { z = D * (1 - .05 * e); x = D * .006 * (Math.sin(t * 1.9) + .5 * Math.sin(t * 4.3)); y = D * .005 * (Math.sin(t * 2.3 + 1) + .4 * Math.sin(t * 5.1)); }
      else z = D * (1 - .035 * e); // respiration
      cam.position.set(x, y, z); cam.lookAt(tx, ty, 0);
    };
    const mime = ['video/mp4;codecs=avc1.42E01E', 'video/mp4', 'video/webm;codecs=vp9', 'video/webm'].find(m => window.MediaRecorder && MediaRecorder.isTypeSupported(m));
    if (!mime) throw new Error('enregistrement vidéo impossible : utilisez Chrome ou Edge');
    place(0, 0); r.render(scene, cam);
    const rec = new MediaRecorder(r.domElement.captureStream(30), { mimeType: mime, videoBitsPerSecond: 10e6 }), ch = [];
    rec.ondataavailable = e => e.data.size && ch.push(e.data);
    const done = new Promise(res => rec.onstop = res); rec.start(250);
    await new Promise(res => {
      const t0 = performance.now();
      const f = () => {
        const t = (performance.now() - t0) / 1000, k = Math.min(1, t / secs);
        place(k, t); U.uTime.value = t;
        if (dust) { const a = dust.geometry.attributes.position; for (let i = 0; i < a.count; i++) { a.array[i * 3 + 1] += vh * .0007; a.array[i * 3] += Math.sin(t + i) * vw * .0003; if (a.array[i * 3 + 1] > vh * .6) a.array[i * 3 + 1] = -vh * .6; } a.needsUpdate = true; }
        r.render(scene, cam); o.onProgress && o.onProgress(k);
        if (k < 1) requestAnimationFrame(f); else res();
      };
      requestAnimationFrame(f);
    });
    rec.stop(); await done; live.remove();
    URL.revokeObjectURL(img.src); tex.dispose(); dtex.dispose(); mat.dispose(); plane.geometry.dispose(); r.dispose();
    return new Blob(ch, { type: mime.split(';')[0] });
  }
};

window.AMM = AMM;
