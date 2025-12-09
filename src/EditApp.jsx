import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import './App.css'

const API_BASE = '/api'

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
      const response = await fetch(`${API_BASE}/courses`)
      if (!response.ok) throw new Error('Failed to fetch courses')
      const data = await response.json()
      setCourses(data)
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
    try {
      setDownloading(prev => ({ ...prev, [`${courseId}_${slot}`]: true }))
      const response = await fetch(`${API_BASE}/download-image/${courseId}/${slot}`, {
        method: 'POST'
      })
      const data = await response.json()

      if (data.success) {
        await fetchCourses({ preserveScroll: true })
      } else {
        alert(`Failed to download image: ${data.error || 'Unknown error'}`)
      }
    } catch (err) {
      alert(`Error downloading image: ${err.message}`)
      console.error('Error downloading image:', err)
    } finally {
      setDownloading(prev => ({ ...prev, [`${courseId}_${slot}`]: false }))
    }
  }

  const regenerateImage = async (courseId, slot = 'hero') => {
    try {
      setDownloading(prev => ({ ...prev, [`${courseId}_${slot}`]: true }))
      const response = await fetch(`${API_BASE}/regenerate-image/${courseId}/${slot}`, {
        method: 'POST'
      })
      const data = await response.json()

      if (data.success) {
        await fetchCourses({ preserveScroll: true })
      } else {
        alert(`Failed to regenerate image: ${data.error || 'Unknown error'}`)
      }
    } catch (err) {
      alert(`Error regenerating image: ${err.message}`)
      console.error('Error regenerating image:', err)
    } finally {
      setDownloading(prev => ({ ...prev, [`${courseId}_${slot}`]: false }))
    }
  }

  const setHeroImage = async (courseId, slot) => {
    try {
      setDownloading(prev => ({ ...prev, [`${courseId}_setHero`]: true }))
      const response = await fetch(`${API_BASE}/set-hero-image/${courseId}/${slot}`, {
        method: 'POST'
      })
      const data = await response.json()

      if (data.success) {
        await fetchCourses({ preserveScroll: true })
      } else {
        alert(`Failed to set hero image: ${data.error || 'Unknown error'}`)
      }
    } catch (err) {
      alert(`Error setting hero image: ${err.message}`)
      console.error('Error setting hero image:', err)
    } finally {
      setDownloading(prev => ({ ...prev, [`${courseId}_setHero`]: false }))
    }
  }

  const openPicker = async (course, slot = 'hero') => {
    setPickerCourse(course)
    setPickerSlot(slot)
    setPickerOpen(true)
    setPickerImages([])
    setPickerError(null)
    setPickerLoading(true)
    try {
      const response = await fetch(`${API_BASE}/search-images/${course.id}?limit=20`)
      if (!response.ok) throw new Error('Failed to search images')
      const data = await response.json()
      setPickerImages(data.results || [])
    } catch (err) {
      setPickerError(err.message)
    } finally {
      setPickerLoading(false)
    }
  }

  const closePicker = () => {
    setPickerOpen(false)
    setPickerCourse(null)
    setPickerSlot('hero')
    setPickerImages([])
    setPickerError(null)
  }

  const chooseImage = async (courseId, url, slot) => {
    try {
      setDownloading(prev => ({ ...prev, [`${courseId}_${slot}`]: true }))
      const response = await fetch(`${API_BASE}/download-from-url/${courseId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, slot })
      })
      const text = await response.text()
      let data = {}
      try {
        data = JSON.parse(text)
      } catch (_) {
        throw new Error(`Non-JSON response: ${text.slice(0, 120)}`)
      }

      if (data.success) {
        await fetchCourses({ preserveScroll: true })
        closePicker()
      } else {
        const detail = data.detail ? ` (${data.detail})` : ''
        alert(`Failed to save image: ${data.error || 'Unknown error'}${detail}`)
      }
    } catch (err) {
      alert(`Error saving image: ${err.message}`)
      console.error('Error saving chosen image:', err)
    } finally {
      setDownloading(prev => ({ ...prev, [`${courseId}_${slot}`]: false }))
    }
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
    
    try {
      setSavingDescription(true)
      const response = await fetch(`${API_BASE}/update-course/${infoCourse.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ blurb: editedBlurb })
      })
      
      const data = await response.json()
      if (data.success) {
        await fetchCourses({ preserveScroll: true })
        // Update the infoCourse with new blurb
        setInfoCourse({ ...infoCourse, blurb: editedBlurb })
        setEditingDescription(false)
      } else {
        alert(`Failed to save description: ${data.error || 'Unknown error'}`)
      }
    } catch (err) {
      alert(`Error saving description: ${err.message}`)
      console.error('Error saving description:', err)
    } finally {
      setSavingDescription(false)
    }
  }

  const downloadAllImages = async () => {
    if (!confirm('This will download images for all courses without images. This may take a while. Continue?')) {
      return
    }

    try {
      setDownloading(prev => ({ ...prev, 'all': true }))
      const response = await fetch(`${API_BASE}/download-all`, {
        method: 'POST'
      })
      const data = await response.json()

      alert(`Downloaded ${data.filter(r => r.success).length} of ${data.length} images`)
      await fetchCourses()
    } catch (err) {
      alert(`Error downloading images: ${err.message}`)
      console.error('Error downloading all images:', err)
    } finally {
      setDownloading(prev => ({ ...prev, 'all': false }))
    }
  }

  const downloadSecondaryImages = async () => {
    const coursesWithHero = courses.filter(c => {
      const images = c.images || { hero: null, additional: [] }
      return images.hero || c.hasImage
    })
    
    const coursesNeedingSecondary = coursesWithHero.filter(c => {
      const images = c.images || { hero: null, additional: [] }
      return !images.additional || images.additional.length < 2
    })

    if (coursesNeedingSecondary.length === 0) {
      alert('All courses with hero images already have secondary images!')
      return
    }

    if (!confirm(`This will download secondary images (slots 1 & 2) for ${coursesNeedingSecondary.length} courses that have hero images but are missing secondary images. This may take a while. Continue?`)) {
      return
    }

    try {
      setDownloading(prev => ({ ...prev, 'secondary': true }))
      const response = await fetch(`${API_BASE}/download-secondary-images`, {
        method: 'POST'
      })
      const data = await response.json()

      const slot1Count = data.filter(r => r.slot1).length
      const slot2Count = data.filter(r => r.slot2).length
      alert(`Downloaded ${slot1Count} slot 1 images and ${slot2Count} slot 2 images`)
      await fetchCourses()
    } catch (err) {
      alert(`Error downloading secondary images: ${err.message}`)
      console.error('Error downloading secondary images:', err)
    } finally {
      setDownloading(prev => ({ ...prev, 'secondary': false }))
    }
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

