document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevenir el comportamiento por defecto del formulario

        // Recoger los datos del formulario
        const correoElectronico = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            // Enviar los datos al servidor
            const response = await fetch('/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ correo_electronico: correoElectronico, password: password })
            });

            if (response.ok) {
                const data = await response.json(); // Parsear la respuesta JSON
                let redirectTo = ''; // Inicializar la variable de redirección
            
                // Determinar la redirección basada en el id_grupo
                switch (data.usuario.id_grupo) {
                    case 1:
                        redirectTo = 'admin/index.html';
                        break;
                    case 2:
                        redirectTo = 'vendedor/ventas.html';
                        break;
                    case 3:
                        redirectTo = 'almacenista/index.html';
                        break;
                    default:
                        console.error('Grupo de usuario no reconocido');
                        return; // Salir si el id_grupo no es reconocido
                }
            
                // Redireccionar al usuario a la página correspondiente
                window.location.href = redirectTo;
            } else  {
                // Solo intentar analizar como JSON si hay contenido
                if (response.headers.get("content-length") !== "0") {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Error al iniciar sesión');
                } else {
                    throw new Error('Error al iniciar sesión sin mensaje de error específico');
                }
            }

            // Verificar si hay contenido antes de intentar analizarlo
            if (response.headers.get("content-length") !== "0") {
                const data = await response.json(); // Suponiendo que el servidor responde con datos útiles después del inicio de sesión
                alert('Inicio de sesión exitoso');
                // Manejar la respuesta del servidor, por ejemplo, guardar el token de sesión, redirigir, etc.
            } else {
                // Manejar el caso de éxito sin cuerpo
                alert('Inicio de sesión exitoso, sin datos adicionales.');
                // Redirigir al usuario o actualizar la UI según sea necesario
            }
        } catch (error) {
            console.error('Error al iniciar sesión:', error);
            alert(`Error al iniciar sesión: ${error.message}`);
        }
    });
});