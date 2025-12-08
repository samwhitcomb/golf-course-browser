import React, { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import './CourseMap.css'

// Fix for default marker icons in Leaflet with webpack/vite
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

// Component to set map view
function SetMapView({ center, zoom }) {
  const map = useMap()
  
  useEffect(() => {
    map.setView(center, zoom)
  }, [map, center, zoom])
  
  return null
}

function CourseMap({ course }) {
  // Get course coordinates
  const latitude = course.latitude
  const longitude = course.longitude
  
  if (!latitude || !longitude) {
    return (
      <div className="course-map-error">
        <p>Course location data not available</p>
      </div>
    )
  }

  const center = [latitude, longitude]
  const zoom = 17 // High zoom for hole-by-hole view

  // Create custom golf course marker
  const golfIcon = L.divIcon({
    className: 'golf-course-marker',
    html: '<div class="golf-marker-pin">⛳</div>',
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -40]
  })

  return (
    <div className="course-map-container">
      <div className="course-map-info">
        <h3 className="map-course-name">{course.name}</h3>
        <div className="map-course-details">
          {course.yardage && <span>{course.yardage.toLocaleString()} yds</span>}
          {course.par && <span>Par {course.par}</span>}
          <span>18 Holes</span>
          {course.type && <span className="course-type-badge">{course.type}</span>}
        </div>
        <p className="map-course-location">{course.location}</p>
      </div>
      
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '600px', width: '100%' }}
        zoomControl={true}
      >
        {/* Esri World Imagery - Satellite view */}
        <TileLayer
          attribution='&copy; <a href="https://www.esri.com/">Esri</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        />
        
        <SetMapView center={center} zoom={zoom} />
        
        <Marker
          position={center}
          icon={golfIcon}
        >
          <Popup>
            <div className="map-popup-content">
              <h4>{course.name}</h4>
              <p>{course.location}</p>
              {course.yardage && <p>{course.yardage.toLocaleString()} yards</p>}
            </div>
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  )
}

export default CourseMap


