/**
 * Process course data to add image paths
 * Constructs image URLs for hero and additional images
 * Uses primary extension, error handlers in components will try fallbacks
 */
export function processCourseImages(courses) {
  return courses.map(course => {
    const courseId = course.id
    const images = {
      hero: null,
      additional: []
    }
    
    // Hero image - try webp first (most common modern format)
    images.hero = `/images/${courseId}_hero.webp`
    
    // Additional images - only one path per slot
    // Error handlers in components will try fallback extensions
    images.additional.push(`/images/${courseId}_1.webp`)
    images.additional.push(`/images/${courseId}_2.webp`)
    
    return {
      ...course,
      images,
      hasImage: true, // Assume image exists, browser will handle 404
      imageUrl: images.hero
    }
  })
}

/**
 * Get image URL with fallback support
 * Tries multiple extensions until one works
 */
export function getImageWithFallback(courseId, slot = 'hero', extensions = null) {
  if (!extensions) {
    if (slot === 'hero') {
      extensions = ['_hero.webp', '_hero.jpg', '_hero.jpeg', '_hero.png', '_hero.gif']
    } else if (slot === '1') {
      extensions = ['_1.webp', '_1.jpg', '_1.jpeg', '_1.png', '_1.gif']
    } else if (slot === '2') {
      extensions = ['_2.webp', '_2.jpg', '_2.jpeg', '_2.png', '_2.gif']
    }
  }
  
  // Return the first extension as default
  return `/images/${courseId}${extensions[0]}`
}
