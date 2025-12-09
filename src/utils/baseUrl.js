// Get the base URL for GitHub Pages
// This will be '/golf-course-browser/' in production, or '/' in development
export const BASE_URL = import.meta.env.BASE_URL || '/'

// Helper function to create paths with base URL
export const getAssetPath = (path) => {
  // Remove leading slash if present, then add base URL
  const cleanPath = path.startsWith('/') ? path.slice(1) : path
  return `${BASE_URL}${cleanPath}`
}

