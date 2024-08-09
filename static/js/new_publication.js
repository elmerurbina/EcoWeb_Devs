document.getElementById('publicationForm').addEventListener('submit', function(event) {
    const title = document.getElementById('title').value.trim();
    const category = document.getElementById('category').value;
    const content = document.getElementById('content').value.trim();


    if (!title || !category || !content) {
        alert('Por favor, completa todos los campos requeridos.');
        event.preventDefault();
    }
});

document.getElementById('image').addEventListener('change', function() {
    const fileName = this.files[0] ? this.files[0].name : 'Ningún archivo seleccionado';
    console.log(fileName);
});