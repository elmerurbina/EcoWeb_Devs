document.addEventListener('DOMContentLoaded', function() {
    // Function to validate the form
    function validateForm(form) {
        let isValid = true;

        // Remove previous error messages
        form.querySelectorAll('.error-message').forEach(el => el.remove());

        // Check if required fields are filled
        form.querySelectorAll('[required]').forEach(input => {
            const label = input.previousElementSibling.textContent.trim();
            if (input.value.trim() === '') {
                isValid = false;
                displayErrorMessage(input, `El campo ${label} es obligatorio.`);
            }
        });

        // Additional validations for specific fields
        const titulo = form.querySelector('#titulo');
        if (titulo && titulo.value.trim().length < 5) {
            isValid = false;
            displayErrorMessage(titulo, 'El título debe tener al menos 5 caracteres.');
        }

        const descripcion = form.querySelector('#descripcion');
        if (descripcion && descripcion.value.trim().length < 10) {
            isValid = false;
            displayErrorMessage(descripcion, 'La descripción debe tener al menos 10 caracteres.');
        }

        // Validate file input (optional example)
        const evidencia = form.querySelector('#evidencia');
        if (evidencia && evidencia.files.length === 0) {
            isValid = false;
            displayErrorMessage(evidencia, 'Debes seleccionar un archivo para la evidencia.');
        }

        return isValid;
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

    // Attach event listener to the form
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!validateForm(form)) {
                event.preventDefault(); // Prevent form submission if validation fails
            }
        });
    }
});
