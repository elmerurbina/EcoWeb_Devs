// La funcion de este codigo es mostrar el mensaje de suscrpcion exitosa cuando se suscribe al correo
document.getElementById('subscribeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var emailInput = document.getElementById('email');
    var message = document.getElementById('message');

    if (validateEmail(emailInput.value)) {
        message.textContent = 'Suscripción realizada con éxito';
        message.style.color = 'green';
    } else {
        message.textContent = 'Por favor, ingresa un correo electrónico válido';
        message.style.color = 'red';
    }

    message.style.display = 'block';
});

function validateEmail(email) {
    var re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return re.test(String(email).toLowerCase());
}
