document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('Select-Ventas').addEventListener('click', function() {
        window.location.href = 'http://127.0.0.1:5000/vendedor/ventas.html';
      });
      
    document.getElementById('Select-Apartado').addEventListener('click', function() {
        window.location.href = 'http://127.0.0.1:5000/vendedor/apartados.html';
    });

    const productTableBody = document.getElementById('product-table-body');
    const completeSaleButton = document.getElementById('complete-sale');
    const productCodeInput = document.getElementById('product-code');
    const paymentMethodSelect = document.getElementById('payment-method');

    let products = [];

    const quantityInputs = document.querySelectorAll('.quantity-input');

    quantityInputs.forEach(input => {
        input.addEventListener('input', calcularMonto);
    });
    

    function calcularMonto() {
        const montoInput = document.getElementById('monto');

                // 1. Obtener todos los inputs de cantidad
        const quantityInputs = document.querySelectorAll('.quantity-input');

        // Función para calcular y actualizar el total
        function updateTotal() {
        let total = 0;
        // 3. Calcular el total
        quantityInputs.forEach(input => {
            const row = input.closest('tr'); // Encuentra la fila del input
            const price = parseFloat(row.cells[2].textContent); // Obtiene el precio de la fila
            const quantity = parseInt(input.value); // Obtiene la cantidad del input
            total += price * quantity; // Suma al total
        });

        // 4. Actualizar el valor del input montoInput
        montoInput.value = total.toFixed(2); // Asegura dos decimales en el total
        }

        // 2. Añadir un evento 'change' a cada input de cantidad
        quantityInputs.forEach(input => {
        input.addEventListener('change', updateTotal);
        });

        // Llama a updateTotal inicialmente para establecer el total inicial
        updateTotal();
    }
    
    function renderProducts() {
        productTableBody.innerHTML = '';
        products.forEach((product, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${product.titulo}</td>
                <td>${product.id_libro}</td>
                <td>${product.precio.toFixed(2)}</td>
                <td><input type="number" value="${product.cantidad}" min="1" class="form-control quantity-input" data-index="${index}"></td>
                <td>
                    <button class="btn btn-danger btn-sm delete-button" data-index="${index}">Eliminar</button>
                </td>
            `;
            productTableBody.appendChild(row);
        });
        calcularMonto(); // Llamar a calcularMonto al final de renderizar los productos
    }

    async function fetchProductData(id_libro, cantidad) {
        try {
            const response = await fetch('http://127.0.0.1:5000/ventas/get_libro/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ items: [{ id_libro, cantidad }], metodo_pago: paymentMethodSelect.value})
            });
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Error: ${response.status} ${response.statusText}. ${errorText}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching product data:', error);
            throw error;
        }
    }

    productCodeInput.addEventListener('keypress', async (event) => {
        if (event.key === 'Enter') {
            const id_libro = parseInt(productCodeInput.value);
            const cantidad = 1; // Default quantity for a new product

            try {
                const productData = await fetchProductData(id_libro, cantidad);
                if (productData) {
                    products.push({ ...productData, cantidad });
                    renderProducts();
                    productCodeInput.value = ''; // Clear the input
                } else {
                    alert('Producto no encontrado o no hay suficiente stock');
                }
            } catch (error) {
                alert(`Error al obtener datos del producto: ${error.message}`);
            }
        }
    });

    productTableBody.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-button')) {
            const index = event.target.getAttribute('data-index');
            products.splice(index, 1);
            renderProducts();
        }
    });

    productTableBody.addEventListener('input', async (event) => {
        if (event.target.classList.contains('quantity-input')) {
            const index = parseInt(event.target.getAttribute('data-index'));
            const newQuantity = parseInt(event.target.value);
            const id_libro = products[index].id_libro;

            if (newQuantity > 0) {
                try {
                    await fetchProductData(id_libro, newQuantity);
                    products[index].cantidad = newQuantity;
                } catch (error) {
                    console.error('Error fetching product data:', error);
                    alert(`Error al actualizar la cantidad: ${error.message}`);
                    event.target.value = products[index].cantidad;
                }
            } else {
                event.target.value = products[index].cantidad;
            }
        }
    });

    completeSaleButton.addEventListener('click', async () => {
        try {
            const items = products.map(product => ({
                id_libro: product.id_libro,
                cantidad: product.cantidad
            }));
            const metodo_pago = paymentMethodSelect.value;

            const response = await fetch('http://127.0.0.1:5000/ventas/completar/', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ items, metodo_pago })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Error: ${response.status} ${response.statusText}. ${errorText}`);
            }

            products.length = 0;
            renderProducts();
            alert('Venta completada exitosamente!');
        } catch (error) {
            console.error('Error al completar la venta:', error);
            alert(`Error al completar la venta: ${error.message}`);
        }
    });

    renderProducts();
});
