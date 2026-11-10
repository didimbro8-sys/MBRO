/* AM Studio Vidéo IA — moteur open source gratuit.
   Modèles ouverts hébergés sur Hugging Face (ZeroGPU) :
   - image : FLUX.1 Krea [dev] (Black Forest Labs, poids ouverts)
   - image → vidéo : Wan 2.2 (Alibaba, licence Apache 2.0)
   - texte → vidéo : LTX-Video (Lightricks, poids ouverts)
   Sans compte, le quota gratuit est limité par jour ; un jeton Hugging Face gratuit (Sauvegarde → Moteur) l'augmente. */
/* Script classique + import() dynamique : fonctionne aussi en double-cliquant sur index.html (file://). */
(async () => {
let Client;
try { ({ Client } = await import("https://cdn.jsdelivr.net/npm/@gradio/client@1.15.1/dist/index.min.js")); }
catch (e) { window.OS = { error: "Moteur open source non chargé (connexion internet requise)." }; return; }

// Identifiants des Spaces (l'adresse directe *.hf.space est refusée par le navigateur pour des raisons de sécurité CORS).
const SPACES = { image: "black-forest-labs/FLUX.1-Krea-dev", animate: "prithivMLmods/Wan2.2-Fast", t2v: "Lightricks/ltx-video-distilled" };
const SIZES = { "9:16": [576, 1024], "1:1": [1024, 1024], "16:9": [1024, 576] };
const VSIZES = { "9:16": [512, 896], "1:1": [704, 704], "16:9": [896, 512] };
const clients = {};
const token = () => { try { return localStorage.getItem("amstudio-hf") || undefined; } catch (e) { return undefined; } };
async function client(k) { return clients[k] || (clients[k] = await Client.connect(SPACES[k], token() ? { hf_token: token() } : {})); }
function fileUrl(d) { if (!d) return null; if (typeof d === "string") return d; if (d.video) return fileUrl(d.video); return d.url || null; }
async function grab(d) { const u = fileUrl(d); if (!u) throw new Error("réponse sans fichier"); const r = await fetch(u); if (!r.ok) throw new Error("téléchargement impossible"); return r.blob(); }
const blobToDataURL = b => new Promise((res, rej) => { const f = new FileReader(); f.onload = () => res(f.result); f.onerror = rej; f.readAsDataURL(b); });
function explain(e) {
  const m = String((e && (e.message || e.title)) || e);
  if (/metadata could not be loaded|429|rate limit/i.test(m)) return "Hugging Face limite les appels pour le moment. Réessayez dans une heure.";
  if (/quota|ZeroGPU|exceeded/i.test(m)) return "quota gratuit du jour atteint. Ajoutez un jeton Hugging Face gratuit (Sauvegarde) ou réessayez plus tard.";
  return m.slice(0, 200);
}

window.OS = {
  spaces: SPACES,
  async image(prompt, fmt = "9:16") {
    const [w, h] = SIZES[fmt] || SIZES["9:16"];
    try { const r = await (await client("image")).predict("/infer", { prompt, seed: 0, randomize_seed: true, width: w, height: h, guidance_scale: 4.5, num_inference_steps: 28 }); return grab(r.data[0]); }
    catch (e) { throw new Error(explain(e)); }
  },
  async animate(imageBlob, prompt, secs = 5) {
    try {
      const r = await (await client("animate")).predict("/generate_video", { image_b64: await blobToDataURL(imageBlob), prompt, steps: 6, negative_prompt: "blurry, distorted face, deformed hands, extra fingers, plastic skin, cartoon, text, watermark, jittery", duration_seconds: Math.min(5, Math.max(1, secs)), guidance_scale: 1, guidance_scale_2: 1, seed: 42, randomize_seed: true });
      return grab(r.data[0]);
    } catch (e) { throw new Error(explain(e)); }
  },
  async t2v(prompt, fmt = "9:16", secs = 5) {
    const [w, h] = VSIZES[fmt] || VSIZES["9:16"];
    try {
      const r = await (await client("t2v")).predict("/text_to_video", { prompt, negative_prompt: "worst quality, inconsistent motion, blurry, jittery, distorted, plastic skin, deformed hands", input_image_filepath: null, input_video_filepath: null, height_ui: h, width_ui: w, mode: "text-to-video", duration_ui: Math.min(8, secs), ui_frames_to_use: 9, seed_ui: 42, randomize_seed: true, ui_guidance_scale: 1, improve_texture_flag: true });
      return grab(r.data[0]);
    } catch (e) { throw new Error(explain(e)); }
  }
};
window.dispatchEvent(new Event("os-ready"));
})();
