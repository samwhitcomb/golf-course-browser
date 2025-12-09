// User preferences stored in localStorage

const FAVORITES_KEY = 'golf_courses_favorites'
const PLAY_LATER_KEY = 'golf_courses_play_later'
const LAST_PLAYED_KEY = 'golf_courses_last_played'
const RATINGS_KEY = 'golf_courses_ratings'
const RATINGS_MIGRATED_KEY = 'golf_courses_ratings_migrated'

/**
 * Get all favorited course IDs
 * @returns {Set<string>} Set of course IDs
 */
export function getFavorites() {
  try {
    const favorites = localStorage.getItem(FAVORITES_KEY)
    if (favorites) {
      const ids = JSON.parse(favorites)
      return new Set(Array.isArray(ids) ? ids : [])
    }
  } catch (err) {
    console.error('Error reading favorites from localStorage:', err)
  }
  return new Set()
}

/**
 * Toggle favorite status for a course
 * @param {string} courseId - Course ID to toggle
 * @returns {boolean} New favorite status (true if now favorited, false if removed)
 */
export function toggleFavorite(courseId) {
  try {
    const favorites = getFavorites()
    const isFavorited = favorites.has(courseId)
    
    if (isFavorited) {
      favorites.delete(courseId)
    } else {
      favorites.add(courseId)
    }
    
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(Array.from(favorites)))
    return !isFavorited
  } catch (err) {
    console.error('Error toggling favorite in localStorage:', err)
    return false
  }
}

/**
 * Check if a course is favorited
 * @param {string} courseId - Course ID to check
 * @returns {boolean} True if favorited
 */
export function isFavorite(courseId) {
  const favorites = getFavorites()
  return favorites.has(courseId)
}

/**
 * Set the last played course
 * @param {string} courseId - Course ID that was played
 */
export function setLastPlayed(courseId) {
  try {
    localStorage.setItem(LAST_PLAYED_KEY, courseId)
    // Remove from play later list when played
    removeFromPlayLater(courseId)
  } catch (err) {
    console.error('Error setting last played in localStorage:', err)
  }
}

/**
 * Get the last played course ID
 * @returns {string|null} Course ID or null if none
 */
export function getLastPlayed() {
  try {
    return localStorage.getItem(LAST_PLAYED_KEY)
  } catch (err) {
    console.error('Error reading last played from localStorage:', err)
    return null
  }
}

/**
 * Get all play later course IDs
 * @returns {Set<string>} Set of course IDs
 */
export function getPlayLater() {
  try {
    const playLater = localStorage.getItem(PLAY_LATER_KEY)
    if (playLater) {
      const ids = JSON.parse(playLater)
      return new Set(Array.isArray(ids) ? ids : [])
    }
  } catch (err) {
    console.error('Error reading play later from localStorage:', err)
  }
  return new Set()
}

/**
 * Toggle play later status for a course
 * @param {string} courseId - Course ID to toggle
 * @returns {boolean} New play later status (true if now in list, false if removed)
 */
export function togglePlayLater(courseId) {
  try {
    const playLater = getPlayLater()
    const isInList = playLater.has(courseId)
    
    if (isInList) {
      playLater.delete(courseId)
    } else {
      playLater.add(courseId)
    }
    
    localStorage.setItem(PLAY_LATER_KEY, JSON.stringify(Array.from(playLater)))
    return !isInList
  } catch (err) {
    console.error('Error toggling play later in localStorage:', err)
    return false
  }
}

/**
 * Check if a course is in play later list
 * @param {string} courseId - Course ID to check
 * @returns {boolean} True if in play later list
 */
export function isPlayLater(courseId) {
  const playLater = getPlayLater()
  return playLater.has(courseId)
}

/**
 * Remove a course from play later list (when played)
 * @param {string} courseId - Course ID to remove
 */
export function removeFromPlayLater(courseId) {
  try {
    const playLater = getPlayLater()
    playLater.delete(courseId)
    localStorage.setItem(PLAY_LATER_KEY, JSON.stringify(Array.from(playLater)))
  } catch (err) {
    console.error('Error removing from play later in localStorage:', err)
  }
}

/**
 * Get all course ratings
 * @returns {Map<string, number>} Map of courseId -> rating (1-5)
 */
export function getRatings() {
  try {
    const ratings = localStorage.getItem(RATINGS_KEY)
    if (ratings) {
      const data = JSON.parse(ratings)
      return new Map(Object.entries(data))
    }
  } catch (err) {
    console.error('Error reading ratings from localStorage:', err)
  }
  return new Map()
}

/**
 * Set rating for a course
 * @param {string} courseId - Course ID to rate
 * @param {number} rating - Rating value (1-5)
 */
export function setRating(courseId, rating) {
  try {
    if (rating < 1 || rating > 5) {
      console.error('Rating must be between 1 and 5')
      return
    }
    const ratings = getRatings()
    ratings.set(courseId, rating)
    localStorage.setItem(RATINGS_KEY, JSON.stringify(Object.fromEntries(ratings)))
  } catch (err) {
    console.error('Error setting rating in localStorage:', err)
  }
}

/**
 * Get rating for a specific course
 * @param {string} courseId - Course ID to check
 * @returns {number} Rating (1-5) or 0 if not rated
 */
export function getRating(courseId) {
  const ratings = getRatings()
  return ratings.get(courseId) || 0
}

/**
 * Get all course IDs that have ratings
 * @returns {string[]} Array of course IDs that have been rated
 */
export function getRatedCourses() {
  const ratings = getRatings()
  return Array.from(ratings.keys())
}

/**
 * Remove rating for a course
 * @param {string} courseId - Course ID to remove rating from
 */
export function removeRating(courseId) {
  try {
    const ratings = getRatings()
    ratings.delete(courseId)
    localStorage.setItem(RATINGS_KEY, JSON.stringify(Object.fromEntries(ratings)))
  } catch (err) {
    console.error('Error removing rating from localStorage:', err)
  }
}

/**
 * Migrate existing favorites to 5-star ratings
 * This runs once on first load
 */
export function migrateFavoritesToRatings() {
  try {
    // Check if migration has already been done
    const migrated = localStorage.getItem(RATINGS_MIGRATED_KEY)
    if (migrated === 'true') {
      return
    }

    // Get all favorites
    const favorites = getFavorites()
    
    if (favorites.size > 0) {
      // Convert each favorite to a 5-star rating
      const ratings = getRatings()
      favorites.forEach(courseId => {
        // Only set if not already rated
        if (!ratings.has(courseId)) {
          ratings.set(courseId, 5)
        }
      })
      localStorage.setItem(RATINGS_KEY, JSON.stringify(Object.fromEntries(ratings)))
    }

    // Mark migration as complete
    localStorage.setItem(RATINGS_MIGRATED_KEY, 'true')
  } catch (err) {
    console.error('Error migrating favorites to ratings:', err)
  }
}

