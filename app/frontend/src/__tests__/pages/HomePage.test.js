import React from 'react';
import { render, screen } from '@testing-library/react';
import HomePage from '../../pages/HomePage';

// Mock the RSVPForm component to isolate HomePage testing
jest.mock('../../components/RSVPForm', () => () => (
  <div data-testid="rsvp-form-mock">RSVP Form Component</div>
));

describe('HomePage Component', () => {
  test('renders wedding information correctly', () => {
    render(<HomePage />);
    
    // Check wedding details
    expect(screen.getByText('יהל & אסף')).toBeInTheDocument();
    expect(screen.getByText('כ״ה באייר תשפ״ה • 23.05.2025')).toBeInTheDocument();
    
    // The location appears multiple times, so we need to check differently
    const locationElements = screen.getAllByText('הלורנס, הצורפים 18, תל אביב-יפו');
    expect(locationElements.length).toBeGreaterThan(0);
  });

  test('renders wedding sections', () => {
    render(<HomePage />);
    
    // Check for main sections
    expect(screen.getByText('פרטי האירוע')).toBeInTheDocument();
    expect(screen.getByText('קבלת פנים')).toBeInTheDocument();
    expect(screen.getByText('חופה')).toBeInTheDocument();
    expect(screen.getByText('מסיבה')).toBeInTheDocument();
    
    // Check that RSVP form is included
    expect(screen.getByTestId('rsvp-form-mock')).toBeInTheDocument();
  });
}); 