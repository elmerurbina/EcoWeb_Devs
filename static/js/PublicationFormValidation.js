document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('publicationForm');
    const submitButton = form.querySelector('button[type="submit"]');

    submitButton.addEventListener('click', (event) => {
        // No enviar formularios sin llenar todos los campos requeridos
        if (!validateForm()) {
            event.preventDefault();
            alert('Por favor, completa todos los campos obligatorios.');
        }
    });

    function validateForm() {
        let isValid = true;

       // Cargar todos los campos requeridos
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.border = '1px solid red'; // Agregar un borde rojo a los campos requeridos
            } else {
                field.style.border = ''; // Cuando el usuario empieza a escribir, quitar el color rojo
            }
        });

        // Comprueba si existe imagen seleccionada
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
