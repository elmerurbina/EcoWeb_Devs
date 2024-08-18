document.getElementById('recover-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const messageDiv = document.getElementById('message');

    if (validateEmail(email)) {
        messageDiv.textContent = 'Se ha enviado un correo electrónico a ' + email + ' con las instrucciones para recuperar tu cuenta.';
        messageDiv.style.color = 'green';
    } else {
        messageDiv.textContent = 'Por favor, introduce un correo electrónico válido.';
        messageDiv.style.color = 'red';
    }
});

// Simple email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}
