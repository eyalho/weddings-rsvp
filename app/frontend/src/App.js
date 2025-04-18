import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import './styles/App.css';

// Import pages
import HomePage from './pages/HomePage';
import GalleryPage from './pages/GalleryPage';
import SchedulePage from './pages/SchedulePage';
import TravelPage from './pages/TravelPage';
import RegistryPage from './pages/RegistryPage';

function App() {
  const location = useLocation();
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>John & Jane's Wedding</h1>
        <p className="wedding-date">June 15, 2024</p>
        
        <nav className="main-nav">
          <ul>
            <li className={location.pathname === '/' ? 'active' : ''}>
              <Link to="/">Home</Link>
            </li>
            <li className={location.pathname === '/schedule' ? 'active' : ''}>
              <Link to="/schedule">Schedule</Link>
            </li>
            <li className={location.pathname === '/gallery' ? 'active' : ''}>
              <Link to="/gallery">Gallery</Link>
            </li>
            <li className={location.pathname === '/travel' ? 'active' : ''}>
              <Link to="/travel">Travel</Link>
            </li>
            <li className={location.pathname === '/registry' ? 'active' : ''}>
              <Link to="/registry">Registry</Link>
            </li>
          </ul>
        </nav>
      </header>
      
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/schedule" element={<SchedulePage />} />
          <Route path="/gallery" element={<GalleryPage />} />
          <Route path="/travel" element={<TravelPage />} />
          <Route path="/registry" element={<RegistryPage />} />
        </Routes>
      </main>
      
      <footer className="App-footer">
        <p>&copy; 2024 John & Jane</p>
      </footer>
    </div>
  );
}

export default App; 