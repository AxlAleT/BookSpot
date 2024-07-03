document.addEventListener("DOMContentLoaded", function() {
    const menuItems = document.querySelectorAll(".menu li");
    const sections = document.querySelectorAll(".section");
    const selectionButtons = document.querySelectorAll(".selection-button");
    const views = document.querySelectorAll(".view");
    const searchInput = document.getElementById("search-input");

    menuItems.forEach(item => {
        item.addEventListener("click", function() {
            sections.forEach(section => {
                section.classList.remove("active");
            });
            const sectionId = this.getAttribute("data-section");
            const sectionToShow = document.getElementById(sectionId);
            if (sectionToShow) {
                sectionToShow.classList.add("active");
            }
        });
    });

    selectionButtons.forEach(button => {
        button.addEventListener("click", function() {
            selectionButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");
            views.forEach(view => view.classList.remove("active"));
            const viewId = this.getAttribute("data-view");
            const viewToShow = document.getElementById(viewId);
            if (viewToShow) {
                viewToShow.classList.add("active");
            }
        });
    });

    window.mostrarFormularioAgregar = function() {
        document.getElementById("add-book-form").style.display = "block";
    }

    document.getElementById("form-agregar-libro").addEventListener("submit", function(event) {
        event.preventDefault();
        const titulo = document.getElementById("titulo").value;
        const precio = document.getElementById("precio").value;
        const cantidad = document.getElementById("cantidad").value;

        fetch('http://127.0.0.1:5000/inventario/agregar_libro/', {
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
                alert(data.message);
                actualizarInventario();
                document.getElementById("add-book-form").style.display = "none";
                document.getElementById("form-agregar-libro").reset();
            }
        })
        .catch(error => {
            alert("Error: " + error);
        });
    });

    function actualizarInventario() {
        fetch("http://127.0.0.1:5000/inventario/obtener_libros/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error al obtener libros: " + data.error);
                return;
            }
            const tableBody = document.getElementById("inventory-table-body");
            tableBody.innerHTML = "";

            data.forEach(libro => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${libro.id}</td>
                    <td>${libro.título}</td>
                    <td>${libro.precio}</td>
                    <td>${libro.available_quantity}</td>
                    <td>
                        <button class="btn edit" data-id="${libro.id}">Editar</button>
                        <button class="btn delete" data-id="${libro.id}">Eliminar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            agregarEventosBotones();
        })
        .catch(error => {
            console.error("Error al obtener el inventario:", error);
        });
    }

    function agregarEventosBotones() {
        const editButtons = document.querySelectorAll(".btn.edit");
        const deleteButtons = document.querySelectorAll(".btn.delete");

        editButtons.forEach(button => {
            button.addEventListener("click", function() {
                const libroId = this.getAttribute("data-id");
                fetch(`/obtener_libros/?numero=${libroId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert("Error al obtener detalles del libro: " + data.error);
                        return;
                    }
                    abrirFormularioEditar(data.libro);
                })
                .catch(error => {
                    alert("Error: " + error);
                });
            });
        });

        deleteButtons.forEach(button => {
            button.addEventListener("click", function() {
                const libroId = this.getAttribute("data-id");
                eliminarLibro(libroId);
            });
        });
    }

    function abrirFormularioEditar(libro) {
        const modal = document.getElementById("edit-book-modal");
        modal.style.display = "block";

        document.getElementById("edit-id").value = libro.id;
        document.getElementById("edit-título").value = libro.título;
        document.getElementById("edit-precio").value = libro.precio;
        document.getElementById("edit-available_quantity").value = libro.available_quantity;

        document.getElementById("form-editar-libro").addEventListener("submit", function(event) {
            event.preventDefault();

            const id = document.getElementById("edit-id").value;
            const título = document.getElementById("edit-título").value;
            const precio = document.getElementById("edit-precio").value;
            const available_quantity = document.getElementById("edit-available_quantity").value;

            fetch(`http://127.0.0.1:5000/inventario/editar_libro/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ id, título, precio, available_quantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    alert(data.message);
                    actualizarInventario();
                    modal.style.display = "none";
                    document.getElementById("form-editar-libro").reset();
                }
            })
            .catch(error => {
                alert("Error: " + error);
            });
        });

        const closeButton = document.getElementById("close-edit-modal");
        closeButton.addEventListener("click", function() {
            modal.style.display = "none";
        });
    }

    function eliminarLibro(id) {
        if (confirm("¿Estás seguro de que quieres eliminar este libro?")) {
            fetch(`http://127.0.0.1:5000/inventario/eliminar_libro/${id}`, {
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
                    actualizarInventario();
                }
            })
            .catch(error => {
                alert("Error: " + error);
            });
        }
    }

    searchInput.addEventListener("input", function() {
        const searchTerm = searchInput.value.toLowerCase();
        fetch(`http://127.0.0.1:5000/inventario/buscar_libro/?keyword=${searchTerm}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error al buscar libros: " + data.error);
                return;
            }
            const tableBody = document.getElementById("inventory-table-body");
            tableBody.innerHTML = "";
            data.forEach(libro => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${libro.id}</td>
                    <td>${libro.título}</td>
                    <td>${libro.precio}</td>
                    <td>${libro.available_quantity}</td>
                    <td>
                        <button class="btn edit" data-id="${libro.id}">Editar</button>
                        <button class="btn delete" data-id="${libro.id}">Eliminar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error en la búsqueda de libros:", error);
        });
    });
});
