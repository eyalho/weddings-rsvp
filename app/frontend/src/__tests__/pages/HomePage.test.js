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
    expect(screen.getByText('John & Jane')).toBeInTheDocument();
    expect(screen.getByText('June 15, 2024')).toBeInTheDocument();
    expect(screen.getByText('Central Park, New York')).toBeInTheDocument();
  });

  test('renders wedding sections', () => {
    render(<HomePage />);
    
    // Check for main sections
    expect(screen.getByText('Wedding Details')).toBeInTheDocument();
    expect(screen.getByText('Ceremony')).toBeInTheDocument();
    expect(screen.getByText('Reception')).toBeInTheDocument();
    
    // Check that RSVP form is included
    expect(screen.getByTestId('rsvp-form-mock')).toBeInTheDocument();
  });
}); 