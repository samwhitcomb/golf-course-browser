import React from 'react'
import { upgradeToStudio } from '../utils/subscription'
import './UpgradeModal.css'

function UpgradeModal({ onClose, onUpgrade, onPlayStandard, course }) {
  const handleUpgrade = () => {
    // In a real app, this would trigger payment/subscription API
    // For demo, we'll use localStorage
    upgradeToStudio()
    if (onUpgrade) {
      onUpgrade()
    }
    onClose()
    // Refresh page or update state to reflect subscription
    window.location.reload()
  }

  const handleStartTrial = () => {
    // Start free trial
    upgradeToStudio()
    if (onUpgrade) {
      onUpgrade()
    }
    onClose()
    window.location.reload()
  }

  return (
    <div className="upgrade-modal-backdrop" onClick={onClose}>
      <div className="upgrade-modal" onClick={e => e.stopPropagation()}>
        <button className="upgrade-modal-close" onClick={onClose}>×</button>
        
        <div className="upgrade-modal-header">
          <h2 className="upgrade-modal-title">Unlock Studios Access</h2>
          <p className="upgrade-modal-subtitle">
            Experience {course?.name || 'this course'} in stunning detail
          </p>
        </div>

        <div className="upgrade-modal-content">
          <div className="upgrade-benefits">
            <h3>Studios Benefits</h3>
            <ul className="benefits-list">
              <li>
                <span className="benefit-icon">✓</span>
                <div>
                  <strong>Lidar Scanned</strong>
                  <p>Sub-centimeter accuracy for true-to-life terrain</p>
                </div>
              </li>
              <li>
                <span className="benefit-icon">✓</span>
                <div>
                  <strong>True 4K Native Textures</strong>
                  <p>Crystal-clear graphics at maximum resolution</p>
                </div>
              </li>
              <li>
                <span className="benefit-icon">✓</span>
                <div>
                  <strong>Advanced Slope Engine</strong>
                  <p>Realistic undulations and physics corrections</p>
                </div>
              </li>
              <li>
                <span className="benefit-icon">✓</span>
                <div>
                  <strong>10x More Topographical Data</strong>
                  <p>Experience courses exactly as they exist in real life</p>
                </div>
              </li>
            </ul>
          </div>

          <div className="upgrade-pricing">
            <div className="pricing-option">
              <div className="pricing-header">
                <h4>Studios Membership</h4>
                <div className="pricing-amount">
                  <span className="pricing-currency">$</span>
                  <span className="pricing-value">9.99</span>
                  <span className="pricing-period">/month</span>
                </div>
              </div>
              <ul className="pricing-features">
                <li>Access to all Studios courses</li>
                <li>Lidar-scanned precision</li>
                <li>4K native textures</li>
                <li>Advanced physics engine</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="upgrade-modal-actions">
          <button
            className="upgrade-btn upgrade-btn-primary"
            onClick={handleStartTrial}
          >
            Start 7-Day Free Trial
          </button>
          <button
            className="upgrade-btn upgrade-btn-secondary"
            onClick={handleUpgrade}
          >
            Upgrade Now
          </button>
          {onPlayStandard && (
            <button
              className="upgrade-btn upgrade-btn-tertiary"
              onClick={onPlayStandard}
            >
              Play in Standard Mode
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default UpgradeModal

