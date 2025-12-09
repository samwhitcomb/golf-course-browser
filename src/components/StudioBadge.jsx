import React from 'react'
import './StudioBadge.css'

function StudioBadge({ variant = 'default', size = 'medium' }) {
  return (
    <div className={`studio-badge studio-badge-${variant} studio-badge-${size}`}>
      <span className="studio-badge-text">STUDIOS</span>
    </div>
  )
}

export default StudioBadge


