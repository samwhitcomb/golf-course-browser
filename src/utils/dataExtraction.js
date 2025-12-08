// Utility functions for extracting data from course descriptions

export function extractArchitect(course) {
  if (course.architect) return course.architect
  
  const desc = course.description || ''
  const blurb = course.blurb ? course.blurb.join(' ') : ''
  const fullText = (desc + ' ' + blurb).toLowerCase()
  
  const architectPatterns = [
    { name: 'Alister MacKenzie', patterns: ['alister mackenzie', 'mackenzie'] },
    { name: 'Donald Ross', patterns: ['donald ross', 'ross'] },
    { name: 'Pete Dye', patterns: ['pete dye', 'p. dye'] },
    { name: 'Jack Nicklaus', patterns: ['jack nicklaus', 'nicklaus'] },
    { name: 'Ben Crenshaw', patterns: ['ben crenshaw', 'crenshaw'] },
    { name: 'Bill Coore', patterns: ['bill coore', 'coore'] },
    { name: 'A.W. Tillinghast', patterns: ['tillinghast', 'a.w. tillinghast'] },
    { name: 'Hugh Wilson', patterns: ['hugh wilson'] },
    { name: 'Old Tom Morris', patterns: ['old tom morris', 'tom morris'] },
    { name: 'Harry Colt', patterns: ['harry colt', 'colt'] },
    { name: 'Tom Weiskopf', patterns: ['tom weiskopf', 'weiskopf'] },
    { name: 'Tom Fazio', patterns: ['tom fazio', 'fazio'] },
    { name: 'Robert Trent Jones', patterns: ['robert trent jones', 'rtj'] },
    { name: 'George Thomas', patterns: ['george thomas'] },
    { name: 'William Flynn', patterns: ['william flynn', 'flynn'] },
    { name: 'Perry Maxwell', patterns: ['perry maxwell', 'maxwell'] },
    { name: 'Walter Travis', patterns: ['walter travis', 'travis'] },
  ]
  
  for (const arch of architectPatterns) {
    for (const pattern of arch.patterns) {
      if (fullText.includes(pattern)) {
        return arch.name
      }
    }
  }
  
  return null
}

export function extractEstablishedYear(course) {
  if (course.established) return course.established
  
  const desc = course.description || ''
  const blurb = course.blurb ? course.blurb.join(' ') : ''
  const fullText = desc + ' ' + blurb
  
  // Look for patterns like "founded 1933", "established 1928", "opened 1907"
  const yearPatterns = [
    /founded\s+(\d{4})/i,
    /established\s+(\d{4})/i,
    /opened\s+(\d{4})/i,
    /built\s+(\d{4})/i,
    /since\s+(\d{4})/i,
  ]
  
  for (const pattern of yearPatterns) {
    const match = fullText.match(pattern)
    if (match && match[1]) {
      const year = parseInt(match[1])
      if (year >= 1800 && year <= new Date().getFullYear()) {
        return year
      }
    }
  }
  
  return null
}

export function getDifficultyRating(course) {
  const rating = course.rating || 0
  
  if (rating >= 4.5) return { level: 'Brutal', percent: 100, color: '#dc2626' }
  if (rating >= 4.0) return { level: 'Hard', percent: 75, color: '#f59e0b' }
  if (rating >= 3.5) return { level: 'Moderate', percent: 50, color: '#eab308' }
  return { level: 'Resort Style', percent: 25, color: '#22c55e' }
}

export function getCountryFlag(location) {
  const locationLower = (location || '').toLowerCase()
  
  // United Kingdom & Ireland
  if (locationLower.includes('scotland') || locationLower.includes('england') || 
      locationLower.includes('northern ireland') || locationLower.includes('uk')) {
    return '🇬🇧'
  }
  if (locationLower.includes('ireland')) return '🇮🇪'
  
  // Australia
  if (locationLower.includes('australia') || locationLower.includes('tasmania')) {
    return '🇦🇺'
  }
  
  // New Zealand
  if (locationLower.includes('new zealand')) {
    return '🇳🇿'
  }
  
  // Japan
  if (locationLower.includes('japan') || locationLower.includes('kobe') || 
      locationLower.includes('osaka') || locationLower.includes('saitama')) {
    return '🇯🇵'
  }
  
  // South Korea
  if (locationLower.includes('south korea') || locationLower.includes('jeju')) {
    return '🇰🇷'
  }
  
  // China
  if (locationLower.includes('china') || locationLower.includes('shenzhen')) {
    return '🇨🇳'
  }
  
  // Thailand
  if (locationLower.includes('thailand') || locationLower.includes('pattaya') || 
      locationLower.includes('pathum thani')) {
    return '🇹🇭'
  }
  
  // Spain
  if (locationLower.includes('spain') || locationLower.includes('sotogrande') || 
      locationLower.includes('casares')) {
    return '🇪🇸'
  }
  
  // Portugal
  if (locationLower.includes('portugal') || locationLower.includes('cascais') || 
      locationLower.includes('óbidos')) {
    return '🇵🇹'
  }
  
  // France
  if (locationLower.includes('france') || locationLower.includes('paris') || 
      locationLower.includes('chantilly') || locationLower.includes('mortefontaine')) {
    return '🇫🇷'
  }
  
  // South Africa
  if (locationLower.includes('south africa') || locationLower.includes('george') || 
      locationLower.includes('kleinmond') || locationLower.includes('mpumalanga') || 
      locationLower.includes('sun city')) {
    return '🇿🇦'
  }
  
  // Canada
  if (locationLower.includes('canada') || locationLower.includes('toronto') || 
      locationLower.includes('ancaster') || locationLower.includes('nova scotia') || 
      locationLower.includes('inverness')) {
    return '🇨🇦'
  }
  
  // Mexico
  if (locationLower.includes('mexico') || locationLower.includes('playa del carmen')) {
    return '🇲🇽'
  }
  
  // Dominican Republic
  if (locationLower.includes('dominican') || locationLower.includes('punta cana') || 
      locationLower.includes('cap cana') || locationLower.includes('la romana')) {
    return '🇩🇴'
  }
  
  // Default to USA
  return '🇺🇸'
}

