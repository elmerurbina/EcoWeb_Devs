// Este codigo redirige a la ruta del sistema de autenticacion cuando se hace click en un boton del foro
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btnPregunta').addEventListener('click', function() {
        redirectToLogin();
    });

    document.getElementById('btnDebate').addEventListener('click', function() {
        redirectToLogin();
    });

    document.getElementById('btnHilo').addEventListener('click', function() {
        redirectToLogin();
    });

    function redirectToLogin() {
        window.location.href = '/login';
    }
});
