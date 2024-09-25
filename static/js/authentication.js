// Check to which form user want to load
const sign_in_container = document.querySelector('.sign-in-container'), 
      sign_up_container = document.querySelector('.sign-up-container');

document.addEventListener('click', e => {
    if (e.target.matches('.ok-account')) {
        sign_in_container.style.display = 'block';
        sign_up_container.style.display = 'none';
    } else if (e.target.matches('.no-account')) {
        sign_up_container.style.display = 'block';
        sign_in_container.style.display = 'none';
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // Validate the form
    function validateForm(form) {
        let isValid = true;

        form.querySelectorAll('.error-message').forEach(el => el.remove());

        // Check if required fields are filled
        form.querySelectorAll('[required]').forEach(input => {
            const errorMessage = input.nextElementSibling; // Assume error message will be the next sibling
            if (input.value.trim() === '') {
                isValid = false;
                displayErrorMessage(input, `El campo ${input.placeholder} es obligatorio.`);
            }
        });

        // Validate password strength for registration
        if (form.id === 'register-form') {
            const password = form.querySelector('#register-password').value;
            const confirmPassword = form.querySelector('#register-confirm-password').value;
            if (!validatePassword(password)) {
                isValid = false;
                displayErrorMessage(form.querySelector('#register-password'), 'La contraseña debe tener al menos 6 caracteres, incluyendo una letra mayúscula, una letra minúscula y un número.');
            }
            if (password !== confirmPassword) {
                isValid = false;
                displayErrorMessage(form.querySelector('#register-confirm-password'), 'Las contraseñas no coinciden.');
            }
        }

        return isValid;
    }

    // Function to validate password strength
    function validatePassword(password) {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}$/;
        return passwordRegex.test(password);
    }

    // Function to display error messages below input fields
    function displayErrorMessage(input, message) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = message;
        // Remove any existing error message
        if (input.nextElementSibling && input.nextElementSibling.classList.contains('error-message')) {
            input.nextElementSibling.remove();
        }
        input.parentNode.insertBefore(errorMessage, input.nextSibling);
    }

    // Attach event listeners to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(form)) {
                event.preventDefault(); // Prevent form submission
            }
        });
    });
});
