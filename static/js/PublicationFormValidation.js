document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('publicationForm');
    const submitButton = form.querySelector('button[type="submit"]');

    submitButton.addEventListener('click', (event) => {
        // Prevent form submission if validation fails
        if (!validateForm()) {
            event.preventDefault(); // Prevent form from being submitted
            alert('Por favor, completa todos los campos obligatorios.');
        }
    });

    function validateForm() {
        let isValid = true;

        // Get all required fields
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.border = '1px solid red'; // Highlight empty required fields
            } else {
                field.style.border = ''; // Remove highlight if field is filled
            }
        });

        // Check if file input has a file selected
        const fileInput = form.querySelector('input[type="file"]');
        if (fileInput && fileInput.files.length === 0) {
            fileInput.style.border = '1px solid red'; // Highlight file input if no file is selected
            isValid = false;
        } else {
            fileInput.style.border = ''; // Remove highlight if a file is selected
        }

        return isValid;
    }
});
