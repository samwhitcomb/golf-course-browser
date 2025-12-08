import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { processCourseImages } from './utils/imagePaths'
import './App.css'

function EditApp() {
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [downloading, setDownloading] = useState({})
  const [error, setError] = useState(null)
  const [pickerOpen, setPickerOpen] = useState(false)
  const [pickerCourse, setPickerCourse] = useState(null)
  const [pickerSlot, setPickerSlot] = useState('hero')
  const [pickerImages, setPickerImages] = useState([])
  const [pickerLoading, setPickerLoading] = useState(false)
  const [pickerError, setPickerError] = useState(null)
  const [infoOpen, setInfoOpen] = useState(false)
  const [infoCourse, setInfoCourse] = useState(null)
  const [editingDescription, setEditingDescription] = useState(false)
  const [editedBlurb, setEditedBlurb] = useState(['', ''])
  const [savingDescription, setSavingDescription] = useState(false)

  const getBlurb = (course) => {
    // Use custom descriptions if available, otherwise generate
    if (course.blurb && Array.isArray(course.blurb) && course.blurb.length >= 2) {
      return course.blurb
    }
    
    // Fallback to generated blurbs
    const templates = [
      (c) => [
        `${c.name} is a standout track that blends its setting in ${c.location} with a routing that rewards thoughtful shot-making. ${c.description}`,
        `Known for its character and consistency, it has earned a ${c.rating?.toFixed ? c.rating.toFixed(1) : c.rating}/5 reputation. Regulars point to its history and memorable holes as the reason it remains a must-play in the region.`
      ],
      (c) => [
        `Set in ${c.location}, ${c.name} weaves scenery into strategy, asking golfers to choose lines carefully while enjoying the landscape. ${c.description}`,
        `Its acclaim (${c.rating?.toFixed ? c.rating.toFixed(1) : c.rating}/5) comes from a mix of architecture, conditioning, and a few signature moments that keep players talking long after the round.`
      ],
      (c) => [
        `${c.name} sits in ${c.location}, offering a classic feel with enough bite to keep low-handicaps honest. ${c.description}`,
        `Stories around the clubhouse often cite its storied holes and steady challenge; with a ${c.rating?.toFixed ? c.rating.toFixed(1) : c.rating}/5 rating, it stays firmly on the shortlist for return trips.`
      ],
    ]
    const idx = Math.abs((course.id || '').split('').reduce((a, ch) => a + ch.charCodeAt(0), 0)) % templates.length
    return templates[idx](course)
  }

  useEffect(() => {
    fetchCourses()
  }, [])

  const fetchCourses = async (opts = {}) => {
    const preserveScroll = !!opts.preserveScroll
    const currentScroll = preserveScroll ? window.scrollY : null
    try {
      setLoading(true)
      const response = await fetch('/courses.json')
      if (!response.ok) throw new Error('Failed to fetch courses')
      const data = await response.json()
      // Process course data to add image paths
      const processedData = processCourseImages(data)
      setCourses(processedData)
      setError(null)
    } catch (err) {
      setError(err.message)
      console.error('Error fetching courses:', err)
    } finally {
      setLoading(false)
      if (preserveScroll && currentScroll !== null) {
        requestAnimationFrame(() => {
          window.scrollTo({ top: currentScroll })
        })
      }
    }
  }

  const downloadImage = async (courseId, slot = 'hero') => {
    alert('Image scraping is disabled in static mode. This feature requires a backend server.')
  }

  const regenerateImage = async (courseId, slot = 'hero') => {
    alert('Image scraping is disabled in static mode. This feature requires a backend server.')
  }

  const setHeroImage = async (courseId, slot) => {
    alert('Image management is disabled in static mode. This feature requires a backend server.')
  }

  const openPicker = async (course, slot = 'hero') => {
    alert('Image scraping is disabled in static mode. This feature requires a backend server.')
  }

  const closePicker = () => {
    setPickerOpen(false)
    setPickerCourse(null)
    setPickerSlot('hero')
    setPickerImages([])
    setPickerError(null)
  }

  const chooseImage = async (courseId, url, slot) => {
    alert('Image scraping is disabled in static mode. This feature requires a backend server.')
  }

  const openInfo = (course) => {
    setInfoCourse(course)
    setInfoOpen(true)
    setEditingDescription(false)
    // Initialize edited blurb with current blurb or empty
    const currentBlurb = getBlurb(course)
    setEditedBlurb([currentBlurb[0] || '', currentBlurb[1] || ''])
  }

  const closeInfo = () => {
    setInfoOpen(false)
    setInfoCourse(null)
    setEditingDescription(false)
    setEditedBlurb(['', ''])
  }

  const saveDescription = async () => {
    if (!infoCourse) return
    
    // Save to localStorage in static mode
    try {
      setSavingDescription(true)
      const savedDescriptions = JSON.parse(localStorage.getItem('course_descriptions') || '{}')
      savedDescriptions[infoCourse.id] = { blurb: editedBlurb }
      localStorage.setItem('course_descriptions', JSON.stringify(savedDescriptions))
      
      // Update the infoCourse with new blurb
      setInfoCourse({ ...infoCourse, blurb: editedBlurb })
      setEditingDescription(false)
      
      // Update courses list
      setCourses(prev => prev.map(c => 
        c.id === infoCourse.id ? { ...c, blurb: editedBlurb } : c
      ))
    } catch (err) {
      alert(`Error saving description: ${err.message}`)
      console.error('Error saving description:', err)
    } finally {
      setSavingDescription(false)
    }
  }

  const downloadAllImages = async () => {
    alert('Image scraping is disabled in static mode. This feature requires a backend server.')
  }

  const downloadSecondaryImages = async () => {
    alert('Image scraping is disabled in static mode. This feature requires a backend server.')
  }

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading courses...</div>
      </div>
    )
  }

  const coursesWithImages = courses.filter(c => c.hasImage).length
  const coursesWithoutImages = courses.length - coursesWithImages

  return (
    <div className="app">
      <header className="header">
        <h1>Golf Course Image Scraper</h1>
        <div className="stats">
          <span>Total: {courses.length}</span>
          <span>With Images: {coursesWithImages}</span>
          <span>Without Images: {coursesWithoutImages}</span>
        </div>
        <div className="header-actions">
          {coursesWithoutImages > 0 && (
            <button
              className="btn btn-primary"
              onClick={downloadAllImages}
              disabled={downloading.all || downloading.secondary}
            >
              {downloading.all ? 'Downloading...' : `Download All (${coursesWithoutImages})`}
            </button>
          )}
          {coursesWithImages > 0 && (
            <button
              className="btn btn-secondary"
              onClick={downloadSecondaryImages}
              disabled={downloading.all || downloading.secondary}
            >
              {downloading.secondary ? 'Downloading...' : 'Download Secondary Images'}
            </button>
          )}
          <Link to="/presentation" className="btn btn-secondary presentation-link">
            View Presentation
          </Link>
        </div>
      </header>

      <div className="page-description">
        <h2>About This Tool</h2>
        <p>
          This tool helps you manage golf course images and descriptions. The basic function is for scraping images 
          from Google Images and choosing better ones for each course. You can also edit course descriptions directly 
          from the course detail modal.
        </p>
        <div className="static-mode-notice" style={{ 
          marginTop: '16px', 
          padding: '12px', 
          backgroundColor: 'rgba(251, 191, 36, 0.2)', 
          border: '1px solid rgba(251, 191, 36, 0.5)',
          borderRadius: '4px',
          color: '#fbbf24'
        }}>
          <strong>Static Mode:</strong> Image scraping and download features are disabled. Description edits are saved to browser storage only.
        </div>
      </div>

      {error && (
        <div className="error-banner">
          Error: {error}
        </div>
      )}

      <div className="courses-grid">
        {courses.map(course => (
          <div 
            key={course.id} 
            className="course-card"
            onClick={() => openInfo(course)}
          >
            <button
              className="info-button"
              title="Course details"
              onClick={(e) => {
                e.stopPropagation()
                openInfo(course)
              }}
            >
              i
            </button>
            <div className="course-images-grid">
              {['hero', '1', '2'].map(slot => {
                const images = course.images || { hero: null, additional: [] }
                const imageUrl = slot === 'hero' 
                  ? images.hero 
                  : images.additional && images.additional[parseInt(slot) - 1]
                const hasImage = !!imageUrl
                const isHero = slot === 'hero'
                const slotLabel = isHero ? 'Hero' : `Image ${slot}`
                
                return (
                  <div 
                    key={slot} 
                    className={`course-image-slot ${isHero ? 'hero-slot' : ''}`}
                    onClick={(e) => e.stopPropagation()}
                  >
                    {isHero && <div className="hero-badge">HERO</div>}
                    <div className="course-image-container-small">
                      {hasImage ? (
                        <img 
                          src={imageUrl} 
                          alt={`${course.name} - ${slotLabel}`}
                          className="course-image-small"
                          onError={(e) => {
                            e.target.style.display = 'none'
                            e.target.nextSibling.style.display = 'flex'
                          }}
                        />
                      ) : null}
                      <div 
                        className="course-image-placeholder-small"
                        style={{ display: hasImage ? 'none' : 'flex' }}
                      >
                        <span>No Image</span>
                      </div>
                    </div>
                    <div className="image-slot-actions">
                      {hasImage && !isHero && (
                        <button
                          className="btn btn-small btn-set-hero"
                          onClick={() => setHeroImage(course.id, slot)}
                          disabled={downloading[`${course.id}_setHero`]}
                          title="Set as hero image"
                        >
                          Set Hero
                        </button>
                      )}
                      {hasImage ? (
                        <>
                          <button
                            className="btn btn-small btn-secondary"
                            onClick={() => regenerateImage(course.id, slot)}
                            disabled={downloading[`${course.id}_${slot}`]}
                          >
                            Regenerate
                          </button>
                          <button
                            className="btn btn-small btn-primary"
                            onClick={() => openPicker(course, slot)}
                            disabled={downloading[`${course.id}_${slot}`]}
                          >
                            Choose
                          </button>
                        </>
                      ) : (
                        <button
                          className="btn btn-small btn-primary"
                          onClick={() => downloadImage(course.id, slot)}
                          disabled={downloading[`${course.id}_${slot}`]}
                        >
                          Download
                        </button>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
            <div className="course-info">
              <h3 className="course-name">{course.name}</h3>
              <p className="course-location">{course.location}</p>
              <p className="course-description">{course.description}</p>
              <div className="course-rating">Rating: {course.rating} / 5.0</div>
            </div>
          </div>
        ))}
      </div>

      {pickerOpen && (
        <div className="modal-backdrop" onClick={closePicker}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Select an image{pickerCourse ? ` for ${pickerCourse.name}` : ''} ({pickerSlot === 'hero' ? 'Hero' : `Image ${pickerSlot}`})</h3>
              <button className="modal-close" onClick={closePicker}>×</button>
            </div>
            <div className="modal-body">
              {pickerLoading && <div className="modal-status">Searching images...</div>}
              {pickerError && <div className="error-banner">Error: {pickerError}</div>}
              {!pickerLoading && !pickerError && pickerImages.length === 0 && (
                <div className="modal-status">No images found.</div>
              )}
              <div className="picker-grid">
                {pickerImages.map((img) => (
                  <button
                    key={img.url}
                    className="picker-card"
                    onClick={() => chooseImage(pickerCourse.id, img.url, pickerSlot)}
                    disabled={downloading[`${pickerCourse?.id}_${pickerSlot}`]}
                    title="Use this image"
                  >
                    <img src={img.thumb || img.url} alt="Candidate" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {infoOpen && (
        <div className="modal-backdrop" onClick={closeInfo}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{infoCourse?.name || 'Course details'}</h3>
              <button className="modal-close" onClick={closeInfo}>×</button>
            </div>
            <div className="modal-body">
              {infoCourse && (
                <div className="info-body">
                  <div className="info-row"><strong>Location:</strong> {infoCourse.location}</div>
                  <div className="info-row"><strong>Rating:</strong> {infoCourse.rating} / 5.0</div>
                  {(infoCourse.batch || infoCourse.type) && (
                    <div className="info-row">
                      <strong>Tags:</strong>
                      <div className="tags-container">
                        {infoCourse.type && (
                          <span className="course-tag course-type-tag">{infoCourse.type}</span>
                        )}
                        {infoCourse.batch && (
                          <span className="course-tag batch-tag">{infoCourse.batch}</span>
                        )}
                      </div>
                    </div>
                  )}
                  <div className="info-section">
                    <div className="info-section-header">
                      <strong>Description</strong>
                      {!editingDescription ? (
                        <button
                          className="btn btn-secondary btn-small"
                          onClick={() => {
                            const currentBlurb = getBlurb(infoCourse)
                            setEditedBlurb([currentBlurb[0] || '', currentBlurb[1] || ''])
                            setEditingDescription(true)
                          }}
                        >
                          Edit
                        </button>
                      ) : (
                        <div className="edit-actions">
                          <button
                            className="btn btn-primary btn-small"
                            onClick={saveDescription}
                            disabled={savingDescription}
                          >
                            {savingDescription ? 'Saving...' : 'Save'}
                          </button>
                          <button
                            className="btn btn-secondary btn-small"
                            onClick={() => {
                              setEditingDescription(false)
                              const currentBlurb = getBlurb(infoCourse)
                              setEditedBlurb([currentBlurb[0] || '', currentBlurb[1] || ''])
                            }}
                            disabled={savingDescription}
                          >
                            Cancel
                          </button>
                        </div>
                      )}
                    </div>
                    {editingDescription ? (
                      <div className="description-editor">
                        <label>Paragraph 1:</label>
                        <textarea
                          className="description-textarea"
                          value={editedBlurb[0]}
                          onChange={(e) => setEditedBlurb([e.target.value, editedBlurb[1]])}
                          rows={4}
                          placeholder="Enter first paragraph..."
                        />
                        <label>Paragraph 2:</label>
                        <textarea
                          className="description-textarea"
                          value={editedBlurb[1]}
                          onChange={(e) => setEditedBlurb([editedBlurb[0], e.target.value])}
                          rows={4}
                          placeholder="Enter second paragraph..."
                        />
                      </div>
                    ) : (
                      <div className="info-text-container">
                        {getBlurb(infoCourse).map((p, idx) => (
                          <div key={idx} className="info-text">{p}</div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default EditApp

