import React from 'react'
import { HashRouter, Routes, Route } from 'react-router-dom'
import BrowseApp from './BrowseApp'
import './App.css'

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<BrowseApp />} />
        <Route path="/presentation" element={<BrowseApp />} />
      </Routes>
    </HashRouter>
  )
}

export default App
