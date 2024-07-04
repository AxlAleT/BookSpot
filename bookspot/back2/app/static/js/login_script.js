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
                const data = await response.json(); // Parsear la respuesta JSON una sola vez aquí

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
                        redirectTo = '/almacenista/inventario.html';
                        break;
                    default:
                        console.error('Grupo de usuario no reconocido');
                        return; // Salir si el id_grupo no es reconocido
                }
            
                // Redireccionar al usuario a la página correspondiente
                window.location.href = redirectTo;

                // Opcional: mostrar mensaje de éxito aquí si es necesario
                alert('Inicio de sesión exitoso');
            } else {
                // Solo intentar analizar como JSON si hay contenido
                if (response.headers.get("content-length") !== "0") {
                    const errorData = await response.json(); // Aquí ya no deberías leer la respuesta nuevamente
                    throw new Error(errorData.error || 'Error al iniciar sesión');
                } else {
                    throw new Error('Error al iniciar sesión sin mensaje de error específico');
                }
            }
        } catch (error) {
            console.error('Error al iniciar sesión:', error);
            alert(`Error al iniciar sesión: ${error.message}`);
        }
    });
});