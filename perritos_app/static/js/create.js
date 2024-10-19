document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form'); // Selecciona el formulario
    const button = document.querySelector('.create__button'); // Selecciona el botón

    button.addEventListener('click', function(event) {
        event.preventDefault(); // Evita el envío predeterminado

        // Aquí puedes realizar validaciones si es necesario

        form.submit(); // Envía el formulario
    });
});