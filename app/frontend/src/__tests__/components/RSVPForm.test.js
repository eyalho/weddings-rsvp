import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RSVPForm from '../../components/RSVPForm';

describe('RSVPForm Component', () => {
  test('renders form elements correctly', () => {
    render(<RSVPForm />);
    
    // Check if important elements exist
    expect(screen.getByText('RSVP to our Wedding')).toBeInTheDocument();
    expect(screen.getByLabelText(/Full Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/I will attend the wedding/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Submit RSVP/i })).toBeInTheDocument();
  });

  test('updates form values on input change', () => {
    render(<RSVPForm />);
    
    // Get form inputs
    const nameInput = screen.getByLabelText(/Full Name/i);
    const emailInput = screen.getByLabelText(/Email/i);
    const attendingCheckbox = screen.getByLabelText(/I will attend the wedding/i);
    
    // Simulate user input
    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.click(attendingCheckbox); // Toggle from true to false
    
    // Check if the inputs reflect the changes
    expect(nameInput.value).toBe('John Doe');
    expect(emailInput.value).toBe('john@example.com');
    expect(attendingCheckbox.checked).toBe(false);
  });
}); 