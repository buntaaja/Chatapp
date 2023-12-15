document.addEventListener('DOMContentLoaded', () => {
    // Make 'enter' key submit message
    let msg = document.querySelector('#user_message');
    
    msg.addEventListener('keydown', event => {
        if (event.keyCode === 13) {
            event.preventDefault();
            document.querySelector('#send_message').click();
            msg.value = '';  // Clear the input field after sending the message
        }
    });
});