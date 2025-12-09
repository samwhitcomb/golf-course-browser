import React, { useState } from 'react'
import './StatsBar.css'

function StatsBar({ course, stats }) {
  const [playerCount, setPlayerCount] = useState(2)
  const [hoveredSegment, setHoveredSegment] = useState(null)
  const [showHandicapTooltip, setShowHandicapTooltip] = useState(false)

  if (!stats) return null

  const scoreRelativeToPar = stats.averageScore - stats.par
  const scoreRelativeText = scoreRelativeToPar >= 0 
    ? `(+${scoreRelativeToPar.toFixed(0)})` 
    : `(${scoreRelativeToPar.toFixed(0)})`

  // GIR tag logic
  const getGIRTag = (percentage) => {
    if (percentage < 45) {
      return { text: 'Narrow', color: '#dc2626', emoji: '🔴' }
    } else if (percentage <= 60) {
      return { text: 'Average', color: '#eab308', emoji: '🟡' }
    } else {
      return { text: 'Wide', color: '#22c55e', emoji: '🟢' }
    }
  }

  const girTag = getGIRTag(stats.girPercentage)

  // Calculate segment widths for heatmap
  const segmentWidths = {
    birdieEagle: stats.scoreDistribution.birdieEagle,
    par: stats.scoreDistribution.par,
    bogey: stats.scoreDistribution.bogey,
    doubleBogeyPlus: stats.scoreDistribution.doubleBogeyPlus
  }

  const getSegmentTooltip = (type) => {
    const percentage = stats.scoreDistribution[type]
    const rounds = Math.round(stats.totalRounds * (percentage / 100))
    const labels = {
      birdieEagle: 'Birdie/Eagle',
      par: 'Par',
      bogey: 'Bogey',
      doubleBogeyPlus: 'Double Bogey+'
    }
    return `${labels[type]}: ${percentage}% of rounds (${rounds.toLocaleString()} total)`
  }

  return (
    <div className="stats-bar">
      <div className="stats-bar-container">
        {/* Average Score */}
        <div className="stat-column">
          <div className="stat-label">Average Score</div>
          <div className="stat-primary">
            <span className="stat-value-large">{stats.averageScore.toFixed(1)}</span>
            <span className="stat-info-icon" 
                  onMouseEnter={() => setShowHandicapTooltip(true)}
                  onMouseLeave={() => setShowHandicapTooltip(false)}>
              ⓘ
              {showHandicapTooltip && (
                <div className="stat-tooltip handicap-tooltip">
                  <div className="tooltip-arrow"></div>
                  <div className="tooltip-content">
                    {Object.entries(stats.handicapTiers).map(([tier, score]) => (
                      <div key={tier} className="tooltip-row">
                        <span className="tooltip-label">{tier} HCP Avg:</span>
                        <span className="tooltip-value">{score.toFixed(1)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </span>
          </div>
          <div className="stat-secondary">
            {scoreRelativeText} on Par {stats.par}
          </div>
        </div>

        {/* Average Time */}
        <div className="stat-column">
          <div className="stat-label">Average Time</div>
          <div className="stat-primary">
            <span className="stat-value-large">{stats.averageTime[playerCount]}</span>
          </div>
          <div className="stat-secondary">
            For {playerCount} {playerCount === 1 ? 'Player' : 'Players'}
          </div>
          <div className="player-selector">
            {[1, 2, 3, 4].map(count => (
              <button
                key={count}
                className={`player-btn ${playerCount === count ? 'active' : ''}`}
                onClick={() => setPlayerCount(count)}
              >
                {count}P
              </button>
            ))}
          </div>
        </div>

        {/* GIR Percentage */}
        <div className="stat-column">
          <div className="stat-label">GIR Percentage</div>
          <div className="stat-primary">
            <span className="stat-value-large">{stats.girPercentage}%</span>
          </div>
          <div className="stat-secondary">
            <span className="gir-tag" style={{ color: girTag.color }}>
              {girTag.emoji} {girTag.text}
            </span>
          </div>
          <div className="stat-tertiary">
            Average Stimp {stats.stimpSpeed}
          </div>
        </div>

        {/* Mapping Type (for Studio, Standard, and LEGACY courses) */}
        {stats.mappingType && (
          <div className="stat-column">
            <div className="stat-label">Mapping Type</div>
            <div className="stat-primary">
              <span className={`stat-value-large ${stats.version === 'studio' ? 'studio-premium-text' : ''}`}>
                {stats.mappingType}
              </span>
            </div>
            <div className="stat-secondary">
              {stats.mappingType === 'Radar' 
                ? '+/-5m Accuracy'
                : stats.version === 'studio' 
                ? 'Sub-Centimeter Accuracy' 
                : '1m Accuracy'}
            </div>
          </div>
        )}

        {/* Scoring Zone Heatmap */}
        <div className="stat-column">
          <div className="stat-label">Score Distribution</div>
          <div className="heatmap-container">
            <div className="heatmap-bar">
              <div
                className="heatmap-segment segment-birdie"
                style={{ width: `${segmentWidths.birdieEagle}%` }}
                onMouseEnter={() => setHoveredSegment('birdieEagle')}
                onMouseLeave={() => setHoveredSegment(null)}
              >
                {hoveredSegment === 'birdieEagle' && (
                  <div className="heatmap-tooltip">
                    <div className="tooltip-arrow"></div>
                    {getSegmentTooltip('birdieEagle')}
                  </div>
                )}
              </div>
              <div
                className="heatmap-segment segment-par"
                style={{ width: `${segmentWidths.par}%` }}
                onMouseEnter={() => setHoveredSegment('par')}
                onMouseLeave={() => setHoveredSegment(null)}
              >
                {hoveredSegment === 'par' && (
                  <div className="heatmap-tooltip">
                    <div className="tooltip-arrow"></div>
                    {getSegmentTooltip('par')}
                  </div>
                )}
              </div>
              <div
                className="heatmap-segment segment-bogey"
                style={{ width: `${segmentWidths.bogey}%` }}
                onMouseEnter={() => setHoveredSegment('bogey')}
                onMouseLeave={() => setHoveredSegment(null)}
              >
                {hoveredSegment === 'bogey' && (
                  <div className="heatmap-tooltip">
                    <div className="tooltip-arrow"></div>
                    {getSegmentTooltip('bogey')}
                  </div>
                )}
              </div>
              <div
                className="heatmap-segment segment-double"
                style={{ width: `${segmentWidths.doubleBogeyPlus}%` }}
                onMouseEnter={() => setHoveredSegment('doubleBogeyPlus')}
                onMouseLeave={() => setHoveredSegment(null)}
              >
                {hoveredSegment === 'doubleBogeyPlus' && (
                  <div className="heatmap-tooltip">
                    <div className="tooltip-arrow"></div>
                    {getSegmentTooltip('doubleBogeyPlus')}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatsBar

