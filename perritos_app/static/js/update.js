document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form'); // Selecciona el formulario
    const button = document.querySelector('.create__button'); // Selecciona el botón

    button.addEventListener('click', function(event) {
        event.preventDefault(); // Evita el envío predeterminado

        // Selecciona los checkboxes marcados
        const deleteCheckboxes = document.querySelectorAll('input[name="delete_fotos"]:checked');
        const deleteIds = Array.from(deleteCheckboxes).map(cb => cb.value);
        
        // Crea un input oculto para enviar los IDs de las imágenes a eliminar
        if (deleteIds.length > 0) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'delete_fotos';
            input.value = JSON.stringify(deleteIds); // Envía como JSON
            form.appendChild(input);
        }

        form.submit(); // Envía el formulario
    });
});