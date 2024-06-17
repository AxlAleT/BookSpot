document.addEventListener("DOMContentLoaded", function() {
    const menuItems = document.querySelectorAll(".menu li");
    const sections = document.querySelectorAll(".section");

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
                        <button class="btn edit">Editar</button>
                        <button class="btn delete">Eliminar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Añadir eventos de edición y eliminación a los botones
            const editButtons = document.querySelectorAll(".btn.edit");
            const deleteButtons = document.querySelectorAll(".btn.delete");

            editButtons.forEach((button, index) => {
                button.addEventListener("click", function() {
                    editarLibro(data[index]);
                });
            });

            deleteButtons.forEach((button, index) => {
                button.addEventListener("click", function() {
                    eliminarLibro(data[index].id);
                });
            });
        })
        .catch(error => {
            console.error("Error al obtener el inventario:", error);
        });
    }

    // Función para editar un libro
    function editarLibro(libro) {
        const titulo = prompt("Nuevo título:", libro.titulo);
        const precio = prompt("Nuevo precio:", libro.precio);
        const cantidad = prompt("Nueva cantidad:", libro.available_quantity);

        if (titulo && precio && cantidad) {
            fetch("/api/inventario/editar_libro/", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ id: libro.id, titulo, precio, available_quantity: cantidad })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    alert("Libro editado exitosamente.");
                    // Actualiza la tabla de inventario
                    actualizarInventario();
                }
            })
            .catch(error => {
                alert("Error: " + error);
            });
        }
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
});
