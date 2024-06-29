document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevenir el comportamiento por defecto del formulario

        // Recoger los datos del formulario
        const usuario = loginForm.querySelector('input[type="text"]').value;
        const password = loginForm.querySelector('input[type="password"]').value;

        try {
            // Enviar los datos al servidor
            const response = await fetch('/login/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ correo_electronico: usuario, password: password })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error al iniciar sesión');
            }

            const data = await response.json(); // Suponiendo que el servidor responde con datos útiles después del inicio de sesión
            alert(data.message); // Mostrar mensaje de éxito
            // Aquí puedes redirigir al usuario o actualizar la UI según sea necesario
        } catch (error) {
            console.error('Error al iniciar sesión:', error);
            alert(`Error al iniciar sesión: ${error.message}`);
        }
    });
});
