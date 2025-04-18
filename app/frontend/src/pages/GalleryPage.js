import React from 'react';

function GalleryPage() {
  // In a real application, you would load these from an API or config
  const photos = [
    {
      id: 1,
      src: 'https://via.placeholder.com/400x300?text=Engagement+Photo+1',
      alt: 'Engagement Photo 1',
      caption: 'Our engagement in Central Park'
    },
    {
      id: 2,
      src: 'https://via.placeholder.com/400x300?text=Engagement+Photo+2',
      alt: 'Engagement Photo 2',
      caption: 'Weekend getaway in Wine Country'
    },
    {
      id: 3,
      src: 'https://via.placeholder.com/400x300?text=Engagement+Photo+3',
      alt: 'Engagement Photo 3',
      caption: 'The day we met'
    },
    {
      id: 4,
      src: 'https://via.placeholder.com/400x300?text=Engagement+Photo+4',
      alt: 'Engagement Photo 4',
      caption: 'Holiday memories'
    },
    {
      id: 5,
      src: 'https://via.placeholder.com/400x300?text=Engagement+Photo+5',
      alt: 'Engagement Photo 5',
      caption: 'Family dinner'
    },
    {
      id: 6,
      src: 'https://via.placeholder.com/400x300?text=Engagement+Photo+6',
      alt: 'Engagement Photo 6',
      caption: 'Beach day'
    },
  ];

  return (
    <div className="gallery-page">
      <h1>Our Journey Together</h1>
      <p className="gallery-intro">
        Here are some of our favorite moments from our relationship. We can't wait to create more memories with you on our special day!
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