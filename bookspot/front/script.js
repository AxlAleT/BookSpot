// Función para agregar un producto al inventario
function agregarProducto() {
    var nombre = prompt("Ingrese el nombre del producto:");
    var cantidad = parseInt(prompt("Ingrese la cantidad del producto:"));
    var precio = parseFloat(prompt("Ingrese el precio del producto:"));

    if (nombre && cantidad && precio) {
        // Crear una nueva fila en la tabla con los datos del producto
        var tabla = document.getElementById("tablaInventario").getElementsByTagName("tbody")[0];
        var fila = tabla.insertRow();

        var celdaNombre = fila.insertCell(0);
        var celdaCantidad = fila.insertCell(1);
        var celdaPrecio = fila.insertCell(2);

        celdaNombre.textContent = nombre;
        celdaCantidad.textContent = cantidad;
        celdaPrecio.textContent = "$" + precio.toFixed(2);
    } else {
        alert("Por favor, complete todos los campos correctamente.");
    }
}
