import React, { useState, useEffect, useRef } from 'react'
import HeroHeader from './components/HeroHeader'
import CourseCarousel from './components/CourseCarousel'
import CourseCard from './components/CourseCard'
import CourseDetailModal from './components/CourseDetailModal'
import CarouselSwitcher from './components/CarouselSwitcher'
import SearchBar from './components/SearchBar'
import FilterPanel from './components/FilterPanel'
import MapView from './components/MapView'
import { getBlurb } from './utils/blurbUtils'
import { setLastPlayed, getLastPlayed, getPlayLater, togglePlayLater, isPlayLater, getRatings, setRating, getRating, migrateFavoritesToRatings } from './utils/userPreferences'
import { getAssetPath } from './utils/baseUrl'
import './BrowseApp.css'

function BrowseApp() {
  const [courses, setCourses] = useState([])
  const [filteredCourses, setFilteredCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCourse, setSelectedCourse] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState({ continent: null, mood: null, type: null, contentTier: null })
  const [showFilters, setShowFilters] = useState(false)
  const [showMapView, setShowMapView] = useState(false)
  const [activeTab, setActiveTab] = useState('smart')
  const [ratings, setRatings] = useState(new Map())
  const [playLater, setPlayLater] = useState(new Set())
  const headerRef = useRef(null)

  useEffect(() => {
    fetchCourses()
    // Migrate favorites to ratings on first load
    migrateFavoritesToRatings()
    // Load ratings and play later from localStorage
    setRatings(getRatings())
    setPlayLater(getPlayLater())
    
    const handleScroll = () => {
      if (headerRef.current) {
        if (window.scrollY > 50) {
          headerRef.current.classList.add('scrolled')
        } else {
          headerRef.current.classList.remove('scrolled')
        }
      }
    }
    
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    applyFilters()
  }, [courses, searchQuery, filters])

  const fetchCourses = async () => {
    try {
      setLoading(true)
      const response = await fetch(getAssetPath('courses.json'))
      if (!response.ok) throw new Error('Failed to fetch courses')
      const data = await response.json()
      
      // Process image URLs to include base path
      const processedData = data.map(course => {
        if (course.imageUrl && course.imageUrl.startsWith('/')) {
          course.imageUrl = getAssetPath(course.imageUrl.slice(1))
        }
        if (course.images) {
          if (course.images.hero && course.images.hero.startsWith('/')) {
            course.images.hero = getAssetPath(course.images.hero.slice(1))
          }
          if (course.images.additional) {
            course.images.additional = course.images.additional.map(img => 
              img.startsWith('/') ? getAssetPath(img.slice(1)) : getAssetPath(img)
            )
          }
        }
        return course
      })
      
      setCourses(processedData)
    } catch (err) {
      console.error('Error fetching courses:', err)
    } finally {
      setLoading(false)
    }
  }

  const applyFilters = () => {
    let filtered = [...courses]

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      // If searching for "studio" or "studios", include all Studio courses
      if (query === 'studio' || query === 'studios') {
        filtered = filtered.filter(course => course.isStudio === true)
      } else {
        filtered = filtered.filter(course =>
          course.name.toLowerCase().includes(query) ||
          course.location.toLowerCase().includes(query) ||
          course.description?.toLowerCase().includes(query) ||
          (query.includes('studio') && course.isStudio === true)
        )
      }
    }

    // Mood filter
    if (filters.mood) {
      if (filters.mood === 'chill') {
        filtered = filtered.filter(c => c.rating < 4.0 || c.type === 'resort')
      } else if (filters.mood === 'challenge') {
        filtered = filtered.filter(c => c.rating >= 4.5 || c.type === 'championship')
      } else if (filters.mood === 'practice') {
        // Placeholder - would filter for practice facilities
        filtered = filtered.filter(c => c.type === 'parkland')
      }
    }

    // Type filter
    if (filters.type) {
      filtered = filtered.filter(c => c.type === filters.type)
    }

    // Continent filter
    if (filters.continent) {
      filtered = filtered.filter(c => c.continent === filters.continent)
    }

    // Content Tier filter
    if (filters.contentTier === 'studio') {
      filtered = filtered.filter(c => c.isStudio === true)
    } else if (filters.contentTier === 'free') {
      filtered = filtered.filter(c => !c.isStudio || c.isStudio === false)
    }
    // 'all' or null shows everything

    setFilteredCourses(filtered)
  }

  const handleFilterChange = (filterType, value) => {
    if (filterType === 'clear') {
      setFilters({ continent: null, mood: null, type: null, contentTier: null })
      setSearchQuery('')
    } else {
      setFilters(prev => ({
        ...prev,
        [filterType]: prev[filterType] === value ? null : value
      }))
    }
  }

  const handleSearch = (query) => {
    setSearchQuery(query)
  }

  const handleCourseClick = (course) => {
    setSelectedCourse(course)
  }

  const closeModal = () => {
    setSelectedCourse(null)
  }

  const handleRatingChange = (courseId, rating) => {
    setRating(courseId, rating)
    // Update ratings state
    setRatings(new Map(getRatings()))
  }

  const handlePlayLaterToggle = (courseId) => {
    togglePlayLater(courseId)
    // Force re-render by creating new Set reference
    setPlayLater(new Set(getPlayLater()))
  }

  const handleCoursePlay = (courseId) => {
    setLastPlayed(courseId)
    // Update playLater state after course is played (it gets removed automatically)
    setPlayLater(new Set(getPlayLater()))
  }

  const handleMapCourseClick = (course) => {
    setShowMapView(false)
    handleCourseClick(course)
  }

  // Get smart list carousels
  const getSmartListCarousels = () => {
    // Use filtered courses if filters are active (but not when searching, since search has its own overlay)
    const hasActiveFilters = filters.continent || filters.mood || filters.type || filters.contentTier
    const coursesToUse = (hasActiveFilters && !searchQuery) ? filteredCourses : courses
    const allCourses = coursesToUse.filter(c => c.hasImage)
    const lastPlayedId = getLastPlayed()
    // Default to St. Andrews if no last played course
    const lastPlayedCourse = lastPlayedId 
      ? courses.find(c => c.id === lastPlayedId) 
      : courses.find(c => c.id === 'st-andrews') || null
    
    // Trending Now - First 4 should be Studio courses, then by rating
    const studioCourses = allCourses.filter(c => c.isStudio === true)
    const nonStudioCourses = allCourses.filter(c => !c.isStudio || c.isStudio === false)
    
    // Sort Studio courses by rating, then non-Studio courses by rating
    const sortedStudio = studioCourses.sort((a, b) => b.rating - a.rating)
    const sortedNonStudio = nonStudioCourses.sort((a, b) => b.rating - a.rating)
    
    // First 4 from Studio courses, then fill remaining slots from non-Studio
    const trending = [
      ...sortedStudio.slice(0, 4),
      ...sortedNonStudio.slice(0, 6)
    ].slice(0, 10)
    
    // Because you played...
    let becauseYouPlayed = []
    if (lastPlayedCourse) {
      becauseYouPlayed = allCourses
        .filter(c => {
          if (c.id === lastPlayedCourse.id) return false
          // Similar type (preferred)
          const sameType = c.type === lastPlayedCourse.type
          // Similar rating (±0.5)
          const similarRating = Math.abs(c.rating - lastPlayedCourse.rating) <= 0.5
          // Same continent (preferred)
          const sameContinent = c.continent === lastPlayedCourse.continent
          
          // Prioritize: same type + similar rating, or same continent + similar rating
          return (sameType && similarRating) || (sameContinent && similarRating)
        })
        .sort((a, b) => {
          // Sort by: same type first, then same continent, then by rating
          const aSameType = a.type === lastPlayedCourse.type ? 1 : 0
          const bSameType = b.type === lastPlayedCourse.type ? 1 : 0
          const aSameContinent = a.continent === lastPlayedCourse.continent ? 1 : 0
          const bSameContinent = b.continent === lastPlayedCourse.continent ? 1 : 0
          
          if (aSameType !== bSameType) return bSameType - aSameType
          if (aSameContinent !== bSameContinent) return bSameContinent - aSameContinent
          return b.rating - a.rating
        })
        .slice(0, 10)
    }
    
    // Play Later
    const playLaterList = allCourses
      .filter(c => playLater.has(c.id))
      .sort((a, b) => b.rating - a.rating)
    
    // Rated Courses - sorted by rating with tier dividers (inline in carousel)
    const ratedCoursesList = (() => {
      const ratedCourseIds = Array.from(ratings.keys())
      if (ratedCourseIds.length === 0) return []
      
      // Get all rated courses with their ratings
      const ratedCourses = allCourses
        .filter(c => ratings.has(c.id))
        .map(c => ({
          ...c,
          userRating: ratings.get(c.id)
        }))
        .sort((a, b) => b.userRating - a.userRating) // Sort highest to lowest
      
      // Group by rating tier
      const grouped = {
        5: [],
        4: [],
        3: [],
        2: [],
        1: []
      }
      
      ratedCourses.forEach(course => {
        const rating = course.userRating
        if (rating >= 1 && rating <= 5) {
          grouped[rating].push(course)
        }
      })
      
      // Build array with dividers inline (including 5-star at start)
      const result = []
      const tiers = [5, 4, 3, 2, 1]
      
      tiers.forEach(tier => {
        if (grouped[tier].length > 0) {
          result.push({ type: 'divider', label: `${tier} Stars` })
          result.push(...grouped[tier])
        }
      })
      
      return result
    })()
    
    // For You recommendations
    let forYou = []
    if (ratings.size > 0) {
      // Find courses similar to rated courses
      const ratedCourses = allCourses.filter(c => ratings.has(c.id))
      const avgRating = ratedCourses.reduce((sum, c) => sum + c.rating, 0) / ratedCourses.length
      const ratedTypes = new Set(ratedCourses.map(c => c.type).filter(Boolean))
      const ratedContinents = new Set(ratedCourses.map(c => c.continent).filter(Boolean))
      
      forYou = allCourses
        .filter(c => {
          if (ratings.has(c.id)) return false
          // Similar rating to average rated course (±0.5)
          const similarRating = Math.abs(c.rating - avgRating) <= 0.5
          // Same type as a rated course, or same continent
          const matchesType = ratedTypes.has(c.type)
          const matchesContinent = ratedContinents.has(c.continent)
          
          return similarRating && (matchesType || matchesContinent)
        })
        .sort((a, b) => {
          // Prioritize: same type, then same continent, then by rating
          const aMatchesType = ratedTypes.has(a.type) ? 1 : 0
          const bMatchesType = ratedTypes.has(b.type) ? 1 : 0
          const aMatchesContinent = ratedContinents.has(a.continent) ? 1 : 0
          const bMatchesContinent = ratedContinents.has(b.continent) ? 1 : 0
          
          if (aMatchesType !== bMatchesType) return bMatchesType - aMatchesType
          if (aMatchesContinent !== bMatchesContinent) return bMatchesContinent - aMatchesContinent
          return b.rating - a.rating
        })
        .slice(0, 15)
    } else if (lastPlayedCourse) {
      // Use last played as seed if no rated courses
      forYou = allCourses
        .filter(c => {
          if (c.id === lastPlayedCourse.id) return false
          const similarRating = Math.abs(c.rating - lastPlayedCourse.rating) <= 0.5
          return similarRating
        })
        .sort((a, b) => b.rating - a.rating)
        .slice(0, 15)
    } else {
      // Default: moderate difficulty courses
      forYou = allCourses
        .filter(c => c.rating >= 4.0 && c.rating <= 4.5)
        .sort((a, b) => b.rating - a.rating)
        .slice(0, 15)
    }
    
    return {
      trending,
      becauseYouPlayed,
      playLaterList,
      ratedCoursesList,
      forYou,
      lastPlayedCourse
    }
  }
  
  // Get curated carousels
  const getCuratedCarousels = () => {
    // Use filtered courses if filters are active (but not when searching, since search has its own overlay)
    const hasActiveFilters = filters.continent || filters.mood || filters.type || filters.contentTier
    const coursesToUse = (hasActiveFilters && !searchQuery) ? filteredCourses : courses
    const allCourses = coursesToUse.filter(c => c.hasImage)
    
    return {
      absoluteIcons: allCourses
        .filter(c => c.batch === 'Absolute Icons & Major Venues')
        .sort((a, b) => b.rating - a.rating),
      premierLinks: allCourses
        .filter(c => c.batch === 'Premier Global Links & Sandbelt')
        .sort((a, b) => b.rating - a.rating),
      goldenAge: allCourses
        .filter(c => c.batch === 'Classic American Golden Age Designs')
        .sort((a, b) => b.rating - a.rating),
      historicInternational: allCourses
        .filter(c => c.batch === 'Historic & Championship International Links')
        .sort((a, b) => b.rating - a.rating),
      modernIcons: allCourses
        .filter(c => c.batch === 'Modern American Icons & Stadium Courses')
        .sort((a, b) => b.rating - a.rating),
      destinationResort: allCourses
        .filter(c => c.batch === 'Destination & Scenic Resort Courses')
        .sort((a, b) => b.rating - a.rating),
      desertMountain: allCourses
        .filter(c => c.batch === 'Desert & Mountain Classics')
        .sort((a, b) => b.rating - a.rating),
      strategicArtistic: allCourses
        .filter(c => c.batch === 'Strategic & Artistic Gems')
        .sort((a, b) => b.rating - a.rating),
      international: allCourses
        .filter(c => c.continent && c.continent !== 'North America' && c.continent !== 'Unknown')
        .sort((a, b) => b.rating - a.rating),
      studioOriginals: allCourses
        .filter(c => c.isStudio === true)
        .sort((a, b) => b.rating - a.rating),
    }
  }

  if (loading) {
    return (
      <div className="browse-app">
        <div className="loading-screen">Loading courses...</div>
      </div>
    )
  }

  // Use null to trigger fallback to Chisholm Park Golf Club in HeroHeader
  const featuredCourse = null

  return (
    <div className="browse-app">
      <div className="browse-header" ref={headerRef}>
        <h1>Rapsodo Courses</h1>
        <div className="header-search">
          <SearchBar 
            onSearch={handleSearch} 
            placeholder="Search courses..."
            value={searchQuery}
          />
        </div>
        <div className="header-actions">
          <button
            className="globe-button"
            onClick={() => setShowMapView(true)}
            aria-label="View map"
            title="View courses on map"
          >
            🌍
          </button>
          <button
            className="filter-toggle"
            onClick={() => setShowFilters(!showFilters)}
          >
            {showFilters ? 'Hide' : 'Show'} Filters
          </button>
        </div>
      </div>

      {showFilters && (
        <div className="filters-container">
          <div className="filters-content">
            <FilterPanel filters={filters} onFilterChange={handleFilterChange} />
          </div>
        </div>
      )}

      {searchQuery && (
        <div className="search-results-overlay">
          <div className="search-results-container">
            <div className="search-results-header">
              <h2>Search Results for "{searchQuery}"</h2>
              <button 
                className="clear-search-btn"
                onClick={() => setSearchQuery('')}
                aria-label="Clear search"
              >
                Clear Search
              </button>
            </div>
            <div className="search-results-grid">
              {filteredCourses.length > 0 ? (
                filteredCourses.map(course => (
                  <div key={course.id} className="search-result-card">
                    <CourseCard
                      course={course}
                      onClick={() => handleCourseClick(course)}
                    />
                  </div>
                ))
              ) : (
                <div className="no-results">
                  <p>No courses found matching "{searchQuery}"</p>
                  <button 
                    className="clear-search-btn"
                    onClick={() => setSearchQuery('')}
                  >
                    Clear Search
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      <div className={`main-content ${searchQuery ? 'dimmed' : ''}`}>
        <HeroHeader 
          featuredCourse={featuredCourse}
          onTeeOffClick={handleCoursePlay}
        />

        <div className="browse-content">
          <CarouselSwitcher 
            activeTab={activeTab} 
            onTabChange={setActiveTab} 
          />

          {activeTab === 'smart' && (() => {
            const smartCarousels = getSmartListCarousels()
            return (
              <>
                {smartCarousels.trending.length > 0 && (
                  <CourseCarousel
                    title="Trending Now"
                    courses={smartCarousels.trending}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {smartCarousels.becauseYouPlayed.length > 0 && smartCarousels.lastPlayedCourse && (
                  <CourseCarousel
                    title={`Because you played ${smartCarousels.lastPlayedCourse.name}`}
                    description="Similar courses with a similar difficulty"
                    courses={smartCarousels.becauseYouPlayed}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {smartCarousels.playLaterList.length > 0 && (
                  <CourseCarousel
                    title="Play Later"
                    courses={smartCarousels.playLaterList}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {smartCarousels.ratedCoursesList.length > 0 && (
                  <CourseCarousel
                    title="Rated Courses"
                    courses={smartCarousels.ratedCoursesList}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {smartCarousels.forYou.length > 0 && (
                  <CourseCarousel
                    title="For You"
                    courses={smartCarousels.forYou}
                    onCourseClick={handleCourseClick}
                  />
                )}
              </>
            )
          })()}

          {activeTab === 'curated' && (() => {
            const curatedCarousels = getCuratedCarousels()
            return (
              <>
                {curatedCarousels.absoluteIcons.length > 0 && (
                  <CourseCarousel
                    title="Absolute Icons & Major Venues"
                    description="The most historically significant and globally recognized championship courses, each a foundational pillar of golf's story."
                    courses={curatedCarousels.absoluteIcons}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {curatedCarousels.premierLinks.length > 0 && (
                  <CourseCarousel
                    title="Premier Global Links & Sandbelt"
                    description="The world's finest links and the unique sandbelt style, where firm, fast-running ground and strategic design create the purest forms of the game."
                    courses={curatedCarousels.premierLinks}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {curatedCarousels.goldenAge.length > 0 && (
                  <CourseCarousel
                    title="Classic American Golden Age Designs"
                    description="The foundational inland masterpieces of the early 20th century, showcasing the strategic genius of architects like Tillinghast, Ross, Raynor, and MacKenzie."
                    courses={curatedCarousels.goldenAge}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {curatedCarousels.historicInternational.length > 0 && (
                  <CourseCarousel
                    title="Historic & Championship International Links"
                    description="Legendary Open Championship venues and other historic links from the British Isles, where golf's oldest major has been defined by wind, bunkers, and dramatic finishes."
                    courses={curatedCarousels.historicInternational}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {curatedCarousels.modernIcons.length > 0 && (
                  <CourseCarousel
                    title="Modern American Icons & Stadium Courses"
                    description="Influential and often dramatic designs from the late 20th and 21st centuries that have become major championship venues and bucket-list destinations."
                    courses={curatedCarousels.modernIcons}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {curatedCarousels.destinationResort.length > 0 && (
                  <CourseCarousel
                    title="Destination & Scenic Resort Courses"
                    description="World-class golf at destination resorts, where course design is masterfully integrated with stunning natural landscapes—from ocean cliffs to tropical jungles."
                    courses={curatedCarousels.destinationResort}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {curatedCarousels.desertMountain.length > 0 && (
                  <CourseCarousel
                    title="Desert & Mountain Classics"
                    description="The unique artistry of creating championship golf in arid and mountainous environments, using dramatic elevation changes and breathtaking vistas."
                    courses={curatedCarousels.desertMountain}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {curatedCarousels.strategicArtistic.length > 0 && (
                  <CourseCarousel
                    title="Strategic & Artistic Gems"
                    description="Brilliant, often under-the-radar courses designed by master architects, revered for their strategic depth, artistic flair, and pure, unadulterated fun."
                    courses={curatedCarousels.strategicArtistic}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {curatedCarousels.international.length > 0 && (
                  <CourseCarousel
                    title="International Courses"
                    description="Championship courses from around the world, showcasing the global diversity of golf architecture and the unique challenges of different continents."
                    courses={curatedCarousels.international}
                    onCourseClick={handleCourseClick}
                  />
                )}

                {curatedCarousels.studioOriginals.length > 0 && (
                  <CourseCarousel
                    title="Studio Originals"
                    description="Experience Lidar Detail - Premium courses with sub-centimeter accuracy"
                    courses={curatedCarousels.studioOriginals}
                    onCourseClick={handleCourseClick}
                  />
                )}
              </>
            )
          })()}
        </div>
      </div>

      {showMapView && (
        <MapView
          courses={(filters.continent || filters.mood || filters.type || filters.contentTier) ? filteredCourses : courses}
          onCourseClick={handleMapCourseClick}
          onClose={() => setShowMapView(false)}
        />
      )}

      {selectedCourse && (
        <CourseDetailModal
          course={selectedCourse}
          onClose={closeModal}
          getBlurb={getBlurb}
          userRating={getRating(selectedCourse.id)}
          onRatingChange={(rating) => handleRatingChange(selectedCourse.id, rating)}
          isPlayLater={isPlayLater(selectedCourse.id)}
          onPlayLaterToggle={() => handlePlayLaterToggle(selectedCourse.id)}
          onTeeOffClick={() => {
            handleCoursePlay(selectedCourse.id)
            closeModal()
          }}
        />
      )}
    </div>
  )
}

export default BrowseApp
