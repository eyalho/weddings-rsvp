import React from 'react';

function TravelPage() {
  const hotels = [
    {
      id: 1,
      name: 'The Plaza Hotel',
      description: 'Our wedding venue with a special room block for guests.',
      address: '768 5th Ave, New York, NY 10019',
      phone: '(212) 759-3000',
      website: 'https://www.theplazany.com',
      discount: 'Use code WEDDINGJJ for 15% off the standard rate.',
      cutoffDate: 'May 15, 2024'
    },
    {
      id: 2,
      name: 'Park Central Hotel',
      description: 'A mid-range option, 10-minute walk from the venue.',
      address: '870 7th Ave, New York, NY 10019',
      phone: '(212) 247-8000',
      website: 'https://www.parkcentralny.com',
      discount: 'Use code WEDDING2024 for 10% off the standard rate.',
      cutoffDate: 'May 20, 2024'
    },
    {
      id: 3,
      name: 'Pod 51 Hotel',
      description: 'Budget-friendly option, 15-minute subway ride to the venue.',
      address: '230 E 51st St, New York, NY 10022',
      phone: '(212) 355-0300',
      website: 'https://www.thepodhotel.com',
      discount: 'No special rate available.',
      cutoffDate: 'N/A'
    },
  ];

  return (
    <div className="travel-page">
      <h1>מקום האירוע</h1>
      
      <section className="travel-section">
        <h2>הלורנס</h2>
        <p>החתונה תתקיים באולם האירועים "הלורנס" הממוקם ברחוב הצורפים 18, תל אביב-יפו.</p>
        
        <div className="location-map">
          <iframe 
            title="מפת האולם"
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3381.749717760472!2d34.7550382!3d32.052339!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x151d4ca18b9eec8d%3A0xb67583a4cb94c7cd!2z15TXqdeV16jXpNeZ150gMTgsINeq15wg15DXkdeZ15ET15nXpdeV!5e0!3m2!1siw!2sil!4v1650000000000!5m2!1siw!2sil" 
            width="100%" 
            height="450" 
            style={{ border: 0, borderRadius: "8px", marginTop: "1rem" }}
            allowFullScreen="" 
            loading="lazy" 
            referrerPolicy="no-referrer-when-downgrade">
          </iframe>
        </div>
      </section>
      
      <section className="travel-section">
        <h2>הגעה למקום</h2>
        <div className="travel-info">
          <div className="travel-item">
            <h3>ברכב פרטי</h3>
            <p>ניתן להגיע עם רכב פרטי. באזור קיימות מספר חניות:</p>
            <ul>
              <li><strong>חניון הצורפים</strong> - ברחוב הצורפים 18, צמוד לאולם</li>
              <li><strong>חניון רוטשילד</strong> - במרחק הליכה של 5 דקות מהאולם</li>
              <li><strong>חניון נחלת בנימין</strong> - במרחק הליכה של 7 דקות מהאולם</li>
            </ul>
          </div>
          
          <div className="travel-item">
            <h3>בתחבורה ציבורית</h3>
            <p>קווי אוטובוס רבים עוברים באזור:</p>
            <ul>
              <li><strong>קווים 10, 14, 18</strong> - תחנת פילון/אלנבי</li>
              <li><strong>קווים 63, 83, 239</strong> - תחנת הרצל/נחלת בנימין</li>
              <li><strong>קווים 4, 104, 204</strong> - תחנת אלנבי/שד׳ רוטשילד</li>
            </ul>
            <p>תחנת הרכבת הקלה הקרובה ביותר היא "אלנבי" במרחק של כ-7 דקות הליכה.</p>
          </div>
        </div>
      </section>
      
      <section className="travel-section">
        <h2>מידע על האולם</h2>
        <p>הלורנס הוא אולם אירועים בלב תל אביב המשלב עיצוב מודרני עם אווירה אורבנית ייחודית.</p>
        
        <div className="venue-details">
          <p><strong>כתובת:</strong> הצורפים 18, תל אביב-יפו</p>
          <p><strong>טלפון:</strong> 03-1234567</p>
          <p><strong>אתר אינטרנט:</strong> <a href="http://www.lawrence.co.il" target="_blank" rel="noopener noreferrer" className="ltr">www.lawrence.co.il</a></p>
          <p><strong>שעות האירוע:</strong> קבלת פנים תחל בשעה 12:00, והאירוע צפוי להסתיים בסביבות השעה 18:00</p>
        </div>
      </section>
      
      <section className="travel-section">
        <h2>לינה</h2>
        <p>למגיעים מרחוק, הנה מספר אפשרויות לינה בקרבת מקום:</p>
        
        <div className="hotels-list">
          <div className="hotel-card">
            <h3>מלון רוטשילד 22</h3>
            <p>מלון בוטיק יוקרתי במרחק של 10 דקות הליכה מהאולם.</p>
            <div className="hotel-details">
              <p><strong>כתובת:</strong> שד׳ רוטשילד 22, תל אביב</p>
              <p><strong>טלפון:</strong> 03-9876543</p>
              <p><strong>מרחק מהאולם:</strong> 800 מטר</p>
            </div>
          </div>
          
          <div className="hotel-card">
            <h3>מלון דיזנגוף סוויטס</h3>
            <p>מלון דירות במחיר סביר במרחק של 15 דקות הליכה מהאולם.</p>
            <div className="hotel-details">
              <p><strong>כתובת:</strong> דיזנגוף 165, תל אביב</p>
              <p><strong>טלפון:</strong> 03-7654321</p>
              <p><strong>מרחק מהאולם:</strong> 1.2 ק״מ</p>
            </div>
          </div>
          
          <div className="hotel-card">
            <h3>מלון הים</h3>
            <p>מלון על חוף הים במרחק נסיעה קצרה מהאולם.</p>
            <div className="hotel-details">
              <p><strong>כתובת:</strong> טיילת הרברט סמואל 122, תל אביב</p>
              <p><strong>טלפון:</strong> 03-8765432</p>
              <p><strong>מרחק מהאולם:</strong> 1.5 ק״מ</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default TravelPage; 