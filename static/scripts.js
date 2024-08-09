document.addEventListener('DOMContentLoaded', function() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        const toggleButton = document.createElement('button');
        toggleButton.type = 'button';
        toggleButton.textContent = 'Show';
        toggleButton.style.marginLeft = '1px';

        toggleButton.addEventListener('click', function() {
            if (field.type === 'password') {
                field.type = 'text';
                toggleButton.textContent = 'Hide';
            } else {
                field.type = 'password';
                toggleButton.textContent = 'Show';
            }
        });

        field.parentElement.appendChild(toggleButton);
    });
});
