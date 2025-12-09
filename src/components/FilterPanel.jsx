import React from 'react'
import './FilterPanel.css'

function FilterPanel({ filters, onFilterChange }) {
  const moodFilters = [
    { id: 'chill', label: 'Chill', description: 'Wide fairways, easy greens' },
    { id: 'challenge', label: 'Challenge', description: 'Tight fairways, deep rough, fast greens' },
    { id: 'practice', label: 'Practice', description: 'Driving ranges and short game' },
  ]

  const typeFilters = [
    { id: 'links', label: 'Links' },
    { id: 'parkland', label: 'Parkland' },
    { id: 'coastal', label: 'Coastal' },
    { id: 'desert', label: 'Desert' },
    { id: 'mountain', label: 'Mountain' },
    { id: 'championship', label: 'Championship' },
  ]

  const continentFilters = [
    { id: 'North America', label: 'North America' },
    { id: 'Europe', label: 'Europe' },
    { id: 'Oceania', label: 'Oceania' },
    { id: 'Asia', label: 'Asia' },
    { id: 'South America', label: 'South America' },
    { id: 'Africa', label: 'Africa' },
    { id: 'Middle East', label: 'Middle East' },
  ]

  const contentTierFilters = [
    { id: 'all', label: 'All Courses' },
    { id: 'free', label: 'Free' },
    { id: 'studio', label: 'Studio' },
  ]

  return (
    <div className="filter-panel">
      <div className="filter-section">
        <h3 className="filter-section-title">Content Tier</h3>
        <div className="filter-buttons">
          {contentTierFilters.map(filter => (
            <button
              key={filter.id}
              className={`filter-button ${filters.contentTier === filter.id ? 'active' : ''}`}
              onClick={() => onFilterChange('contentTier', filter.id)}
            >
              {filter.label}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-section">
        <h3 className="filter-section-title">Continent</h3>
        <div className="filter-buttons">
          {continentFilters.map(filter => (
            <button
              key={filter.id}
              className={`filter-button ${filters.continent === filter.id ? 'active' : ''}`}
              onClick={() => onFilterChange('continent', filter.id)}
            >
              {filter.label}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-section">
        <h3 className="filter-section-title">Mood</h3>
        <div className="filter-buttons">
          {moodFilters.map(filter => (
            <button
              key={filter.id}
              className={`filter-button ${filters.mood === filter.id ? 'active' : ''}`}
              onClick={() => onFilterChange('mood', filter.id)}
              title={filter.description}
            >
              {filter.label}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-section">
        <h3 className="filter-section-title">Type</h3>
        <div className="filter-buttons">
          {typeFilters.map(filter => (
            <button
              key={filter.id}
              className={`filter-button ${filters.type === filter.id ? 'active' : ''}`}
              onClick={() => onFilterChange('type', filter.id)}
            >
              {filter.label}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-actions">
        <button
          className="filter-clear"
          onClick={() => onFilterChange('clear', null)}
        >
          Clear Filters
        </button>
      </div>
    </div>
  )
}

export default FilterPanel

