// Configuration du générateur de site. Vous n'avez pas besoin de modifier ce fichier.
export default function (eleventyConfig) {
  // Sécurité : tout texte saisi dans l'administration est échappé avant d'être affiché
  eleventyConfig.setNunjucksEnvironmentOptions({ autoescape: true, throwOnUndefined: false });

  // Le texte des articles est du Markdown pur : tout code HTML collé est affiché comme du texte, jamais exécuté
  eleventyConfig.amendLibrary("md", (md) => md.set({ html: false }));

  // Fichiers copiés tels quels
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/favicon.svg");
  eleventyConfig.addPassthroughCopy("src/favicon.png");
  eleventyConfig.addPassthroughCopy("src/site.webmanifest");
  eleventyConfig.addPassthroughCopy("src/_headers");
  eleventyConfig.addPassthroughCopy("src/.well-known");

  const escape = (s) => String(s ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");

  // "[à compléter]" s'affiche comme une étiquette visible, pour ne rien oublier
  eleventyConfig.addFilter("todo", (s) =>
    escape(s).replace(/\[([^\]]+)\]/g, '<span class="todo">$1</span>'));

  // Même chose dans le texte libre déjà converti en HTML
  eleventyConfig.addFilter("todoHtml", (html) => String(html ?? "").replace(/\[([^\]<>]+)\](?!\()/g, '<span class="todo">$1</span>'));

  const mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
  eleventyConfig.addFilter("dateFr", (d) => { const x = new Date(d); return `${x.getUTCDate()} ${mois[x.getUTCMonth()]} ${x.getUTCFullYear()}`; });
  eleventyConfig.addFilter("moisAnnee", (d) => { const x = new Date(d); return `${mois[x.getUTCMonth()]} ${x.getUTCFullYear()}`; });
  eleventyConfig.addFilter("iso", (d) => new Date(d).toISOString().slice(0, 10));
  // JSON sûr à l'intérieur d'une balise <script> (empêche toute sortie de la balise)
  eleventyConfig.addFilter("json", (v) => JSON.stringify(v ?? "")
    .replace(/</g, "\\u003c").replace(/>/g, "\\u003e").replace(/&/g, "\\u0026")
    .replace(/\u2028/g, "\\u2028").replace(/\u2029/g, "\\u2029"));

  // Liens et images : seuls les chemins du site (/...) et les adresses https:// sont acceptés.
  // Bloque javascript:, data:, http:// et tout lien piégé saisi par erreur dans l'administration.
  eleventyConfig.addFilter("safeUrl", (u) => {
    const v = String(u ?? "").trim();
    if (/^\/(?!\/)[^\s"'<>]*$/.test(v)) return v;
    if (/^https:\/\/[^\s"'<>]+$/i.test(v)) return v;
    return "";
  });
  // Images et fichiers : uniquement ceux hébergés sur le site (envoyés via l'administration)
  eleventyConfig.addFilter("localUrl", (u) => { const v = String(u ?? "").trim(); return /^\/(?!\/)[^\s"'<>]*$/.test(v) ? v : ""; });
  // Numéro chronologique : la plus ancienne réalisation porte le n° 01
  eleventyConfig.addFilter("rang", (coll, url) => { const i = coll.findIndex((p) => p.url === url); return i < 0 ? 0 : coll.length - i; });
  eleventyConfig.addFilter("vitrines", (coll) => (coll || []).filter((p) => p.data.vitrine));
  eleventyConfig.addFilter("pad", (n) => String(n).padStart(2, "0"));

  const visibles = (items) => items.filter((p) => p.data.publie !== false);
  const recentes = (a, b) => (b.date - a.date);

  eleventyConfig.addCollection("realisations", (api) =>
    visibles(api.getFilteredByGlob("src/realisations/*.md")).sort(recentes));
  eleventyConfig.addCollection("aLaUne", (api) =>
    visibles(api.getFilteredByGlob("src/realisations/*.md")).filter((p) => p.data.a_la_une)
      .sort((a, b) => (a.data.priorite ?? 99) - (b.data.priorite ?? 99) || recentes(a, b)).slice(0, 3));
  eleventyConfig.addCollection("journal", (api) =>
    visibles(api.getFilteredByGlob("src/journal/*.md")).sort(recentes));

  return {
    dir: { input: "src", includes: "_includes", data: "_data", output: "_site" },
    markdownTemplateEngine: false,
    htmlTemplateEngine: "njk",
  };
}
