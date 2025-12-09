import React from 'react'
import { getAssetPath } from '../utils/baseUrl'
import StudioBadge from './StudioBadge'
import './HeroHeader.css'

function HeroHeader({ featuredCourse, onTeeOffClick }) {
  const videoPath = getAssetPath('videos/CHISHOLM PARK GOLF CLUB - FLYOVER TOUR www.helicamfilms.com - Tony Young (1080p, h264).mp4')
  
  const handleTeeOff = () => {
    if (featuredCourse && onTeeOffClick) {
      onTeeOffClick(featuredCourse.id)
    }
  }
  
  return (
    <div className="hero-header">
      <div className="hero-video-container">
        <video
          className="hero-video"
          autoPlay
          loop
          muted
          playsInline
        >
          <source src={videoPath} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <div className="hero-overlay"></div>
      </div>
      <div className="hero-content">
        <div className="hero-text">
          <h2 className="hero-title">Featured Course</h2>
          <div className="hero-course-header">
            <h1 className="hero-course-name">
              {featuredCourse ? featuredCourse.name : 'Chisholm Park Golf Club'}
            </h1>
            <StudioBadge variant="hero" />
          </div>
          <p className="hero-description">
            {featuredCourse ? featuredCourse.description : 'A stunning 18-hole championship links course located on the scenic Otago Peninsula in Dunedin, New Zealand'}
          </p>
          <div className="hero-actions">
            <button 
              className="hero-btn hero-btn-primary"
              onClick={handleTeeOff}
            >
              Tee Off Now
            </button>
            <button className="hero-btn hero-btn-secondary">View Scorecard</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HeroHeader

