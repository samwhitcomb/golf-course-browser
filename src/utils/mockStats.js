/**
 * Generate mock statistics for a golf course based on its characteristics
 * @param {Object} course - Course object with rating, yardage, type, etc.
 * @param {string} version - 'standard' or 'studio' (default: 'studio' if isStudio, else 'standard')
 * @returns {Object} Stats object with all required metrics
 */
export function generateMockStats(course, version = null) {
  const rating = course.rating || 4.0
  const yardage = course.yardage || 7000
  const par = course.par || 72
  const type = course.type || 'parkland'
  const isStudio = course.isStudio || false
  
  // Determine version
  const isIgolf = course.isIgolf || false
  if (!version) {
    if (isIgolf) {
      version = 'igolf'
    } else {
      version = isStudio ? 'studio' : 'standard'
    }
  }
  
  // Studio version is more challenging due to accuracy
  // LEGACY version is less accurate, so slightly easier than standard
  const versionMultiplier = version === 'studio' ? 1.05 : version === 'igolf' ? 0.90 : 0.95
  
  // Average Score: Higher rating = higher average score
  // Base score around par, adjusted by difficulty
  // Studio version has slightly higher scores due to more accurate/challenging terrain
  let baseScore = par + (rating - 4.0) * 8
  if (version === 'studio') {
    baseScore += 0.7 // Studio is more challenging
  } else if (version === 'igolf') {
    baseScore -= 1.0 // LEGACY is easier (less accurate mapping)
  } else {
    baseScore -= 0.7 // Standard is easier
  }
  const averageScore = Math.round((baseScore + Math.random() * 2 - 1) * 10) / 10
  
  // Handicap tiers - better players score lower
  const handicapTiers = {
    '0-5': Math.round((averageScore - 8 + Math.random() * 2) * 10) / 10,
    '6-10': Math.round((averageScore - 4 + Math.random() * 2) * 10) / 10,
    '11-15': Math.round((averageScore + Math.random() * 2) * 10) / 10,
    '16-20': Math.round((averageScore + 4 + Math.random() * 2) * 10) / 10,
    '21+': Math.round((averageScore + 8 + Math.random() * 2) * 10) / 10
  }
  
  // Average Time: Based on yardage and difficulty
  // Base time for 2 players, longer courses take more time
  const baseMinutes = 60 + (yardage - 6500) / 50
  const timeFor2 = Math.round(baseMinutes)
  const averageTime = {
    1: formatTime(timeFor2 - 10),
    2: formatTime(timeFor2),
    3: formatTime(timeFor2 + 15),
    4: formatTime(timeFor2 + 30)
  }
  
  // GIR Percentage: Lower for difficult courses
  // Championship courses have lower GIR
  // Studio version has lower GIR due to more accurate terrain
  let girBase = 50
  if (rating >= 4.5) {
    girBase = 38
  } else if (rating >= 4.0) {
    girBase = 42
  } else if (rating >= 3.5) {
    girBase = 48
  } else {
    girBase = 55
  }
  
  // Adjust for version: Studio is more challenging (lower GIR)
  if (version === 'studio') {
    girBase = Math.max(20, girBase - 3) // Studio is 3% harder
  } else if (version === 'igolf') {
    girBase = Math.min(80, girBase + 5) // iGolf is 5% easier (less accurate mapping)
  } else {
    girBase = Math.min(80, girBase + 3) // Standard is 3% easier
  }
  
  const girPercentage = Math.round(girBase + (Math.random() * 6 - 3))
  
  // Stimp Speed: Higher for championship courses
  let stimpSpeed = 9
  if (rating >= 4.5) {
    stimpSpeed = 11 + Math.round(Math.random() * 2)
  } else if (rating >= 4.0) {
    stimpSpeed = 10 + Math.round(Math.random() * 2)
  } else {
    stimpSpeed = 9 + Math.round(Math.random() * 2)
  }
  
  // Greens Size
  const greensSizes = ['Small', 'Medium', 'Large']
  const greensSize = greensSizes[Math.floor(Math.random() * greensSizes.length)]
  
  // Score Distribution: More bogeys for difficult courses
  let birdieEagle, parScore, bogey, doubleBogeyPlus
  
  if (rating >= 4.5) {
    // Very difficult
    birdieEagle = 10 + Math.round(Math.random() * 5)
    parScore = 35 + Math.round(Math.random() * 5)
    bogey = 35 + Math.round(Math.random() * 5)
    doubleBogeyPlus = 20 - (birdieEagle + parScore + bogey - 100)
  } else if (rating >= 4.0) {
    // Difficult
    birdieEagle = 12 + Math.round(Math.random() * 5)
    parScore = 38 + Math.round(Math.random() * 5)
    bogey = 32 + Math.round(Math.random() * 5)
    doubleBogeyPlus = 18 - (birdieEagle + parScore + bogey - 100)
  } else if (rating >= 3.5) {
    // Moderate
    birdieEagle = 15 + Math.round(Math.random() * 5)
    parScore = 40 + Math.round(Math.random() * 5)
    bogey = 30 + Math.round(Math.random() * 5)
    doubleBogeyPlus = 15 - (birdieEagle + parScore + bogey - 100)
  } else {
    // Easy
    birdieEagle = 18 + Math.round(Math.random() * 5)
    parScore = 42 + Math.round(Math.random() * 5)
    bogey = 28 + Math.round(Math.random() * 5)
    doubleBogeyPlus = 12 - (birdieEagle + parScore + bogey - 100)
  }
  
  // Ensure percentages add up to 100
  const total = birdieEagle + parScore + bogey + doubleBogeyPlus
  if (total !== 100) {
    const diff = 100 - total
    bogey += diff
  }
  
  const scoreDistribution = {
    birdieEagle: Math.max(0, birdieEagle),
    par: Math.max(0, parScore),
    bogey: Math.max(0, bogey),
    doubleBogeyPlus: Math.max(0, doubleBogeyPlus)
  }
  
  // Total rounds: More popular courses have more rounds
  const totalRounds = rating >= 4.5 
    ? 20000 + Math.floor(Math.random() * 10000)
    : rating >= 4.0
    ? 15000 + Math.floor(Math.random() * 10000)
    : 10000 + Math.floor(Math.random() * 10000)
  
  // Add mapping type based on version or course type
  let mappingType
  if (course.isIgolf) {
    mappingType = course.igolfFeatures?.mappingType || 'Radar'
  } else if (version === 'studio') {
    mappingType = course.studioFeatures?.mappingType || 'Lidar'
  } else {
    mappingType = course.standardFeatures?.mappingType || 'Satellite'
  }
  
  return {
    averageScore,
    par,
    handicapTiers,
    averageTime,
    girPercentage,
    stimpSpeed,
    greensSize,
    scoreDistribution,
    totalRounds,
    mappingType,
    version
  }
}

/**
 * Format minutes into time string (e.g., 75 -> "1h 15m")
 * @param {number} minutes - Total minutes
 * @returns {string} Formatted time string
 */
function formatTime(minutes) {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  if (hours === 0) {
    return `${mins}m`
  }
  if (mins === 0) {
    return `${hours}h`
  }
  return `${hours}h ${mins}m`
}

