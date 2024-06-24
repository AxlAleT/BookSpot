document.addEventListener("DOMContentLoaded", function() {
    const menuItems = document.querySelectorAll(".menu li");
    const sections = document.querySelectorAll(".section");
    const searchInput = document.getElementById("search-input");

    menuItems.forEach(item => {
        item.addEventListener("click", function() {
            // Ocultar todas las secciones
            sections.forEach(section => {
                section.classList.remove("active");
            });

            // Obtener la sección correspondiente al menú clicado
            const sectionId = this.getAttribute("data-section");
            const sectionToShow = document.getElementById(sectionId);

            // Mostrar la sección correspondiente
            if (sectionToShow) {
                sectionToShow.classList.add("active");
            }
        });
    });

    // Muestra el formulario para agregar un nuevo libro
    window.mostrarFormularioAgregar = function() {
        document.getElementById("add-book-form").style.display = "block";
    }

    // Maneja el envío del formulario para agregar un nuevo libro
    document.getElementById("form-agregar-libro").addEventListener("submit", function(event) {
        event.preventDefault();

        const titulo = document.getElementById("titulo").value;
        const precio = document.getElementById("precio").value;
        const cantidad = document.getElementById("cantidad").value;

        fetch("/api/inventario/agregar_libro/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ titulo, precio, cantidad })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("Libro agregado exitosamente.");
                // Actualiza la tabla de inventario
                actualizarInventario();
                // Ocultar el formulario de agregar libro
                document.getElementById("add-book-form").style.display = "none";
                // Limpiar el formulario
                document.getElementById("form-agregar-libro").reset();
            }
        })
        .catch(error => {
            alert("Error: " + error);
        });
    });

    // Función para actualizar la tabla de inventario
    function actualizarInventario() {
        fetch("/api/inventario/obtener_libros/?numero=0")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("inventory-table-body");
            tableBody.innerHTML = "";

            data.forEach(libro => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${libro.id}</td>
                    <td>${libro.titulo}</td>
                    <td>${libro.precio}</td>
                    <td>${libro.available_quantity}</td>
                    <td>
                        <button class="btn edit" data-id="${libro.id}">Editar</button>
                        <button class="btn delete" data-id="${libro.id}">Eliminar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Añadir eventos de edición y eliminación a los botones
            const editButtons = document.querySelectorAll(".btn.edit");
            const deleteButtons = document.querySelectorAll(".btn.delete");

            editButtons.forEach(button => {
                button.addEventListener("click", function() {
                    const libroId = this.getAttribute("data-id");
                    const libro = data.find(libro => libro.id === parseInt(libroId));
                    if (libro) {
                        abrirFormularioEditar(libro);
                    }
                });
            });

            deleteButtons.forEach(button => {
                button.addEventListener("click", function() {
                    const libroId = this.getAttribute("data-id");
                    eliminarLibro(libroId);
                });
            });
        })
        .catch(error => {
            console.error("Error al obtener el inventario:", error);
        });
    }

    // Función para abrir el formulario modal de edición de libro
    function abrirFormularioEditar(libro) {
        const modal = document.getElementById("edit-book-modal");
        modal.style.display = "block";

        // Llenar el formulario con los datos actuales del libro
        document.getElementById("edit-id").value = libro.id;
        document.getElementById("edit-titulo").value = libro.titulo;
        document.getElementById("edit-precio").value = libro.precio;
        document.getElementById("edit-cantidad").value = libro.available_quantity;

        // Manejar el envío del formulario de edición
        document.getElementById("form-editar-libro").addEventListener("submit", function(event) {
            event.preventDefault();

            const id = document.getElementById("edit-id").value;
            const titulo = document.getElementById("edit-titulo").value;
            const precio = document.getElementById("edit-precio").value;
            const cantidad = document.getElementById("edit-cantidad").value;

            fetch(`/api/inventario/editar_libro/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ titulo, precio, available_quantity: cantidad })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    alert("Libro editado exitosamente.");
                    // Actualiza la tabla de inventario
                    actualizarInventario();
                    // Cierra el modal de edición
                    modal.style.display = "none";
                    // Limpiar el formulario
                    document.getElementById("form-editar-libro").reset();
                }
            })
            .catch(error => {
                alert("Error: " + error);
            });
        });

        // Manejar el cierre del modal de edición
        const closeButton = document.getElementById("close-edit-modal");
        closeButton.addEventListener("click", function() {
            modal.style.display = "none";
        });
    }

    // Función para eliminar un libro
    function eliminarLibro(id) {
        if (confirm("¿Estás seguro de que quieres eliminar este libro?")) {
            fetch(`/api/inventario/eliminar_libro/${id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    alert("Libro eliminado exitosamente.");
                    // Actualiza la tabla de inventario
                    actualizarInventario();
                }
            })
            .catch(error => {
                alert("Error: " + error);
            });
        }
    }

    // Inicializa la tabla de inventario
    actualizarInventario();

    // Función para filtrar libros por título
    searchInput.addEventListener("input", function() {
        const searchTerm = searchInput.value.toLowerCase();
        const rows = document.querySelectorAll("#inventory-table-body tr");

        rows.forEach(row => {
            const title = row.querySelector("td:nth-child(2)").textContent.toLowerCase();
            if (title.includes(searchTerm)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
});
