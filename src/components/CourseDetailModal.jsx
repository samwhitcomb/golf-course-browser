import React, { useState, useEffect } from 'react'
import StatsBar from './StatsBar'
import ScorecardPreview from './ScorecardPreview'
import CourseMap from './CourseMap'
import StudioBadge from './StudioBadge'
import VersionSelector from './VersionSelector'
import UpgradeModal from './UpgradeModal'
import StarRating from './StarRating'
import { generateMockStats } from '../utils/mockStats'
import { hasStudioAccess } from '../utils/subscription'
import './CourseDetailModal.css'

function CourseDetailModal({ course, onClose, getBlurb, userRating = 0, onRatingChange, isPlayLater, onPlayLaterToggle, onTeeOffClick }) {
  if (!course) return null

  const architect = course.architect || 'Unknown'
  
  // Get all available images (hero + additional)
  const heroImage = course.images?.hero || course.imageUrl
  const additionalImages = course.images?.additional || []
  const allImages = [heroImage, ...additionalImages].filter(Boolean)
  const [selectedImageIndex, setSelectedImageIndex] = useState(0)
  const [activeTab, setActiveTab] = useState('overview')
  const [showUpgradeModal, setShowUpgradeModal] = useState(false)
  const [selectedVersion, setSelectedVersion] = useState(course.isStudio ? 'studio' : 'standard')
  
  const isStudio = course.isStudio || false
  const hasStandardVersion = course.hasStandardVersion || false
  const userHasStudioAccess = hasStudioAccess()
  
  // Default to Studio version if course is Studio (for conversion opportunity)
  useEffect(() => {
    if (isStudio && hasStandardVersion) {
      setSelectedVersion('studio')
    }
  }, [isStudio, hasStandardVersion])
  
  const handleVersionChange = (version) => {
    setSelectedVersion(version)
  }
  
  // Get the currently displayed image
  const currentImage = allImages[selectedImageIndex] || heroImage

  const handleRatingChange = (rating) => {
    if (onRatingChange) {
      onRatingChange(rating)
    }
  }

  const handlePlayLaterClick = (e) => {
    e.stopPropagation()
    if (onPlayLaterToggle) {
      onPlayLaterToggle()
    }
  }

  // Generate mock stats for the course based on selected version
  const stats = generateMockStats(course, selectedVersion)
  
  const handleTeeOffClick = (e) => {
    e.stopPropagation()
    // If Studio version selected and user doesn't have access, show upgrade modal
    if (selectedVersion === 'studio' && !userHasStudioAccess) {
      setShowUpgradeModal(true)
    } else if (onTeeOffClick) {
      onTeeOffClick()
    }
  }
  
  const handlePlayStandardClick = () => {
    setSelectedVersion('standard')
    if (onTeeOffClick) {
      onTeeOffClick()
    }
  }
  
  const handleViewStudioFeatures = () => {
    setSelectedVersion('studio')
    if (!userHasStudioAccess) {
      setShowUpgradeModal(true)
    }
  }
  
  const handlePlayStandardFromModal = () => {
    setShowUpgradeModal(false)
    setSelectedVersion('standard')
    // Play in standard mode - this would trigger standard version play
    if (onTeeOffClick) {
      onTeeOffClick()
    }
  }
  
  // Get video URL for Studio version (flyover video)
  const getVideoUrl = () => {
    // Map Studio course IDs to their video filenames
    const videoMap = {
      'pebble-beach': 'Pebble Beach.mp4',
      'cypress-point': 'Cypress.mp4',
      'tara-iti': 'Tara Iti.mp4',
      'cabot-cliffs': 'Cabbot.mp4'
    }
    
    // Check if course has a mapped video
    if (videoMap[course.id]) {
      return `/videos/${videoMap[course.id]}`
    }
    
    // Fallback to course videoUrl or default pattern
    return course.videoUrl || `/videos/${course.id}.mp4`
  }
  
  const handleVideoClick = (e) => {
    e.stopPropagation()
    // Find the video element - could be e.currentTarget (if clicking video) or need to find it
    let video = e.currentTarget
    if (video.tagName !== 'VIDEO') {
      // If clicking the button, find the video element
      const heroSection = e.currentTarget.closest('.modal-hero')
      video = heroSection?.querySelector('.modal-hero-video')
    }
    
    if (!video) return
    
    if (video.requestFullscreen) {
      video.requestFullscreen()
    } else if (video.webkitRequestFullscreen) {
      video.webkitRequestFullscreen()
    } else if (video.mozRequestFullScreen) {
      video.mozRequestFullScreen()
    } else if (video.msRequestFullscreen) {
      video.msRequestFullscreen()
    } else if (video.webkitEnterFullscreen) {
      // iOS Safari
      video.webkitEnterFullscreen()
    }
  }

  return (
    <div className="modal-backdrop-browse" onClick={onClose}>
      <div className="modal-browse" onClick={e => e.stopPropagation()}>
        <div className="modal-header-actions">
          <button className="modal-close-browse" onClick={onClose}>×</button>
          {onRatingChange && (
            <div className="modal-rating-container">
              <StarRating 
                value={userRating} 
                onChange={handleRatingChange}
              />
            </div>
          )}
        </div>
        
        <div className="modal-hero">
          {selectedVersion === 'studio' && isStudio ? (
            <>
              <video
                src={getVideoUrl()}
                className="modal-hero-video"
                autoPlay
                loop
                muted
                playsInline
                onClick={handleVideoClick}
                style={{ cursor: 'pointer' }}
                title="Click to view fullscreen"
              />
              <div className="hero-disclaimer">In-game footage</div>
              <button 
                className="hero-maximize-btn"
                onClick={handleVideoClick}
                aria-label="View fullscreen"
                title="View fullscreen"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
                </svg>
              </button>
            </>
          ) : (
            currentImage && (
              <>
                <img 
                  src={currentImage} 
                  alt={course.name} 
                  className="modal-hero-image"
                  onError={(e) => {
                    // Try fallback extensions if primary fails
                    const src = e.target.src
                    if (src.includes('_hero.webp')) {
                      e.target.src = src.replace('_hero.webp', '_hero.jpg')
                    } else if (src.includes('_hero.jpg')) {
                      e.target.src = src.replace('_hero.jpg', '_hero.png')
                    } else if (src.includes('_hero.png')) {
                      e.target.src = src.replace('_hero.png', '_hero.jpeg')
                    } else if (src.includes('_1.webp')) {
                      e.target.src = src.replace('_1.webp', '_1.jpg')
                    } else if (src.includes('_1.jpg')) {
                      e.target.src = src.replace('_1.jpg', '_1.png')
                    } else if (src.includes('_2.webp')) {
                      e.target.src = src.replace('_2.webp', '_2.jpg')
                    } else if (src.includes('_2.jpg')) {
                      e.target.src = src.replace('_2.jpg', '_2.png')
                    }
                  }}
                />
                <div className="hero-disclaimer">Not actual course photography</div>
              </>
            )
          )}
          {selectedVersion === 'standard' && allImages.length > 1 && (
            <div className="hero-image-previews">
              {allImages.map((img, index) => (
                <button
                  key={index}
                  className={`hero-preview-thumb ${index === selectedImageIndex ? 'active' : ''}`}
                  onClick={() => setSelectedImageIndex(index)}
                  aria-label={`View image ${index + 1}`}
                >
                  <img 
                    src={img} 
                    alt={`Preview ${index + 1}`}
                    onError={(e) => {
                      // Try fallback extensions
                      const src = e.target.src
                      if (src.includes('_hero.webp')) {
                        e.target.src = src.replace('_hero.webp', '_hero.jpg')
                      } else if (src.includes('_hero.jpg')) {
                        e.target.src = src.replace('_hero.jpg', '_hero.png')
                      } else if (src.includes('_1.webp')) {
                        e.target.src = src.replace('_1.webp', '_1.jpg')
                      } else if (src.includes('_1.jpg')) {
                        e.target.src = src.replace('_1.jpg', '_1.png')
                      } else if (src.includes('_2.webp')) {
                        e.target.src = src.replace('_2.webp', '_2.jpg')
                      } else if (src.includes('_2.jpg')) {
                        e.target.src = src.replace('_2.jpg', '_2.png')
                      }
                    }}
                  />
                </button>
              ))}
            </div>
          )}
          <div className="modal-hero-overlay">
            <div className="modal-hero-header">
              <div className="modal-title-container">
                <h1 className="modal-title">{course.name}</h1>
                {isStudio && <StudioBadge variant="modal" size="medium" />}
              </div>
            </div>
            <div className="modal-meta">
              <span className="modal-location">{course.location}</span>
              <div className="modal-ratings">
                <span className="modal-rating">Global: ★ {course.rating.toFixed(1)}</span>
                {userRating > 0 && (
                  <span className="modal-user-rating">Your Rating: {userRating}/5</span>
                )}
              </div>
            </div>
            {onTeeOffClick && (
              <div className="modal-actions">
                {isStudio && hasStandardVersion ? (
                  <>
                    {selectedVersion === 'studio' ? (
                      <>
                        {!userHasStudioAccess ? (
                          <>
                            <button
                              className="modal-tee-off-btn modal-upgrade-btn"
                              onClick={handleTeeOffClick}
                            >
                              Upgrade to Studio & Play
                            </button>
                            <button
                              className="modal-play-later-btn"
                              onClick={handlePlayStandardClick}
                            >
                              Play Standard Version
                            </button>
                          </>
                        ) : (
                          <>
                            <button
                              className="modal-tee-off-btn modal-upgrade-btn"
                              onClick={handleTeeOffClick}
                            >
                              Tee Off Now (Studio)
                            </button>
                            <button
                              className="modal-secondary-btn"
                              onClick={handlePlayStandardClick}
                            >
                              Play Standard Version
                            </button>
                          </>
                        )}
                      </>
                    ) : (
                      <>
                        <button
                          className="modal-tee-off-btn"
                          onClick={handleTeeOffClick}
                        >
                          Tee Off Now (Standard)
                        </button>
                            <button
                              className="modal-secondary-btn"
                              onClick={handleViewStudioFeatures}
                            >
                              View Studio Features
                            </button>
                      </>
                    )}
                  </>
                ) : (
                  <>
                    <button
                      className={`modal-tee-off-btn ${isStudio ? 'modal-upgrade-btn' : ''}`}
                      onClick={handleTeeOffClick}
                    >
                      Tee Off Now
                    </button>
                    {onPlayLaterToggle && (
                      <button
                        className={`modal-play-later-btn ${isPlayLater ? 'active' : ''}`}
                        onClick={handlePlayLaterClick}
                      >
                        {isPlayLater ? '✓ Play Later' : 'Play Later'}
                      </button>
                    )}
                  </>
                )}
              </div>
            )}
          </div>
        </div>

        {isStudio && hasStandardVersion && (
          <VersionSelector
            selectedVersion={selectedVersion}
            onVersionChange={handleVersionChange}
            isStudio={isStudio}
            hasStandardVersion={hasStandardVersion}
          />
        )}

        <StatsBar course={course} stats={stats} />

        <div className="modal-tabs">
          <button
            className={`modal-tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button
            className={`modal-tab ${activeTab === 'scorecard' ? 'active' : ''}`}
            onClick={() => setActiveTab('scorecard')}
          >
            Scorecard
          </button>
          <button
            className={`modal-tab ${activeTab === 'map' ? 'active' : ''}`}
            onClick={() => setActiveTab('map')}
          >
            Map
          </button>
        </div>

        <div className="modal-content">
          {activeTab === 'overview' && (
            <>
             

              <div className="modal-section">
                <h2 className="section-title">About</h2>
                <div className="section-content">
                  {getBlurb && getBlurb(course).map((p, idx) => (
                    <p key={idx} className="course-description-text">{p}</p>
                  ))}
                </div>
              </div>

              <div className="modal-section">
                <div className="section-content">
                  <div className="info-item">
                    <strong>Architect:</strong> {architect}
                  </div>
                  <div className="info-item">
                    <strong>Established:</strong> {course.established || 'N/A'}
                  </div>
                </div>
              </div>

              {isStudio && hasStandardVersion && (
                <div className="modal-section">
                  <h2 className="section-title">Version Comparison</h2>
                  <div className="section-content">
                    <div className="version-comparison-table">
                      <div className="comparison-header">
                        <div className="comparison-cell header">Feature</div>
                        <div className="comparison-cell header">Standard Version</div>
                        <div className="comparison-cell header studio-header">Studio Version</div>
                      </div>
                      <div className="comparison-row">
                        <div className="comparison-cell label">Mapping</div>
                        <div className="comparison-cell">{course.standardFeatures?.mappingType || 'Satellite'} ({course.standardFeatures?.accuracy || '1m'})</div>
                        <div className="comparison-cell studio-cell">{course.studioFeatures?.mappingType || 'Lidar'} ({course.studioFeatures?.accuracy || 'Sub-Centimeter'})</div>
                      </div>
                      <div className="comparison-row">
                        <div className="comparison-cell label">Graphics</div>
                        <div className="comparison-cell">{course.standardFeatures?.resolution || 'HD (1080p)'}</div>
                        <div className="comparison-cell studio-cell">{course.studioFeatures?.resolution || 'True 4K Native'}</div>
                      </div>
                      <div className="comparison-row">
                        <div className="comparison-cell label">Physics</div>
                        <div className="comparison-cell">{course.standardFeatures?.physics || 'Standard Terrain Model'}</div>
                        <div className="comparison-cell studio-cell">{course.studioFeatures?.physics || 'Advanced Slope Engine'}</div>
                      </div>
                      <div className="comparison-row">
                        <div className="comparison-cell label">File Size</div>
                        <div className="comparison-cell">{course.standardFeatures?.fileSize || '500 MB'}</div>
                        <div className="comparison-cell studio-cell">{course.studioFeatures?.fileSize || '5 GB'}</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div className="modal-section">
                <h2 className="section-title">Tech Specs</h2>
                <div className="section-content">
                  <div className="tech-badges">
                    {selectedVersion === 'studio' ? (
                      <>
                        <span className="tech-badge studio-badge studio-shimmer">Lidar Scanned</span>
                        <span className="tech-badge studio-badge">4K Resolution</span>
                        <span className="tech-badge studio-badge">Advanced Physics</span>
                      </>
                    ) : (
                      <>
                        <span className="tech-badge">Satellite Mapped</span>
                        <span className="tech-badge">HD Resolution</span>
                        <span className="tech-badge">Standard Physics</span>
                      </>
                    )}
                    <span className="tech-badge">2024 Update</span>
                  </div>
                  {selectedVersion === 'studio' && (
                    <div className="tech-specs-detail">
                      <p><strong>Mapping:</strong> {course.studioFeatures?.mappingType || 'Lidar'} ({course.studioFeatures?.accuracy || 'Sub-Centimeter Accuracy'})</p>
                      <p><strong>Resolution:</strong> {course.studioFeatures?.resolution || 'True 4K Native Textures'}</p>
                      <p><strong>Physics:</strong> {course.studioFeatures?.physics || 'Advanced Slope Engine (Realistic Undulations)'}</p>
                    </div>
                  )}
                  {selectedVersion === 'standard' && isStudio && (
                    <div className="tech-specs-detail">
                      <p><strong>Mapping:</strong> {course.standardFeatures?.mappingType || 'Satellite'} ({course.standardFeatures?.accuracy || '1m Accuracy'})</p>
                      <p><strong>Resolution:</strong> {course.standardFeatures?.resolution || 'HD Textures (1080p)'}</p>
                      <p><strong>Physics:</strong> {course.standardFeatures?.physics || 'Standard Terrain Model'}</p>
                    </div>
                  )}
                </div>
              </div>

              <div className="modal-section">
                <h2 className="section-title">User Reviews</h2>
                <div className="section-content">
                  <div className="player-tips">
                    <p className="tips-placeholder">Player tips and reviews coming soon</p>
                  </div>
                </div>
              </div>

              {(course.batch || course.type) && (
                <div className="modal-section">
                  <h2 className="section-title">Tags</h2>
                  <div className="section-content">
                    <div className="tags-container-browse">
                      {course.type && (
                        <span className="tag-browse tag-type">{course.type}</span>
                      )}
                      {course.batch && (
                        <span className="tag-browse tag-batch">{course.batch}</span>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </>
          )}

          {activeTab === 'scorecard' && (
            <div className="tab-content-scorecard">
              <ScorecardPreview course={course} />
            </div>
          )}

          {activeTab === 'map' && (
            <div className="tab-content-map">
              <CourseMap course={course} />
            </div>
          )}
        </div>

        {showUpgradeModal && (
          <UpgradeModal
            onClose={() => setShowUpgradeModal(false)}
            onUpgrade={() => {
              // In a real app, this would trigger payment/subscription flow
              // For demo, we'll just close and show success
              setShowUpgradeModal(false)
              alert('Upgrade flow would start here. For demo, you can manually set subscription in browser console: localStorage.setItem("rapsodo_subscription", JSON.stringify({tier: "studio"}))')
            }}
            onPlayStandard={handlePlayStandardFromModal}
            course={course}
          />
        )}
      </div>
    </div>
  )
}

export default CourseDetailModal

