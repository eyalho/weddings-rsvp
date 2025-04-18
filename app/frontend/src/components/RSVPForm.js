import React, { useState } from 'react';

function RSVPForm() {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [attending, setAttending] = useState(true);
  const [guests, setGuests] = useState(1);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('RSVP submitted:', { name, phone, attending, guests });
    // Here you would typically make an API call to your backend
  };

  return (
    <div className="rsvp-form">
      <h2>אישור הגעה</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">שם מלא</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            placeholder="שם מלא"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="phone">טלפון נייד</label>
          <input
            type="tel"
            id="phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
            placeholder="050-0000000"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="guests">מספר אורחים</label>
          <select
            id="guests"
            value={guests}
            onChange={(e) => setGuests(Number(e.target.value))}
            required
          >
            {[1, 2, 3, 4].map(num => (
              <option key={num} value={num}>
                {num}
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={attending}
              onChange={(e) => setAttending(e.target.checked)}
            />
            אשמח להגיע לחגוג איתכם
          </label>
        </div>
        
        <button type="submit">שליחה</button>
      </form>
    </div>
  );
}

export default RSVPForm; 