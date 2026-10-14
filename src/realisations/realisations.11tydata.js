// Un brouillon (case « Publier » décochée) ne génère aucune page et n'apparaît nulle part.
export default {
  layout: "realisation.njk",
  publie: true,
  eleventyComputed: {
    permalink: (data) => {
      if (!data.page.inputPath.endsWith(".md")) return data.permalink;
      return data.publie === false ? false : `/realisations/${data.page.fileSlug}/`;
    },
    eleventyExcludeFromCollections: (data) => data.page.inputPath.endsWith(".md") && data.publie === false,
  },
};
