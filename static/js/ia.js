document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const imageInput = document.getElementById('image');
    const errorMessage = document.createElement('p');
    errorMessage.id = "error-message";
    errorMessage.style.color = "red";

    // Remove any previous error message
    const existingErrorMessage = document.getElementById('error-message');
    if (existingErrorMessage) {
        existingErrorMessage.remove();
    }

    // Check if the user selected an image
    if (!imageInput.files.length) {
        errorMessage.textContent = 'Por favor proporcionar una imagen';
        document.getElementById('upload-form').appendChild(errorMessage);
        return;
    }

    const formData = new FormData(this);

    // Show the uploaded image in the 'species-image' element
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('species-image').src = e.target.result;
    };
    reader.readAsDataURL(imageInput.files[0]);

    // Send the form data to the server
    fetch('/recognize', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.species_info) {
           document.getElementById('species-name').textContent = data.species_info.name || 'No disponible';
    document.getElementById('species-description').textContent = data.species_info.description || 'No disponible';
        } else {
            document.getElementById('species-name').textContent = 'Error';
            document.getElementById('species-description').textContent = 'No se pudo reconocer la especie';
            // Show error message in red
            errorMessage.textContent = 'No se pudo procesar la solicitud.';
            document.getElementById('upload-form').appendChild(errorMessage);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('species-name').textContent = 'Error';
        document.getElementById('species-description').textContent = 'No se pudo procesar la solicitud.';
        // Show error message in red
        errorMessage.textContent = 'Error al procesar la solicitud.';
        document.getElementById('upload-form').appendChild(errorMessage);
    });
});
