document.addEventListener('DOMContentLoaded', function() {
    const rsvpForm = document.getElementById('rsvp-form');
    const responseMessage = document.getElementById('response-message');

    rsvpForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const attending = document.querySelector('input[name="attending"]:checked').value;

        if (name === '') {
            alert('Please enter your name.');
            return;
        }

        responseMessage.textContent = `Thank you, ${name}! Your response has been recorded: ${attending === 'yes' ? 'Attending' : 'Not Attending'}.`;
        rsvpForm.reset();
    });
});