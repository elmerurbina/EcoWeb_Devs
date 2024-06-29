document.addEventListener('DOMContentLoaded', (event) => {
    const formType = "{{ form_type }}";
    if (formType) {
        document.getElementById(formType).style.display = 'block';
    }

    // Smooth scroll for menu links
    document.querySelectorAll('.fixed-menu a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
