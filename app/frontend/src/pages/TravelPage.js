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
      <h1>Travel & Accommodations</h1>
      
      <section className="travel-section">
        <h2>Getting to New York City</h2>
        <div className="travel-info">
          <div className="travel-item">
            <h3>By Air</h3>
            <p>The closest airports to the venue are:</p>
            <ul>
              <li><strong>LaGuardia Airport (LGA)</strong> - 9 miles from Central Park</li>
              <li><strong>John F. Kennedy International Airport (JFK)</strong> - 16 miles from Central Park</li>
              <li><strong>Newark Liberty International Airport (EWR)</strong> - 17 miles from Central Park</li>
            </ul>
          </div>
          
          <div className="travel-item">
            <h3>By Train</h3>
            <p>Amtrak services Penn Station, which is a 20-minute subway ride to the venue.</p>
          </div>
        </div>
      </section>
      
      <section className="travel-section">
        <h2>Accommodations</h2>
        <p>We've arranged special rates at the following hotels. Please book early as New York City hotels fill up quickly.</p>
        
        <div className="hotels-list">
          {hotels.map(hotel => (
            <div key={hotel.id} className="hotel-card">
              <h3>{hotel.name}</h3>
              <p>{hotel.description}</p>
              <div className="hotel-details">
                <p><strong>Address:</strong> {hotel.address}</p>
                <p><strong>Phone:</strong> {hotel.phone}</p>
                <p><strong>Website:</strong> <a href={hotel.website} target="_blank" rel="noopener noreferrer">{hotel.website}</a></p>
                <p><strong>Discount:</strong> {hotel.discount}</p>
                <p><strong>Booking Cutoff Date:</strong> {hotel.cutoffDate}</p>
              </div>
            </div>
          ))}
        </div>
      </section>
      
      <section className="travel-section">
        <h2>Local Transportation</h2>
        <p>We recommend using the following options for getting around in New York City:</p>
        <ul>
          <li><strong>Subway:</strong> The easiest way to get around the city. The nearest stations to the venue are 5th Ave/59th St and 57th St.</li>
          <li><strong>Taxi/Rideshare:</strong> Readily available throughout the city.</li>
          <li><strong>Wedding Shuttle:</strong> We will provide a shuttle from the ceremony to the reception venue.</li>
        </ul>
      </section>
    </div>
  );
}

export default TravelPage; 