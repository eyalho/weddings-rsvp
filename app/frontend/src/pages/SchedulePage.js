import React from 'react';

function SchedulePage() {
  const events = [
    {
      id: 1,
      time: '12:00',
      title: 'קבלת פנים',
      location: 'הלורנס, תל אביב',
      description: 'קבלת פנים במתחם החיצוני של האולם, כיבוד קל ושתייה.'
    },
    {
      id: 2,
      time: '13:00',
      title: 'קבלת פנים ממשיכה',
      location: 'הלורנס, תל אביב',
      description: 'המשך קבלת פנים, צילומים ואיחולים לזוג המאושר.'
    },
    {
      id: 3,
      time: '13:30',
      title: 'חופה וקידושין',
      location: 'הלורנס, תל אביב',
      description: 'טקס החופה וקידושין. נשמח שכולם יהיו נוכחים בזמן.'
    },
    {
      id: 4,
      time: '14:30',
      title: 'ארוחה חגיגית',
      location: 'אולם הלורנס',
      description: 'ארוחה חגיגית, תוכלו ליהנות ממגוון מנות ומטעמים.'
    },
    {
      id: 5,
      time: '15:30',
      title: 'ריקודים',
      location: 'רחבת הריקודים',
      description: 'מוזמנים לרקוד ולחגוג איתנו!'
    },
    {
      id: 6,
      time: '18:00',
      title: 'סיום משוער',
      location: 'הלורנס',
      description: 'סיום משוער של האירוע.'
    }
  ];
  
  return (
    <div className="schedule-page">
      <h1>לוח זמנים</h1>
      <p className="schedule-date">יום שישי, כ״ה באייר תשפ״ה, 23.05.2025</p>
      
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
        <h3>מידע נוסף</h3>
        <ul>
          <li><strong>לבוש:</strong> לבוש אלגנטי</li>
          <li><strong>חניה:</strong> חניה זמינה במתחם וברחובות הסמוכים</li>
          <li><strong>הסעות:</strong> פרטים על הסעות יפורסמו בהמשך</li>
        </ul>
      </div>
    </div>
  );
}

export default SchedulePage; 