// Utility function for getting course blurbs

export function getBlurb(course) {
  // First check localStorage for saved descriptions (from EditApp)
  try {
    const savedDescriptions = JSON.parse(localStorage.getItem('course_descriptions') || '{}')
    if (savedDescriptions[course.id] && savedDescriptions[course.id].blurb) {
      return savedDescriptions[course.id].blurb
    }
  } catch (err) {
    console.error('Error reading saved descriptions:', err)
  }
  
  // Use custom descriptions from course data if available
  if (course.blurb && Array.isArray(course.blurb) && course.blurb.length >= 2) {
    return course.blurb
  }
  
  // Fallback to generated blurbs
  const templates = [
    (c) => [
      `${c.name} is a standout track that blends its setting in ${c.location} with a routing that rewards thoughtful shot-making. ${c.description || ''}`,
      `Known for its character and consistency, it has earned a ${c.rating?.toFixed ? c.rating.toFixed(1) : c.rating}/5 reputation. Regulars point to its history and memorable holes as the reason it remains a must-play in the region.`
    ],
    (c) => [
      `Set in ${c.location}, ${c.name} weaves scenery into strategy, asking golfers to choose lines carefully while enjoying the landscape. ${c.description || ''}`,
      `Its acclaim (${c.rating?.toFixed ? c.rating.toFixed(1) : c.rating}/5) comes from a mix of architecture, conditioning, and a few signature moments that keep players talking long after the round.`
    ],
    (c) => [
      `${c.name} sits in ${c.location}, offering a classic feel with enough bite to keep low-handicaps honest. ${c.description || ''}`,
      `Stories around the clubhouse often cite its storied holes and steady challenge; with a ${c.rating?.toFixed ? c.rating.toFixed(1) : c.rating}/5 rating, it stays firmly on the shortlist for return trips.`
    ],
  ]
  const idx = Math.abs((course.id || '').split('').reduce((a, ch) => a + ch.charCodeAt(0), 0)) % templates.length
  return templates[idx](course)
}


