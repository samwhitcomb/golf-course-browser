import React from 'react'
import './SearchBar.css'

function SearchBar({ onSearch, placeholder = "Search courses...", value = "" }) {
  const handleChange = (e) => {
    const value = e.target.value
    onSearch(value)
  }

  const handleClear = () => {
    onSearch('')
  }

  const hasValue = value && value.length > 0

  return (
    <div className="search-bar-container">
      <input
        type="text"
        className="search-input"
        placeholder={placeholder}
        value={value}
        onChange={handleChange}
      />
      {hasValue ? (
        <button
          className="search-clear-button"
          onClick={handleClear}
          aria-label="Clear search"
          type="button"
        >
          ✕
        </button>
      ) : (
        <span className="search-icon">🔍</span>
      )}
    </div>
  )
}

export default SearchBar

