import React from 'react';

function SchedulePage() {
  const events = [
    {
      id: 1,
      time: '2:00 PM - 3:00 PM',
      title: 'Ceremony',
      location: 'Central Park, Bethesda Fountain',
      description: 'Join us as we exchange vows in the beautiful surroundings of Central Park.'
    },
    {
      id: 2,
      time: '3:15 PM - 4:30 PM',
      title: 'Cocktail Hour',
      location: 'The Plaza Hotel, Terrace Garden',
      description: 'Enjoy drinks and hors d\'oeuvres while we take photos. Live music will be provided.'
    },
    {
      id: 3,
      time: '5:00 PM - 6:00 PM',
      title: 'Guest Arrival & Seating',
      location: 'The Plaza Hotel, Grand Ballroom',
      description: 'Take your seats for dinner and festivities.'
    },
    {
      id: 4,
      time: '6:00 PM - 7:30 PM',
      title: 'Dinner',
      location: 'The Plaza Hotel, Grand Ballroom',
      description: 'A formal dinner will be served, including your choice of entrée as specified in your RSVP.'
    },
    {
      id: 5,
      time: '7:30 PM - 8:00 PM',
      title: 'Toasts & Cake Cutting',
      location: 'The Plaza Hotel, Grand Ballroom',
      description: 'Speeches from the wedding party, followed by the cutting of the cake.'
    },
    {
      id: 6,
      time: '8:00 PM - 11:00 PM',
      title: 'Dancing & Celebration',
      location: 'The Plaza Hotel, Grand Ballroom',
      description: 'Dance the night away with us!'
    }
  ];
  
  return (
    <div className="schedule-page">
      <h1>Wedding Day Schedule</h1>
      <p className="schedule-date">Saturday, June 15, 2024</p>
      
      <div className="timeline">
        {events.map(event => (
          <div key={event.id} className="timeline-item">
            <div className="timeline-time">{event.time}</div>
            <div className="timeline-content">
              <h3>{event.title}</h3>
              <div className="timeline-location">{event.location}</div>
              <p>{event.description}</p>
            </div>
          </div>
        ))}
      </div>
      
      <div className="schedule-notes">
        <h3>Additional Information</h3>
        <ul>
          <li>Attire: Formal/Black Tie</li>
          <li>Parking: Valet parking available at The Plaza Hotel</li>
          <li>Transportation: Shuttles will be provided from the ceremony to the reception</li>
        </ul>
      </div>
    </div>
  );
}

export default SchedulePage; 