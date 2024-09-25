document.addEventListener('DOMContentLoaded', (event) => {
    // Show the form based on the form type
    const formType = "{{ form_type }}";
    if (formType) {
        document.getElementById(formType).style.display = 'block';
    }

    // Handle the toggle of answer forms
    document.querySelectorAll('.responder-button').forEach(button => {
        button.addEventListener('click', () => {
            toggleAnswerForm(button);
        });
    });

    // Handle form submission
    document.querySelectorAll('.forum-form').forEach(form => {
        form.addEventListener('submit', (event) => {
            const formId = form.getAttribute('id');
            if (!validateForm(formId)) {
                event.preventDefault();
            }
        });
    });
});

// Function to toggle the answer form visibility
function toggleAnswerForm(button) {
    const answerForm = button.nextElementSibling;
    answerForm.style.display = (answerForm.style.display === 'none' || answerForm.style.display === '') ? 'block' : 'none';
}

// Function to validate fields
function validateForm(formId) {
    const form = document.getElementById(formId);
    const errorElements = form.querySelectorAll('.error-message');
    errorElements.forEach(element => element.textContent = '');

    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    inputs.forEach(input => {
        const errorId = input.id + '-error';
        const errorElement = document.getElementById(errorId);

        if (!input.value.trim()) {
            errorElement.textContent = 'Este campo es obligatorio.';
            input.style.borderColor = 'red';
            isValid = false;
        } else {
            input.style.borderColor = ''; // Reset border color if valid
        }
    });

    return isValid;
}
