import React, { useState } from 'react'
import StudioBadge from './StudioBadge'
import './CourseCard.css'

function CourseCard({ course, onClick }) {
  const [isHovered, setIsHovered] = useState(false)

  const getCountryFlag = (location) => {
    const locationLower = location.toLowerCase()
    
    // United Kingdom & Ireland
    if (locationLower.includes('scotland') || locationLower.includes('england') || 
        locationLower.includes('northern ireland') || locationLower.includes('uk')) {
      return '🇬🇧'
    }
    
    // Australia
    if (locationLower.includes('australia') || locationLower.includes('tasmania')) {
      return '🇦🇺'
    }
    
    // New Zealand
    if (locationLower.includes('new zealand')) {
      return '🇳🇿'
    }
    
    // Japan
    if (locationLower.includes('japan') || locationLower.includes('kobe') || 
        locationLower.includes('osaka') || locationLower.includes('saitama')) {
      return '🇯🇵'
    }
    
    // South Korea
    if (locationLower.includes('south korea') || locationLower.includes('jeju')) {
      return '🇰🇷'
    }
    
    // China
    if (locationLower.includes('china') || locationLower.includes('shenzhen')) {
      return '🇨🇳'
    }
    
    // Thailand
    if (locationLower.includes('thailand') || locationLower.includes('pattaya') || 
        locationLower.includes('pathum thani')) {
      return '🇹🇭'
    }
    
    // Spain
    if (locationLower.includes('spain') || locationLower.includes('sotogrande') || 
        locationLower.includes('casares')) {
      return '🇪🇸'
    }
    
    // Portugal
    if (locationLower.includes('portugal') || locationLower.includes('cascais') || 
        locationLower.includes('óbidos')) {
      return '🇵🇹'
    }
    
    // France
    if (locationLower.includes('france') || locationLower.includes('paris') || 
        locationLower.includes('chantilly') || locationLower.includes('mortefontaine')) {
      return '🇫🇷'
    }
    
    // South Africa
    if (locationLower.includes('south africa') || locationLower.includes('george') || 
        locationLower.includes('kleinmond') || locationLower.includes('mpumalanga') || 
        locationLower.includes('sun city')) {
      return '🇿🇦'
    }
    
    // Canada
    if (locationLower.includes('canada') || locationLower.includes('toronto') || 
        locationLower.includes('ancaster') || locationLower.includes('nova scotia') || 
        locationLower.includes('inverness')) {
      return '🇨🇦'
    }
    
    // Mexico
    if (locationLower.includes('mexico') || locationLower.includes('playa del carmen')) {
      return '🇲🇽'
    }
    
    // Dominican Republic
    if (locationLower.includes('dominican') || locationLower.includes('punta cana') || 
        locationLower.includes('cap cana') || locationLower.includes('la romana')) {
      return '🇩🇴'
    }
    
    // Default to USA
    return '🇺🇸'
  }

  const getDifficulty = (rating) => {
    if (rating >= 4.5) return 'Hard'
    if (rating >= 4.0) return 'Moderate'
    return 'Easy'
  }

  return (
    <div
      className={`course-card-browse ${isHovered ? 'hovered' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={onClick}
    >
      <div className="course-card-image-container">
        {course.isStudio && (
          <div className="course-card-studio-badge">
            <StudioBadge variant="card" size="small" />
          </div>
        )}
        {course.hasImage ? (
          <img
            src={course.imageUrl}
            alt={course.name}
            className="course-card-image"
            onError={(e) => {
              console.error(`Failed to load image for ${course.name}:`, course.imageUrl)
              e.target.style.display = 'none'
            }}
          />
        ) : (
          <div className="course-card-placeholder">
            <span>No Image</span>
          </div>
        )}
        {isHovered && (
          <div className="course-card-overlay">
            <div className="course-card-stats">
              {course.type && (
                <div className="stat-item">
                  <span className="stat-label">Type</span>
                  <span className="stat-value">{course.type}</span>
                </div>
              )}
              <div className="stat-item">
                <span className="stat-label">Quality</span>
                {course.isStudio ? (
                  <span className="stat-value studio-premium studio-shimmer-text">LIDAR SCANNED</span>
                ) : (
                  <span className="stat-value">Satellite</span>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="course-card-info">
        <div className="course-card-header">
          <span className="course-card-flag">{getCountryFlag(course.location)}</span>
          <div className="course-card-rating">
            {course.yardage && (
              <span className="course-yardage">{course.yardage.toLocaleString()} yds</span>
            )}
            <span className="rating-stars">★★★★★</span>
            <span className="rating-value">{course.rating.toFixed(1)}</span>
          </div>
        </div>
        <h3 className="course-card-name">{course.name}</h3>
        {course.isStudio && course.hasStandardVersion && (
          <p className="course-card-standard-indicator">Also available in Standard</p>
        )}
        <p className="course-card-location">{course.location}</p>
      </div>
    </div>
  )
}

export default CourseCard
