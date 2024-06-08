document.addEventListener('DOMContentLoaded', () => {
    const productTableBody = document.getElementById('product-table-body');
    const completeSaleButton = document.getElementById('complete-sale');
    const productCodeInput = document.getElementById('product-code');

    // Placeholder for product data (to be fetched from API or database in future)
    let products = [];

    // Function to render products in the table
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
    }

    // Function to fetch product data from the API
    async function fetchProductData(id_libro, cantidad) {
        try {
            const response = await fetch('http://127.0.0.1:5000/ventas/get_libro/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ items: [{ id_libro, cantidad }] })
            });
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching product data:', error);
        }
    }
    

    // Event listener for product code input (simulating a product scan)
    productCodeInput.addEventListener('keypress', async (event) => {
        if (event.key === 'Enter') {
            const id_libro = parseInt(productCodeInput.value);
            const cantidad = 1; // Default quantity for a new product

            const productData = await fetchProductData(id_libro, cantidad);
            if (productData) {
                products.push({ ...productData, cantidad });
                renderProducts();
                productCodeInput.value = ''; // Clear the input
            } else {
                alert('Producto no encontrado o no hay suficiente stock');
            }
        }
    });

    // Event listener for delete buttons
    productTableBody.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-button')) {
            const index = event.target.getAttribute('data-index');
            products.splice(index, 1);
            renderProducts();
        }
    });

    // Event listener for quantity inputs
    productTableBody.addEventListener('input', (event) => {
        if (event.target.classList.contains('quantity-input')) {
            const index = event.target.getAttribute('data-index');
            const newQuantity = parseInt(event.target.value);
            if (newQuantity > 0) {
                products[index].cantidad = newQuantity;
            }
        }
    });

    // Event listener for complete sale button
    completeSaleButton.addEventListener('click', () => {
        alert('Venta completada!');
        products.length = 0;  // Clear products
        renderProducts();  // Re-render the table
    });

    // Initial rendering of products
    renderProducts();
});
