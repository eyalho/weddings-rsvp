import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/RsvpStatus.css';

const RsvpStatusPage = () => {
  const [stats, setStats] = useState({
    total_guests: 0,
    attending_guests: 0,
    not_attending_guests: 0,
    attendance_rate: 0,
    total_responses: 0
  });
  
  const [guests, setGuests] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchMode, setSearchMode] = useState(false);
  
  const guestsPerPage = 10;
  
  // Function to fetch RSVP statistics
  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/v1/rsvp/stats');
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching RSVP statistics:', err);
      setError('Failed to load RSVP statistics. Please try again later.');
    }
  };
  
  // Function to fetch guests
  const fetchGuests = async (page = 1) => {
    setLoading(true);
    try {
      const skip = (page - 1) * guestsPerPage;
      const response = await axios.get(`/api/v1/rsvp/guests?skip=${skip}&limit=${guestsPerPage}`);
      setGuests(response.data);
      setSearchMode(false);
      setError(null);
    } catch (err) {
      console.error('Error fetching guests:', err);
      setError('Failed to load guest information. Please try again later.');
    } finally {
      setLoading(false);
    }
  };
  
  // Function to search guests
  const searchGuests = async () => {
    if (!searchQuery.trim()) {
      fetchGuests(1);
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.get(`/api/v1/rsvp/guests/search?query=${encodeURIComponent(searchQuery)}`);
      setGuests(response.data);
      setSearchMode(true);
      setError(null);
    } catch (err) {
      console.error('Error searching guests:', err);
      setError('Search failed. Please try again later.');
    } finally {
      setLoading(false);
    }
  };
  
  // Load initial data
  useEffect(() => {
    fetchStats();
    fetchGuests();
  }, []);
  
  // Handle pagination
  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    fetchGuests(newPage);
  };
  
  // Handle search
  const handleSearch = (e) => {
    e.preventDefault();
    searchGuests();
  };
  
  // Reset search
  const handleReset = () => {
    setSearchQuery('');
    fetchGuests(1);
  };
  
  // Format date helper
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('he-IL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  return (
    <div className="rsvp-status-container">
      <h1>סטטוס הגעה</h1>
      
      {/* RSVP Statistics */}
      <div className="rsvp-stats">
        <div className="stat-card">
          <h3>סה"כ אורחים</h3>
          <p className="stat-value">{stats.total_guests}</p>
        </div>
        
        <div className="stat-card">
          <h3>מגיעים</h3>
          <p className="stat-value">{stats.attending_guests}</p>
        </div>
        
        <div className="stat-card">
          <h3>לא מגיעים</h3>
          <p className="stat-value">{stats.not_attending_guests}</p>
        </div>
        
        <div className="stat-card">
          <h3>אחוז הגעה</h3>
          <p className="stat-value">{stats.attendance_rate.toFixed(1)}%</p>
        </div>
      </div>
      
      {/* Search Form */}
      <div className="search-container">
        <form onSubmit={handleSearch}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="חיפוש לפי שם או מספר טלפון"
            className="search-input"
          />
          <button type="submit" className="search-button">חיפוש</button>
          <button type="button" onClick={handleReset} className="reset-button">איפוס</button>
        </form>
      </div>
      
      {/* Error Message */}
      {error && <div className="error-message">{error}</div>}
      
      {/* Loading Indicator */}
      {loading ? (
        <div className="loading">טוען נתונים...</div>
      ) : (
        <>
          {/* Guest Table */}
          <div className="guest-table-container">
            <table className="guest-table">
              <thead>
                <tr>
                  <th>שם</th>
                  <th>סטטוס</th>
                  <th>מספר טלפון</th>
                  <th>הגבלות תזונתיות</th>
                  <th>תאריך עדכון</th>
                </tr>
              </thead>
              <tbody>
                {guests.length > 0 ? (
                  guests.map(guest => (
                    <tr key={guest.id}>
                      <td>{guest.name}</td>
                      <td className={guest.attending ? 'attending' : 'not-attending'}>
                        {guest.attending ? 'מגיע/ה' : 'לא מגיע/ה'}
                      </td>
                      <td dir="ltr">{guest.phone_number}</td>
                      <td>{guest.dietary_restrictions || 'אין'}</td>
                      <td>{formatDate(guest.updated_at)}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="no-results">אין תוצאות</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          
          {/* Pagination */}
          {!searchMode && guests.length > 0 && (
            <div className="pagination">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="page-button"
              >
                הקודם
              </button>
              <span className="page-indicator">עמוד {currentPage}</span>
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={guests.length < guestsPerPage}
                className="page-button"
              >
                הבא
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default RsvpStatusPage; 