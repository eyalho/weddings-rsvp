import React from 'react';
import RSVPForm from '../components/RSVPForm';

function HomePage() {
  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>יהל & אסף</h1>
        <p className="wedding-date">כ״ה באייר תשפ״ה • 23.05.2025</p>
        <p className="wedding-location">הלורנס, הצורפים 18, תל אביב-יפו</p>
        <p className="wedding-invitation">
          אנו שמחים ונרגשים להזמין אתכם לחגוג עמנו את יום נישואינו
        </p>
      </div>
      
      <div className="rsvp-section">
        <RSVPForm />
      </div>
      
      <div className="info-section">
        <h2>פרטי האירוע</h2>
        <p>
          מתרגשים להזמין אתכם לחגוג איתנו. יצרנו אתר זה כדי לספק לכם את כל המידע שתצטרכו לקראת החתונה.
        </p>
        
        <div className="event-details">
          <div className="detail-item">
            <h3>קבלת פנים</h3>
            <p>12:00</p>
            <p>הלורנס, הצורפים 18, תל אביב-יפו</p>
          </div>
          
          <div className="detail-item">
            <h3>חופה</h3>
            <p>13:30</p>
            <p>הלורנס</p>
          </div>
          
          <div className="detail-item">
            <h3>מסיבה</h3>
            <p>14:30 - 18:00</p>
            <p>הלורנס</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage; 