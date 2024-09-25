document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('publicationForm');
    const submitButton = form.querySelector('button[type="submit"]');

    submitButton.addEventListener('click', (event) => {
        // Ensure that all required fields are filled
        if (!validateForm()) {
            event.preventDefault();
            alert('Por favor, completa todos los campos obligatorios.');
        }
    });

    function validateForm() {
        let isValid = true;

       // Load all the required data
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.border = '1px solid red'; // Add a red border to the required fields
            } else {
                field.style.border = ''; // Remove the red border when user start typing
            }
        });

        // Ensure that there are a selected image
        const fileInput = form.querySelector('input[type="file"]');
        if (fileInput && fileInput.files.length === 0) {
            fileInput.style.border = '1px solid red';
            isValid = false;
        } else {
            fileInput.style.border = '';
        }

        return isValid;
    }
});
