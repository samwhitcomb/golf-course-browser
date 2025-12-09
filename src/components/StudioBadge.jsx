import React from 'react'
import './StudioBadge.css'

function StudioBadge({ variant = 'default', size = 'medium' }) {
  return (
    <div className={`studio-badge studio-badge-${variant} studio-badge-${size}`}>
      <span className="studio-badge-icon">💎</span>
      <span className="studio-badge-text">STUDIO</span>
    </div>
  )
}

export default StudioBadge


