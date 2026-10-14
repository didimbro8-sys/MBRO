// Une veille décochée « Publier » ne génère aucune page et n'apparaît nulle part.
export default {
  layout: "veille.njk",
  publie: true,
  eleventyComputed: {
    permalink: (data) => {
      if (!data.page.inputPath.endsWith(".md")) return data.permalink;
      return data.publie === false ? false : `/veille/${data.page.fileSlug}/`;
    },
    eleventyExcludeFromCollections: (data) => data.page.inputPath.endsWith(".md") && data.publie === false,
  },
};
