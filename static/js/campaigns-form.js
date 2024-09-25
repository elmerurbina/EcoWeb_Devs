document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('campaniaForm');
    const submitButton = document.querySelector('.btn-campania');

    submitButton.addEventListener('click', (event) => {
        // Bloquear la validacion por default
        if (!validateForm()) {
            event.preventDefault(); // No permitir el registro con campos obligatorios vacios
            alert('Por favor, complete todos los campos obligatorios.'); // Mensaje a mostrar
        }
    });

    function validateForm() {
        let isValid = true;

        // Cargar todos los campos obligatorios
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.border = '1px solid red'; // Agregar un borde rojo a los campos obligatorios
            } else {
                field.style.border = '';
            }
        });

        return isValid;
    }
});

document.getElementById('hamburger-menu').addEventListener('click', function() {
    const menu = document.getElementById('menu-items');
    menu.classList.toggle('hidden');
});
