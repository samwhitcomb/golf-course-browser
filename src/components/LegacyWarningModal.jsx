import React, { useState } from 'react'
import { dismissLegacyWarning } from '../utils/userPreferences'
import './LegacyWarningModal.css'

function LegacyWarningModal({ course, onClose, onProceed, onCancel }) {
  const [dontShowAgain, setDontShowAgain] = useState(false)

  const handleProceed = () => {
    if (dontShowAgain) {
      dismissLegacyWarning()
    }
    if (onProceed) {
      onProceed()
    }
    onClose()
  }

  const handleCancel = () => {
    if (onCancel) {
      onCancel()
    }
    onClose()
  }

  return (
    <div className="legacy-warning-modal-backdrop" onClick={onClose}>
      <div className="legacy-warning-modal" onClick={e => e.stopPropagation()}>
        <button className="legacy-warning-modal-close" onClick={onClose}>×</button>
        
        <div className="legacy-warning-modal-header">
          <h2 className="legacy-warning-modal-title">Low Quality Course Warning</h2>
        </div>

        <div className="legacy-warning-modal-content">
          <p className="legacy-warning-modal-body">
            This course, <strong>{course?.name || 'this course'}</strong>, is part of our 30,000+ course library and was created using Legacy Modeling Data. It may feature lower resolution textures and simplified graphics compared to our premium courses.
          </p>
        </div>

        <div className="legacy-warning-modal-checkbox">
          <label>
            <input
              type="checkbox"
              checked={dontShowAgain}
              onChange={(e) => setDontShowAgain(e.target.checked)}
            />
            <span>Don't show this warning again for Legacy Courses</span>
          </label>
        </div>

        <div className="legacy-warning-modal-actions">
          <button
            className="legacy-warning-btn legacy-warning-btn-primary"
            onClick={handleProceed}
          >
            Play Anyway (I Understand)
          </button>
          <button
            className="legacy-warning-btn legacy-warning-btn-secondary"
            onClick={handleCancel}
          >
            Return to Premium Courses
          </button>
        </div>
      </div>
    </div>
  )
}

export default LegacyWarningModal

