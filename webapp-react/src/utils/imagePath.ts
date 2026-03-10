export const resolveImagePath = (imgPath: string): string => {
    if (!imgPath) return imgPath;

    // Paths from JSON are relative like "assets_data/member_results/..."
    // Prepend Vite's BASE_URL to make them absolute for the current environment:
    //   Dev:  "/" + "assets_data/..." = "/assets_data/..."
    //   Prod: "/ntl-running-tournaments/html/" + "assets_data/..." = correct GitHub Pages URL
    if (imgPath.startsWith('assets_data/')) {
        const base = import.meta.env.BASE_URL || '/';
        return `${base.endsWith('/') ? base : base + '/'}${imgPath}`;
    }

    return imgPath;
};
