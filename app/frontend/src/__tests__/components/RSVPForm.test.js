import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RSVPForm from '../../components/RSVPForm';

describe('RSVPForm Component', () => {
  test('renders form elements correctly', () => {
    render(<RSVPForm />);
    
    // Check if important elements exist
    expect(screen.getByText('אישור הגעה')).toBeInTheDocument();
    expect(screen.getByLabelText(/שם מלא/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/טלפון נייד/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/אשמח להגיע לחגוג איתכם/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /שליחה/i })).toBeInTheDocument();
  });

  test('updates form values on input change', () => {
    render(<RSVPForm />);
    
    // Get form inputs
    const nameInput = screen.getByLabelText(/שם מלא/i);
    const phoneInput = screen.getByLabelText(/טלפון נייד/i);
    const attendingCheckbox = screen.getByLabelText(/אשמח להגיע לחגוג איתכם/i);
    
    // Simulate user input
    fireEvent.change(nameInput, { target: { value: 'ישראל ישראלי' } });
    fireEvent.change(phoneInput, { target: { value: '050-1234567' } });
    fireEvent.click(attendingCheckbox); // Toggle from true to false
    
    // Check if the inputs reflect the changes
    expect(nameInput.value).toBe('ישראל ישראלי');
    expect(phoneInput.value).toBe('050-1234567');
    expect(attendingCheckbox.checked).toBe(false);
  });
}); 