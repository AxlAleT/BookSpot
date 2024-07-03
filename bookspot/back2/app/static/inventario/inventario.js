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
                <td><button class="btn btn-primary">Editar</button></td>
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
});