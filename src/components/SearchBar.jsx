import React from 'react'
import './SearchBar.css'

function SearchBar({ onSearch, placeholder = "Search courses...", value = "" }) {
  const handleChange = (e) => {
    const value = e.target.value
    onSearch(value)
  }

  return (
    <div className="search-bar-container">
      <input
        type="text"
        className="search-input"
        placeholder={placeholder}
        value={value}
        onChange={handleChange}
      />
      <span className="search-icon">🔍</span>
    </div>
  )
}

export default SearchBar

