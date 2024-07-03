document.addEventListener('DOMContentLoaded', function() {
    const baseUrl = '/inventario/obtener_libros/';
    let currentPage = 1;

    function fetchLibros(page) {
        const numero = (page - 1) * 100; // Calcula el offset basado en la página
        fetch(`${baseUrl}?numero=${numero}`)
            .then(response => response.json())
            .then(data => {
                displayLibros(data);
            })
            .catch(error => console.error('Error al obtener los libros:', error));
    }

    function displayLibros(libros) {
        const tbody = document.querySelector('.table tbody');
        tbody.innerHTML = ''; // Limpia la tabla antes de añadir los nuevos libros
        libros.forEach(libro => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${libro.id}</td>
                <td>${libro.titulo}</td>
                <td>$${libro.precio.toFixed(2)}</td>
                <td>${libro.available_quantity}</td>
                <td><button class="btn btn-primary btn-editar">Editar</button></td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Añade evento click a los enlaces de paginación
    document.querySelectorAll('.pagination a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            currentPage = parseInt(this.textContent);
            fetchLibros(currentPage);
        });
    });

    // Carga inicial de libros
    fetchLibros(currentPage);



    // Referencia al formulario dentro del modal
    const agregarLibroForm = document.getElementById('agregarLibroForm');

    agregarLibroForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevenir el comportamiento por defecto del formulario

        // Crear un objeto FormData basado en el formulario
        const formData = new FormData(agregarLibroForm);
        const libroData = {
            titulo: formData.get('titulo'),
            precio: parseFloat(formData.get('precio')),
            cantidad: parseInt(formData.get('cantidad'), 10)
        };

        // Validar los datos del formulario con el esquema de AddLibroSchema
        // Nota: La validación real debería hacerse en el servidor, aquí es solo para fines ilustrativos
        if (!libroData.titulo || isNaN(libroData.precio) || isNaN(libroData.cantidad)) {
            alert('Por favor, complete el formulario correctamente.');
            return;
        }

        // Enviar los datos al servidor
        fetch('/inventario/agregar_libro/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(libroData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                // Cerrar el modal
                $('#agregarLibroModal').modal('hide');
                // Limpiar el formulario
                agregarLibroForm.reset();
                // Recargar la lista de libros
                fetchLibros(1); // Asumiendo que fetchLibros es una función definida para cargar libros
                alert('Libro agregado exitosamente.');
            }
        })
        .catch(error => {
            console.error('Error al agregar el libro:', error);
            alert('Error al agregar el libro. Por favor, intente de nuevo.');
        });
        fetchLibros(currentPage);
    });


    // Añadir evento click a cada botón de editar
    document.querySelector('.table tbody').addEventListener('click', function(e) {
        // Verificar si el elemento clickeado es un botón de editar
        if (e.target.classList.contains('btn-editar')) {
            const row = e.target.closest('tr');
            const id = row.cells[0].textContent;
            const titulo = row.cells[1].textContent;
            const precio = row.cells[2].textContent.replace('$', ''); // Eliminar el símbolo de dólar
            const cantidad = row.cells[3].textContent;

            // Precargar los datos en el formulario de edición
            document.getElementById('tituloLibroEditar').value = titulo;
            document.getElementById('precioLibroEditar').value = precio;
            document.getElementById('cantidadLibroEditar').value = cantidad;
            document.getElementById('idLibroEditar').value = id; // Asegúrate de tener un campo oculto para el ID en tu formulario

            // Abrir el modal de edición
            $('#editarLibroModal').modal('show');
        }
    });

    // Enviar los datos modificados al servidor
    const editarLibroForm = document.getElementById('editarLibroForm');
    editarLibroForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(editarLibroForm);
        const libroData = {
            id: parseInt(formData.get('id'), 10),
            titulo: formData.get('titulo'),
            precio: parseFloat(formData.get('precio')),
            available_quantity: parseInt(formData.get('cantidad'), 10)
        };

        // Enviar los datos al servidor
        fetch('/inventario/editar_libro/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(libroData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                $('#editarLibroModal').modal('hide'); // Cerrar el modal
                editarLibroForm.reset(); // Limpiar el formulario
                fetchLibros(1); // Recargar la lista de libros
                alert('Libro modificado exitosamente.');
            }
        })
        .catch(error => {
            console.error('Error al modificar el libro:', error);
            alert('Error al modificar el libro. Por favor, intente de nuevo.');
        });
    });

    // Encuentra el botón de cerrar sesión por su clase
    const logoutButton = document.querySelector('.logout-button');

    // Asegúrate de que el botón existe para evitar errores
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            // Previene el comportamiento predeterminado del enlace
            event.preventDefault();

            // Envía una solicitud fetch a la ruta de cierre de sesión
            fetch('/auth/logout/', {
                method: 'POST', // Método POST como se define en el backend
                headers: {
                    // Añade cualquier encabezado necesario aquí
                    // Por ejemplo, 'Content-Type': 'application/json'
                    // Si usas CSRF tokens, asegúrate de incluirlo también
                },
                // No es necesario enviar un cuerpo (body) para esta solicitud,
                // a menos que tu backend lo requiera
            })
            .then(response => {
                if (response.ok) {
                    // Si el cierre de sesión fue exitoso, redirige al usuario al directorio raíz
                    window.location.href = '/';
                } else {
                    // Maneja los errores, por ejemplo, mostrando un mensaje al usuario
                    console.error('Error al cerrar sesión');
                }
            })
            .catch(error => {
                // Maneja errores de red
                console.error('Error de red al intentar cerrar sesión:', error);
            });
        });
    }
});