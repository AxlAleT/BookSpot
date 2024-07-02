document.addEventListener("DOMContentLoaded", function() {
    const sections = {
        crear: document.getElementById("section-crear"),
        concretar: document.getElementById("section-concretar"),
        cancelar: document.getElementById("section-cancelar"),
        modificar: document.getElementById("section-modificar")
    };

    document.getElementById("btn-crear").addEventListener("click", function() {
        mostrarSeccion("crear");
    });
    document.getElementById("btn-concretar").addEventListener("click", function() {
        mostrarSeccion("concretar");
    });
    document.getElementById("btn-cancelar").addEventListener("click", function() {
        mostrarSeccion("cancelar");
    });
    document.getElementById("btn-modificar").addEventListener("click", function() {
        mostrarSeccion("modificar");
    });

    function mostrarSeccion(seccion) {
        for (let key in sections) {
            if (key === seccion) {
                sections[key].style.display = "block";
            } else {
                sections[key].style.display = "none";
            }
        }
    }

    // Mostrar la primera sección por defecto
    mostrarSeccion("crear");

    const formCrearApartado = document.getElementById("form-crear-apartado");
    const formConcretarVenta = document.getElementById("form-concretar-venta");
    const formCancelarApartado = document.getElementById("form-cancelar-apartado");
    const formModificarApartado = document.getElementById("form-modificar-apartado");

    formCrearApartado.addEventListener("submit", function(event) {
        event.preventDefault();
        const data = {
            id_usuario: document.getElementById("id_usuario").value,
            fecha_limite: document.getElementById("fecha_limite").value,
            monto: document.getElementById("monto").value,
            nombre_acreedor: document.getElementById("nombre_acreedor").value,
            items: document.getElementById("items").value.split("\n").map(item => {
                const [id_libro, cantidad, precio_apartado] = item.split(",");
                return { id_libro: parseInt(id_libro), cantidad: parseInt(cantidad), precio_apartado: parseFloat(precio_apartado) };
            })
        };

        fetch("/crear_apartado/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("Apartado creado exitosamente.");
                formCrearApartado.reset();
            }
        })
        .catch(error => alert("Error: " + error));
    });

    formConcretarVenta.addEventListener("submit", function(event) {
        event.preventDefault();
        const data = { id_apartado: document.getElementById("id_apartado").value };

        fetch("/concretar_venta_apartado/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("Venta concretada exitosamente.");
                formConcretarVenta.reset();
            }
        })
        .catch(error => alert("Error: " + error));
    });

    formCancelarApartado.addEventListener("submit", function(event) {
        event.preventDefault();
        const data = { id_apartado: document.getElementById("id_apartado_cancelar").value };

        fetch("/cancelar_apartado/", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("Apartado cancelado exitosamente.");
                formCancelarApartado.reset();
            }
        })
        .catch(error => alert("Error: " + error));
    });

    formModificarApartado.addEventListener("submit", function(event) {
        event.preventDefault();
        const data = {
            id_apartado: document.getElementById("id_apartado_modificar").value,
            id_usuario: document.getElementById("id_usuario_modificar").value,
            fecha_limite: document.getElementById("fecha_limite_modificar").value,
            monto: document.getElementById("monto_modificar").value,
            nombre_acreedor: document.getElementById("nombre_acreedor_modificar").value,
            detalles: document.getElementById("detalles").value.split("\n").map(item => {
                const [id_libro, cantidad, precio_apartado] = item.split(",");
                return { id_libro: parseInt(id_libro), cantidad: parseInt(cantidad), precio_apartado: parseFloat(precio_apartado) };
            })
        };

        fetch("/modificar_apartado/", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("Apartado modificado exitosamente.");
                formModificarApartado.reset();
            }
        })
        .catch(error => alert("Error: " + error));
    });
});
