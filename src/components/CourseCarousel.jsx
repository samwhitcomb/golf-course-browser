import React, { useRef, useState } from 'react'
import CourseCard from './CourseCard'
import './CourseCarousel.css'

function CourseCarousel({ title, description, courses, onCourseClick }) {
  const carouselRef = useRef(null)
  const [showTooltip, setShowTooltip] = useState(false)

  const scroll = (direction) => {
    const container = carouselRef.current
    if (!container) return
    
    const scrollAmount = 400
    container.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth'
    })
  }

  if (!courses || courses.length === 0) {
    return null
  }

  return (
    <div className="carousel-section">
      <div className="carousel-header">
        <div className="carousel-title-section">
          <h2 
            className="carousel-title"
            onMouseEnter={() => description && setShowTooltip(true)}
            onMouseLeave={() => setShowTooltip(false)}
          >
            {title}
            {description && showTooltip && (
              <div className="carousel-tooltip">
                <div className="tooltip-arrow"></div>
                <p className="tooltip-text">{description}</p>
              </div>
            )}
          </h2>
        </div>
        <div className="carousel-controls">
          <button 
            className="carousel-arrow carousel-arrow-left"
            onClick={() => scroll('left')}
            aria-label="Scroll left"
          >
            ‹
          </button>
          <button 
            className="carousel-arrow carousel-arrow-right"
            onClick={() => scroll('right')}
            aria-label="Scroll right"
          >
            ›
          </button>
        </div>
      </div>
      <div className="carousel-container" ref={carouselRef}>
        <div className="carousel-track">
          {courses.map((item, index) => {
            if (item.type === 'divider') {
              return (
                <div key={`divider-${index}`} className="carousel-divider">
                  <div className="carousel-divider-line"></div>
                  <span className="carousel-divider-label">{item.label}</span>
                  <div className="carousel-divider-line"></div>
                </div>
              )
            }
            return (
              <CourseCard
                key={item.id}
                course={item}
                onClick={() => onCourseClick(item)}
              />
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default CourseCarousel

