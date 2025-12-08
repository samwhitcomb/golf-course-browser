import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import BrowseApp from './BrowseApp'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/presentation" element={<BrowseApp />} />
        <Route path="/" element={<Navigate to="/presentation" replace />} />
        {/* Scraper route removed for public build */}
      </Routes>
    </BrowserRouter>
  )
}

export default App
