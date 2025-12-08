import React, { useEffect, useRef } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Tooltip, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import './MapView.css'

// Fix for default marker icons in Leaflet with webpack/vite
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

// Component to fit map bounds to show all markers
function FitBounds({ courses }) {
  const map = useMap()
  
  useEffect(() => {
    if (courses.length > 0) {
      const bounds = L.latLngBounds(
        courses
          .filter(c => c.latitude && c.longitude)
          .map(c => [c.latitude, c.longitude])
      )
      if (bounds.isValid()) {
        map.fitBounds(bounds, { padding: [50, 50] })
      }
    }
  }, [courses, map])
  
  return null
}

function MapView({ courses, onCourseClick, onClose }) {
  const mapRef = useRef(null)

  // Filter courses with valid coordinates
  const coursesWithCoords = courses.filter(
    c => c.latitude && c.longitude && c.hasImage
  )

  // Calculate center point (average of all course coordinates)
  const getCenter = () => {
    if (coursesWithCoords.length === 0) {
      return [39.8283, -98.5795] // Default center (US)
    }
    const avgLat = coursesWithCoords.reduce((sum, c) => sum + c.latitude, 0) / coursesWithCoords.length
    const avgLng = coursesWithCoords.reduce((sum, c) => sum + c.longitude, 0) / coursesWithCoords.length
    return [avgLat, avgLng]
  }

  const center = getCenter()

  // Create custom icon for markers
  const createCustomIcon = (course) => {
    return L.divIcon({
      className: 'custom-marker',
      html: `<div class="marker-pin" style="background-color: ${course.rating >= 4.5 ? '#e50914' : course.rating >= 4.0 ? '#f59e0b' : '#22c55e'}">
        <span class="marker-rating">${course.rating.toFixed(1)}</span>
      </div>`,
      iconSize: [30, 40],
      iconAnchor: [15, 40],
      popupAnchor: [0, -40]
    })
  }

  return (
    <div className="map-view-overlay" onClick={onClose}>
      <div className="map-view-container" onClick={e => e.stopPropagation()}>
        <button className="map-view-close" onClick={onClose}>×</button>
        <div className="map-view-header">
          <h2>Course Locations</h2>
          <p>{coursesWithCoords.length} courses on map</p>
        </div>
        {coursesWithCoords.length > 0 ? (
          <MapContainer
            center={center}
            zoom={4}
            style={{ height: '100%', width: '100%' }}
            ref={mapRef}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <FitBounds courses={coursesWithCoords} />
            {coursesWithCoords.map(course => (
              <Marker
                key={course.id}
                position={[course.latitude, course.longitude]}
                icon={createCustomIcon(course)}
                eventHandlers={{
                  click: () => {
                    if (onCourseClick) {
                      onCourseClick(course)
                    }
                  }
                }}
              >
                <Tooltip permanent={false} direction="top" offset={[0, -40]}>
                  {course.name}
                </Tooltip>
                <Popup>
                  <div className="map-popup-content">
                    <h3>{course.name}</h3>
                    <p>{course.location}</p>
                    <p className="map-popup-rating">★ {course.rating.toFixed(1)}</p>
                    <button
                      className="map-popup-button"
                      onClick={() => {
                        if (onCourseClick) {
                          onCourseClick(course)
                        }
                      }}
                    >
                      View Details
                    </button>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        ) : (
          <div className="map-view-empty">
            <p>No courses with location data available</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default MapView

