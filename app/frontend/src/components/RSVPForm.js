import React, { useState } from 'react';

function RSVPForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [attending, setAttending] = useState(true);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('RSVP submitted:', { name, email, attending });
    // Here you would typically make an API call to your backend
  };

  return (
    <div className="rsvp-form">
      <h2>RSVP to our Wedding</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Full Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={attending}
              onChange={(e) => setAttending(e.target.checked)}
            />
            I will attend the wedding
          </label>
        </div>
        
        <button type="submit">Submit RSVP</button>
      </form>
    </div>
  );
}

export default RSVPForm; 