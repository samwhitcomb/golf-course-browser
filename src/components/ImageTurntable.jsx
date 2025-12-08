import React, { useState, useEffect } from 'react'
import './ImageTurntable.css'

function ImageTurntable({ images }) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isAutoPlaying, setIsAutoPlaying] = useState(false)

  // Filter out null/undefined images
  const validImages = (images || []).filter(img => img)

  useEffect(() => {
    if (isAutoPlaying && validImages.length > 1) {
      const interval = setInterval(() => {
        setCurrentIndex((prev) => (prev + 1) % validImages.length)
      }, 3000) // Change image every 3 seconds
      return () => clearInterval(interval)
    }
  }, [isAutoPlaying, validImages.length])

  if (!validImages || validImages.length === 0) {
    return null
  }

  const goToPrevious = () => {
    setCurrentIndex((prev) => (prev - 1 + validImages.length) % validImages.length)
    setIsAutoPlaying(false)
  }

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % validImages.length)
    setIsAutoPlaying(false)
  }

  const goToImage = (index) => {
    setCurrentIndex(index)
    setIsAutoPlaying(false)
  }

  return (
    <div className="image-turntable">
      <div className="turntable-header">
        <h3 className="turntable-title">Additional Views</h3>
        {validImages.length > 1 && (
          <button
            className={`turntable-autoplay-btn ${isAutoPlaying ? 'active' : ''}`}
            onClick={() => setIsAutoPlaying(!isAutoPlaying)}
            aria-label={isAutoPlaying ? 'Pause slideshow' : 'Play slideshow'}
          >
            {isAutoPlaying ? '⏸' : '▶'}
          </button>
        )}
      </div>
      
      <div className="turntable-container">
        {validImages.length > 1 && (
          <button
            className="turntable-nav turntable-nav-prev"
            onClick={goToPrevious}
            aria-label="Previous image"
          >
            ‹
          </button>
        )}
        
        <div className="turntable-main-image">
          <img
            src={validImages[currentIndex]}
            alt={`Course view ${currentIndex + 1}`}
            className="turntable-image"
          />
          {validImages.length > 1 && (
            <div className="turntable-counter">
              {currentIndex + 1} / {validImages.length}
            </div>
          )}
        </div>

        {validImages.length > 1 && (
          <button
            className="turntable-nav turntable-nav-next"
            onClick={goToNext}
            aria-label="Next image"
          >
            ›
          </button>
        )}
      </div>

      {validImages.length > 1 && (
        <div className="turntable-thumbnails">
          {validImages.map((img, index) => (
            <button
              key={index}
              className={`turntable-thumbnail ${index === currentIndex ? 'active' : ''}`}
              onClick={() => goToImage(index)}
              aria-label={`View image ${index + 1}`}
            >
              <img src={img} alt={`Thumbnail ${index + 1}`} />
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default ImageTurntable


