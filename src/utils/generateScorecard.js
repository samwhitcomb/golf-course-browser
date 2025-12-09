/**
 * Generate mock scorecard data for a golf course with multiple tee box yardages
 * @param {Object} course - Course object with par, yardage, etc.
 * @returns {Object} Object with holes array and tee box information
 */
export function generateScorecard(course) {
  const totalYardage = course.yardage || 7000
  const totalPar = course.par || 72
  const rating = course.rating || 4.0
  
  // Tee box definitions (typical golf course tee colors)
  const teeBoxes = [
    { name: 'Black', color: '#1a1a1a', yardageMultiplier: 1.0 },      // Championship/Longest
    { name: 'Blue', color: '#3b82f6', yardageMultiplier: 0.95 },      // Back tees
    { name: 'White', color: '#ffffff', yardageMultiplier: 0.88 },      // Middle tees
    { name: 'Gold', color: '#fbbf24', yardageMultiplier: 0.82 },      // Senior tees
    { name: 'Red', color: '#ef4444', yardageMultiplier: 0.75 }         // Forward tees
  ]
  
  // Standard par distribution for 18 holes (most common: 4 par-3s, 10 par-4s, 4 par-5s)
  const parDistribution = [3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5]
  
  // Adjust par distribution based on total par
  if (totalPar === 71) {
    parDistribution[0] = 4 // Change one par-3 to par-4
  } else if (totalPar === 73) {
    parDistribution[14] = 4 // Change one par-5 to par-4
  } else if (totalPar === 70) {
    parDistribution[0] = 4
    parDistribution[1] = 4 // Change two par-3s to par-4s
  }
  
  // Generate base yardages for each hole (using Black/Championship tees as base)
  const baseHoles = []
  let remainingYardage = totalYardage
  
  for (let i = 0; i < 18; i++) {
    const par = parDistribution[i]
    
    // Calculate base yardage based on par
    let baseYardage
    if (par === 3) {
      baseYardage = 150 + Math.floor(Math.random() * 50) // 150-200 yards
    } else if (par === 4) {
      baseYardage = 350 + Math.floor(Math.random() * 100) // 350-450 yards
    } else { // par 5
      baseYardage = 500 + Math.floor(Math.random() * 100) // 500-600 yards
    }
    
    // Adjust to match total yardage
    if (i === 17) {
      // Last hole gets remaining yardage
      baseYardage = remainingYardage
    } else {
      // Adjust slightly to match total
      const adjustment = Math.round((totalYardage - remainingYardage) / (18 - i))
      baseYardage += adjustment
      remainingYardage -= baseYardage
    }
    
    // Ensure reasonable bounds
    if (par === 3) {
      baseYardage = Math.max(120, Math.min(230, baseYardage))
    } else if (par === 4) {
      baseYardage = Math.max(300, Math.min(500, baseYardage))
    } else {
      baseYardage = Math.max(450, Math.min(650, baseYardage))
    }
    
    baseHoles.push({
      number: i + 1,
      par: par,
      baseYardage: Math.round(baseYardage)
    })
  }
  
  // Generate yardages for each tee box
  const holes = baseHoles.map(hole => {
    const teeYardages = {}
    teeBoxes.forEach(tee => {
      // Calculate yardage for this tee box
      let yardage = Math.round(hole.baseYardage * tee.yardageMultiplier)
      
      // Add some variation per hole (not all holes shorten equally)
      const variation = Math.round((Math.random() - 0.5) * 20)
      yardage += variation
      
      // Ensure reasonable bounds based on par
      if (hole.par === 3) {
        yardage = Math.max(100, Math.min(230, yardage))
      } else if (hole.par === 4) {
        yardage = Math.max(250, Math.min(500, yardage))
      } else {
        yardage = Math.max(400, Math.min(650, yardage))
      }
      
      teeYardages[tee.name.toLowerCase()] = Math.round(yardage)
    })
    
    return {
      number: hole.number,
      par: hole.par,
      yardages: teeYardages,
      baseYardage: hole.baseYardage
    }
  })
  
  // Calculate handicap (difficulty ranking) based on base yardage
  holes.sort((a, b) => {
    // Harder holes (longer, higher par) get lower handicap
    const difficultyA = a.baseYardage + (a.par * 100)
    const difficultyB = b.baseYardage + (b.par * 100)
    return difficultyB - difficultyA
  })
  
  holes.forEach((hole, index) => {
    hole.handicap = index + 1
  })
  
  // Sort back by hole number
  holes.sort((a, b) => a.number - b.number)
  
  return {
    holes,
    teeBoxes,
    totalPar,
    defaultTee: 'white' // Default to white tees
  }
}

