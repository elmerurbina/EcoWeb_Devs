document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/recognize', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.species_info) {
            document.getElementById('species-name').textContent = data.species_info.name || 'No disponible';
            document.getElementById('species-description').textContent = data.species_info.wikipedia_summary || 'No disponible';
            // Update species image URL if applicable
            document.getElementById('species-image').src = data.species_info.image_url || '';
        } else {
            document.getElementById('species-name').textContent = 'Error';
            document.getElementById('species-description').textContent = 'No se pudo reconocer la especie.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('species-name').textContent = 'Error';
        document.getElementById('species-description').textContent = 'No se pudo procesar la solicitud.';
    });
});
