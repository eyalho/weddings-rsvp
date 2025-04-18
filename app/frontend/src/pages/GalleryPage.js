import React from 'react';

function GalleryPage() {
  // בחיים אמיתיים, היינו טוענים את התמונות מה-API או מקובץ קונפיגורציה
  const photos = [
    {
      id: 1,
      src: 'https://via.placeholder.com/400x300?text=יהל+ואסף+1',
      alt: 'יהל ואסף 1',
      caption: 'הצעת הנישואין בחוף הים'
    },
    {
      id: 2,
      src: 'https://via.placeholder.com/400x300?text=יהל+ואסף+2',
      alt: 'יהל ואסף 2',
      caption: 'טיול בצפון'
    },
    {
      id: 3,
      src: 'https://via.placeholder.com/400x300?text=יהל+ואסף+3',
      alt: 'יהל ואסף 3',
      caption: 'היום שבו נפגשנו'
    },
    {
      id: 4,
      src: 'https://via.placeholder.com/400x300?text=יהל+ואסף+4',
      alt: 'יהל ואסף 4',
      caption: 'זכרונות מחופשה'
    },
    {
      id: 5,
      src: 'https://via.placeholder.com/400x300?text=יהל+ואסף+5',
      alt: 'יהל ואסף 5',
      caption: 'ארוחת ערב משפחתית'
    },
    {
      id: 6,
      src: 'https://via.placeholder.com/400x300?text=יהל+ואסף+6',
      alt: 'יהל ואסף 6',
      caption: 'יום בחוף'
    },
  ];

  return (
    <div className="gallery-page">
      <h1>הסיפור שלנו</h1>
      <p className="gallery-intro">
        הנה כמה מהרגעים האהובים עלינו מהקשר שלנו. אנחנו מחכים ליצור זכרונות חדשים איתכם ביום המיוחד שלנו!
      </p>
      
      <div className="photo-grid">
        {photos.map(photo => (
          <div key={photo.id} className="photo-item">
            <img src={photo.src} alt={photo.alt} />
            <p className="photo-caption">{photo.caption}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default GalleryPage; 