// Utility function for getting course blurbs (same logic as EditApp)

export function getBlurb(course) {
  // Use custom descriptions if available, otherwise generate
  if (course.blurb && Array.isArray(course.blurb)) {
    // For igolf courses, single paragraph is fine; for others, need at least 2
    if (course.isIgolf && course.blurb.length >= 1) {
      return course.blurb
    }
    if (!course.isIgolf && course.blurb.length >= 2) {
      return course.blurb
    }
  }
  
  // For igolf courses with description field, convert to array
  if (course.isIgolf && course.description && !course.blurb) {
    return [course.description]
  }
  
  // Fallback to generated blurbs
  const templates = [
    (c) => [
      `${c.name} is a standout track that blends its setting in ${c.location} with a routing that rewards thoughtful shot-making. ${c.description}`,
      `Known for its character and consistency, it has earned a ${c.rating?.toFixed ? c.rating.toFixed(1) : c.rating}/5 reputation. Regulars point to its history and memorable holes as the reason it remains a must-play in the region.`
    ],
    (c) => [
      `Set in ${c.location}, ${c.name} weaves scenery into strategy, asking golfers to choose lines carefully while enjoying the landscape. ${c.description}`,
      `Its acclaim (${c.rating?.toFixed ? c.rating.toFixed(1) : c.rating}/5) comes from a mix of architecture, conditioning, and a few signature moments that keep players talking long after the round.`
    ],
    (c) => [
      `${c.name} sits in ${c.location}, offering a classic feel with enough bite to keep low-handicaps honest. ${c.description}`,
      `Stories around the clubhouse often cite its storied holes and steady challenge; with a ${c.rating?.toFixed ? c.rating.toFixed(1) : c.rating}/5 rating, it stays firmly on the shortlist for return trips.`
    ],
  ]
  const idx = Math.abs((course.id || '').split('').reduce((a, ch) => a + ch.charCodeAt(0), 0)) % templates.length
  return templates[idx](course)
}


