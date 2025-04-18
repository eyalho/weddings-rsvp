import React from 'react';
import RSVPForm from '../components/RSVPForm';

function HomePage() {
  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>John & Jane</h1>
        <p className="wedding-date">June 15, 2024</p>
        <p className="wedding-location">Central Park, New York</p>
      </div>
      
      <div className="rsvp-section">
        <RSVPForm />
      </div>
      
      <div className="info-section">
        <h2>Wedding Details</h2>
        <p>
          Join us for our special day. We've created this website to provide
          you with all the information you need for our upcoming wedding.
        </p>
        
        <div className="event-details">
          <div className="detail-item">
            <h3>Ceremony</h3>
            <p>2:00 PM - 3:00 PM</p>
            <p>Central Park, Bethesda Fountain</p>
          </div>
          
          <div className="detail-item">
            <h3>Reception</h3>
            <p>6:00 PM - 11:00 PM</p>
            <p>The Plaza Hotel, Grand Ballroom</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage; 