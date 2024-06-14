// JavaScript to handle button clicks and redirect to login route
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
