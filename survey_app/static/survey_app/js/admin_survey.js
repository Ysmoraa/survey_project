document.addEventListener('DOMContentLoaded', function() {
    // Confirmación para acciones importantes
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    const publishForms = document.querySelectorAll('form[action*="publish"]');
    const unpublishForms = document.querySelectorAll('form[action*="unpublish"]');
    
    const confirmAction = (forms, message) => {
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!confirm(message)) {
                    e.preventDefault();
                }
            });
        });
    };
    
    confirmAction(deleteForms, '¿Estás seguro de que quieres eliminar esta encuesta? Esta acción no se puede deshacer.');
    confirmAction(publishForms, '¿Estás seguro de que quieres publicar esta encuesta? Los usuarios podrán verla y responderla.');
    confirmAction(unpublishForms, '¿Estás seguro de que quieres despublicar esta encuesta? Los usuarios no podrán responderla.');
    
    // Mejorar accesibilidad
    document.querySelectorAll('.btn').forEach(btn => {
        btn.setAttribute('aria-label', btn.textContent.trim());
    });
});