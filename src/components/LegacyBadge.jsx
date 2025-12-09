import React from 'react'
import './LegacyBadge.css'

function LegacyBadge({ variant = 'default', size = 'medium' }) {
  return (
    <div className={`legacy-badge legacy-badge-${variant} legacy-badge-${size}`}>
      <span className="legacy-badge-text">LEGACY</span>
    </div>
  )
}

export default LegacyBadge

