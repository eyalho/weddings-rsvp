import React, { useState } from 'react';
import RsvpStatusPage from './RsvpStatusPage';
import '../styles/AdminPage.css';

const AdminPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  // Simple authentication - in a real app, you would use a more secure method
  const adminPassword = 'wedding2025'; // This should be stored securely in a real app
  
  const handleLogin = (e) => {
    e.preventDefault();
    
    if (password === adminPassword) {
      setIsAuthenticated(true);
      setError('');
    } else {
      setError('הסיסמה שהזנת שגויה. נסה שנית.');
    }
  };
  
  if (!isAuthenticated) {
    return (
      <div className="admin-login-container">
        <div className="login-card">
          <h1>אזור מנהל</h1>
          <p className="login-instruction">הזן את הסיסמה כדי לצפות בסטטוס ההגעות</p>
          
          {error && <div className="login-error">{error}</div>}
          
          <form onSubmit={handleLogin} className="login-form">
            <div className="form-group">
              <label htmlFor="password">סיסמה:</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
              />
            </div>
            <button type="submit" className="login-button">כניסה</button>
          </form>
        </div>
      </div>
    );
  }
  
  return (
    <div className="admin-page-container">
      <div className="admin-header">
        <h1>אזור מנהל</h1>
        <button 
          className="logout-button"
          onClick={() => setIsAuthenticated(false)}
        >
          יציאה
        </button>
      </div>
      
      <RsvpStatusPage />
    </div>
  );
};

export default AdminPage; 