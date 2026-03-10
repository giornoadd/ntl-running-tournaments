export const resolveImagePath = (imgPath: string): string => {
    if (!imgPath || !imgPath.startsWith('../member_results/')) {
        return imgPath;
    }

    // When hosted on GitHub Pages, the site lives in a sub-path "/ntl-running-tournaments/html/"
    // So the absolute path to member_results is "/ntl-running-tournaments/member_results/"
    if (window.location.hostname.includes('github.io')) {
        return imgPath.replace('../member_results/', '/ntl-running-tournaments/member_results/');
    }

    // For absolute root (like Vite dev server or standard localhost)
    return imgPath.replace('../member_results/', '/member_results/');
};
