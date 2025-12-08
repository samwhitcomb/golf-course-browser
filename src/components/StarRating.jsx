import React, { useState } from 'react'
import './StarRating.css'

function StarRating({ value = 0, onChange, readOnly = false }) {
  const [hoverValue, setHoverValue] = useState(0)

  const handleStarClick = (rating) => {
    if (!readOnly && onChange) {
      onChange(rating)
    }
  }

  const handleStarHover = (rating) => {
    if (!readOnly) {
      setHoverValue(rating)
    }
  }

  const handleMouseLeave = () => {
    if (!readOnly) {
      setHoverValue(0)
    }
  }

  const displayValue = hoverValue || value

  return (
    <div 
      className={`star-rating ${readOnly ? 'read-only' : ''}`}
      onMouseLeave={handleMouseLeave}
    >
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          type="button"
          className={`star ${star <= displayValue ? 'filled' : 'empty'}`}
          onClick={() => handleStarClick(star)}
          onMouseEnter={() => handleStarHover(star)}
          disabled={readOnly}
          aria-label={`Rate ${star} star${star !== 1 ? 's' : ''}`}
        >
          ★
        </button>
      ))}
    </div>
  )
}

export default StarRating

