import React, { useState, useEffect, useMemo } from 'react';
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
  const [countdown, setCountdown] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0 });
  
  // Wedding date: May 23, 2025 at 12:00 - wrapped in useMemo to avoid recreating on every render
  const weddingDate = useMemo(() => new Date('2025-05-23T12:00:00'), []);
  
  useEffect(() => {
    // Initial calculation
    calculateTimeRemaining();
    
    const intervalId = setInterval(calculateTimeRemaining, 1000);
    
    function calculateTimeRemaining() {
      const now = new Date();
      const difference = weddingDate - now;
      
      if (difference > 0) {
        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);
        
        setCountdown({ days, hours, minutes, seconds });
      }
    }
    
    return () => clearInterval(intervalId);
  }, [weddingDate]);
  
  // Hebrew text formatting
  const formattedCountdown = `בעוד ${countdown.days} ימים ${countdown.hours} שעות`;
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>יהל & אסף</h1>
        <p className="wedding-date">יום שישי, כ״ה באייר תשפ״ה</p>
        <p className="wedding-date">23.05.2025</p>
        <p className="countdown">מתחתנים {formattedCountdown}</p>
        
        <nav className="main-nav">
          <ul>
            <li className={location.pathname === '/' ? 'active' : ''}>
              <Link to="/">ראשי</Link>
            </li>
            <li className={location.pathname === '/schedule' ? 'active' : ''}>
              <Link to="/schedule">לוח זמנים</Link>
            </li>
            <li className={location.pathname === '/gallery' ? 'active' : ''}>
              <Link to="/gallery">גלריה</Link>
            </li>
            <li className={location.pathname === '/travel' ? 'active' : ''}>
              <Link to="/travel">מקום האירוע</Link>
            </li>
            <li className={location.pathname === '/registry' ? 'active' : ''}>
              <Link to="/registry">מתנות</Link>
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
        <p>יהל & אסף 2025 ©</p>
      </footer>
    </div>
  );
}

export default App; 