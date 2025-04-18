import React from 'react';

function RegistryPage() {
  const registries = [
    {
      id: 1,
      name: 'מתנה כספית',
      logo: 'https://via.placeholder.com/150x80?text=מתנה+כספית',
      description: 'נשמח לקבל את ברכתכם באמצעות מתנה כספית שתעזור לנו להתחיל את חיינו המשותפים.',
      url: '#',
    },
    {
      id: 2,
      name: 'טרמינל X',
      logo: 'https://via.placeholder.com/150x80?text=טרמינל+X',
      description: 'רשימת מתנות לבית החדש שלנו.',
      url: 'https://www.terminalx.com/registry',
    },
    {
      id: 3,
      name: 'ירושלמי',
      logo: 'https://via.placeholder.com/150x80?text=ירושלמי',
      description: 'רשימת מתנות וריהוט.',
      url: 'https://www.yerushalmi.co.il',
    },
    {
      id: 4,
      name: 'הירושה לעתיד',
      logo: 'https://via.placeholder.com/150x80?text=הירושה+לעתיד',
      description: 'במקום מתנה, אנא שקלו לתרום לארגון חברתי שקרוב לליבנו.',
      url: 'https://www.future-inheritance.org',
    }
  ];

  return (
    <div className="registry-page">
      <h1>מתנות</h1>
      
      <div className="registry-intro">
        <p>
          תודה שאתם שוקלים להעניק לנו מתנה לרגל החתונה. הנוכחות שלכם ביום המיוחד שלנו היא המתנה הגדולה ביותר,
          אך אם ברצונכם לחגוג איתנו עם מתנה, הנה כמה אפשרויות:
        </p>
      </div>
      
      <div className="registry-list">
        {registries.map(registry => (
          <div key={registry.id} className="registry-card">
            <div className="registry-logo">
              <img src={registry.logo} alt={`לוגו של ${registry.name}`} />
            </div>
            <div className="registry-info">
              <h3>{registry.name}</h3>
              <p>{registry.description}</p>
              {registry.url !== '#' && (
                <a 
                  href={registry.url} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="registry-button"
                >
                  לצפייה ברשימה
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
      
      <div className="registry-note">
        <h3>הערה בנוגע למתנות</h3>
        <p>
          רבים מכם מגיעים מרחוק כדי להצטרף אלינו, ואנו מבינים את העלויות הכרוכות בכך.
          אנא דעו שהנוכחות שלכם חשובה לנו יותר מכל מתנה חומרית, ואנו פשוט נרגשים לחגוג איתכם ביום המיוחד שלנו!
        </p>
        <p>
          אם תבחרו לשלוח מתנה פיזית במקום לרכוש מאחת הרשימות, אנא שלחו אותה לכתובת:
        </p>
        <address>
          יהל ואסף<br />
          רחוב האהבה 123<br />
          תל אביב, 6100000
        </address>
      </div>
    </div>
  );
}

export default RegistryPage; 