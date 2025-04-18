import React from 'react';

function RegistryPage() {
  const registries = [
    {
      id: 1,
      name: 'Crate & Barrel',
      logo: 'https://via.placeholder.com/150x80?text=Crate+%26+Barrel',
      description: 'Kitchen and home goods for our new apartment.',
      url: 'https://www.crateandbarrel.com/gift-registry/',
    },
    {
      id: 2,
      name: 'Zola',
      logo: 'https://via.placeholder.com/150x80?text=Zola',
      description: 'Our main registry with various items and experiences.',
      url: 'https://www.zola.com/registry/',
    },
    {
      id: 3,
      name: 'Honeymoon Fund',
      logo: 'https://via.placeholder.com/150x80?text=Honeymoon+Fund',
      description: 'Contribute to our dream honeymoon in Bali.',
      url: 'https://www.honeyfund.com',
    },
    {
      id: 4,
      name: 'Charity: Water',
      logo: 'https://via.placeholder.com/150x80?text=Charity+Water',
      description: 'In lieu of gifts, consider donating to this charity that\'s close to our hearts.',
      url: 'https://www.charitywater.org',
    }
  ];

  return (
    <div className="registry-page">
      <h1>Gift Registry</h1>
      
      <div className="registry-intro">
        <p>
          Thank you for considering a gift for our wedding. Your presence on our special day is the greatest gift of all, 
          but if you'd like to help us celebrate with a present, we've registered at the following places:
        </p>
      </div>
      
      <div className="registry-list">
        {registries.map(registry => (
          <div key={registry.id} className="registry-card">
            <div className="registry-logo">
              <img src={registry.logo} alt={`${registry.name} logo`} />
            </div>
            <div className="registry-info">
              <h3>{registry.name}</h3>
              <p>{registry.description}</p>
              <a 
                href={registry.url} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="registry-button"
              >
                View Registry
              </a>
            </div>
          </div>
        ))}
      </div>
      
      <div className="registry-note">
        <h3>A Note About Gifts</h3>
        <p>
          Many of you are traveling from afar to join us, and we understand the costs associated with that. 
          Please know that your presence means more to us than any material gift, and we're just excited to 
          have you celebrate with us on our special day!
        </p>
        <p>
          If you choose to send a physical gift rather than purchasing from our registry, please have it shipped to:
        </p>
        <address>
          John &amp; Jane Smith<br />
          123 Wedding Lane<br />
          New York, NY 10001
        </address>
      </div>
    </div>
  );
}

export default RegistryPage; 