// Convert relative paths to absolute URLs
function resolveRelativePaths() {
    const baseUrl = window.location.origin + window.location.pathname.replace(/\/[^\/]*$/, '/');
    
    // Update all relative src attributes
    document.querySelectorAll('[src]').forEach(element => {
        const src = element.getAttribute('src');
        if (src && src.startsWith('./') || src.startsWith('../')) {
            element.src = new URL(src, baseUrl).href;
        }
    });
    
    // Update all relative href attributes
    document.querySelectorAll('[href]').forEach(element => {
        const href = element.getAttribute('href');
        if (href && (href.startsWith('./') || href.startsWith('../')) && !href.startsWith('http')) {
            element.href = new URL(href, baseUrl).href;
        }
    });
}

// Run when DOM is loaded
document.addEventListener('DOMContentLoaded', resolveRelativePaths);