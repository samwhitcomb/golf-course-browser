import React, { useState, useEffect, useRef } from 'react'
import { generateScorecard } from '../utils/generateScorecard'
import './ScorecardPreview.css'

function ScorecardPreview({ course }) {
  const scorecardData = generateScorecard(course)
  const { holes, teeBoxes, totalPar, defaultTee } = scorecardData
  const [selectedTee, setSelectedTee] = useState(defaultTee)
  const [highlightedYardages, setHighlightedYardages] = useState(new Set())
  const [highlightTrigger, setHighlightTrigger] = useState(0)
  
  // Get yardages for selected tee
  const holesWithYardage = holes.map(hole => ({
    ...hole,
    yardage: hole.yardages[selectedTee] || hole.yardages.white
  }))
  
  // Highlight yardages when highlightTrigger changes
  useEffect(() => {
    if (highlightTrigger > 0) {
      // Mark all yardages as highlighted
      const allYardageKeys = holes.map((_, index) => `front-${index}`).concat(
        holes.map((_, index) => `back-${index}`),
        ['front-total', 'back-total', 'grand-total']
      )
      setHighlightedYardages(new Set(allYardageKeys))
      
      // Clear highlight after animation
      const timer = setTimeout(() => {
        setHighlightedYardages(new Set())
      }, 800)
      
      return () => clearTimeout(timer)
    }
  }, [highlightTrigger])
  
  // Trigger highlight when tee changes
  const handleTeeChange = (tee) => {
    setSelectedTee(tee)
    setHighlightTrigger(prev => prev + 1)
  }
  
  const totalYardage = holesWithYardage.reduce((sum, hole) => sum + hole.yardage, 0)
  
  // Calculate front 9 and back 9 totals
  const front9 = holesWithYardage.slice(0, 9)
  const back9 = holesWithYardage.slice(9, 18)
  const front9Par = front9.reduce((sum, hole) => sum + hole.par, 0)
  const back9Par = back9.reduce((sum, hole) => sum + hole.par, 0)
  const front9Yardage = front9.reduce((sum, hole) => sum + hole.yardage, 0)
  const back9Yardage = back9.reduce((sum, hole) => sum + hole.yardage, 0)
  
  const selectedTeeInfo = teeBoxes.find(t => t.name.toLowerCase() === selectedTee) || teeBoxes[2]

  const getParColor = (par) => {
    if (par === 3) return 'par-3'
    if (par === 4) return 'par-4'
    return 'par-5'
  }

  return (
    <div className="scorecard-preview">
      <div className="scorecard-header">
        <h2 className="scorecard-title">{course.name}</h2>
        <div className="scorecard-summary">
          <span>Par {totalPar}</span>
          <span>•</span>
          <span>{totalYardage.toLocaleString()} yds</span>
        </div>
        <div className="tee-selector">
          <span className="tee-selector-label">Tee:</span>
          <div className="tee-buttons">
            {teeBoxes.map(tee => {
              const teeKey = tee.name.toLowerCase()
              const isActive = selectedTee === teeKey
              return (
                <button
                  key={teeKey}
                  className={`tee-button ${isActive ? 'active' : ''}`}
                  onClick={() => handleTeeChange(teeKey)}
                  style={{
                    backgroundColor: isActive ? tee.color : 'transparent',
                    borderColor: tee.color,
                    color: teeKey === 'white' && isActive ? '#1a1a1a' : '#ffffff'
                  }}
                  title={tee.name}
                >
                  {tee.name}
                </button>
              )
            })}
          </div>
        </div>
      </div>

      <div className="scorecard-table">
        <div className="scorecard-row scorecard-header-row">
          <div className="scorecard-cell header">Hole</div>
          <div className="scorecard-cell header">Par</div>
          <div className="scorecard-cell header">Yards</div>
          <div className="scorecard-cell header">HCP</div>
          <div className="scorecard-divider"></div>
          <div className="scorecard-cell header">Hole</div>
          <div className="scorecard-cell header">Par</div>
          <div className="scorecard-cell header">Yards</div>
          <div className="scorecard-cell header">HCP</div>
        </div>

        {front9.map((hole, index) => {
          const backHole = back9[index]
          const frontYardageKey = `front-${index}`
          const backYardageKey = `back-${index}`
          const isFrontHighlighted = highlightedYardages.has(frontYardageKey)
          const isBackHighlighted = highlightedYardages.has(backYardageKey)
          return (
            <div key={hole.number} className="scorecard-row">
              <div className="scorecard-cell hole-number">
                {hole.number}
              </div>
              <div className={`scorecard-cell par ${getParColor(hole.par)}`}>
                {hole.par}
              </div>
              <div className="scorecard-cell yardage">
                <span 
                  className={isFrontHighlighted ? 'yardage-number highlighted' : 'yardage-number'}
                  style={isFrontHighlighted ? { '--highlight-color': selectedTeeInfo.color } : {}}
                >
                  {hole.yardage}
                </span>
              </div>
              <div className="scorecard-cell handicap">{hole.handicap}</div>
              <div className="scorecard-divider"></div>
              <div className="scorecard-cell hole-number">
                {backHole.number}
              </div>
              <div className={`scorecard-cell par ${getParColor(backHole.par)}`}>
                {backHole.par}
              </div>
              <div className="scorecard-cell yardage">
                <span 
                  className={isBackHighlighted ? 'yardage-number highlighted' : 'yardage-number'}
                  style={isBackHighlighted ? { '--highlight-color': selectedTeeInfo.color } : {}}
                >
                  {backHole.yardage}
                </span>
              </div>
              <div className="scorecard-cell handicap">{backHole.handicap}</div>
            </div>
          )
        })}

        <div className="scorecard-row scorecard-totals-row">
          <div className="scorecard-cell total-label">Out</div>
          <div className="scorecard-cell total-value">{front9Par}</div>
          <div className="scorecard-cell total-value">
            <span 
              className={highlightedYardages.has('front-total') ? 'yardage-number highlighted' : 'yardage-number'}
              style={highlightedYardages.has('front-total') ? { '--highlight-color': selectedTeeInfo.color } : {}}
            >
              {front9Yardage}
            </span>
          </div>
          <div className="scorecard-cell"></div>
          <div className="scorecard-divider"></div>
          <div className="scorecard-cell total-label">In</div>
          <div className="scorecard-cell total-value">{back9Par}</div>
          <div className="scorecard-cell total-value">
            <span 
              className={highlightedYardages.has('back-total') ? 'yardage-number highlighted' : 'yardage-number'}
              style={highlightedYardages.has('back-total') ? { '--highlight-color': selectedTeeInfo.color } : {}}
            >
              {back9Yardage}
            </span>
          </div>
          <div className="scorecard-cell"></div>
        </div>

        <div className="scorecard-row scorecard-totals-row final-total">
          <div className="scorecard-cell total-label">Total</div>
          <div className="scorecard-cell total-value">{totalPar}</div>
          <div className="scorecard-cell total-value">
            <span 
              className={highlightedYardages.has('grand-total') ? 'yardage-number highlighted' : 'yardage-number'}
              style={highlightedYardages.has('grand-total') ? { '--highlight-color': selectedTeeInfo.color } : {}}
            >
              {totalYardage}
            </span>
          </div>
          <div className="scorecard-cell"></div>
          <div className="scorecard-divider"></div>
          <div className="scorecard-cell"></div>
          <div className="scorecard-cell"></div>
          <div className="scorecard-cell"></div>
          <div className="scorecard-cell"></div>
        </div>
      </div>
    </div>
  )
}

export default ScorecardPreview

