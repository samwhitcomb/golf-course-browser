import React from 'react'
import './VersionSelector.css'

function VersionSelector({ selectedVersion, onVersionChange, isStudio, hasStandardVersion }) {
  if (!isStudio || !hasStandardVersion) {
    return null
  }

  return (
    <div className="version-selector">
      <div className="version-selector-label">Course Version:</div>
      <div className="version-toggle">
        <button
          className={`version-option ${selectedVersion === 'standard' ? 'active' : ''}`}
          onClick={() => onVersionChange('standard')}
        >
          <span className="version-name">Standard</span>
          <span className="version-badge version-badge-free">FREE</span>
        </button>
        <div className="version-vs">VS</div>
        <button
          className={`version-option version-option-studio ${selectedVersion === 'studio' ? 'active' : ''}`}
          onClick={() => onVersionChange('studio')}
        >
          <span className="version-name">Studios</span>
          <span className="version-badge version-badge-studio">PREMIUM</span>
        </button>
      </div>
    </div>
  )
}

export default VersionSelector


