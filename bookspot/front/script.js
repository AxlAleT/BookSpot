document.addEventListener('DOMContentLoaded', () => {
    const productTableBody = document.getElementById('product-table-body');
    const completeSaleButton = document.getElementById('complete-sale');
    const productCodeInput = document.getElementById('product-code');

    // Placeholder for product data (to be fetched from API or database in future)
    const products = [
        { name: 'Libro 1', code: '001', price: 10.00, quantity: 1 },
        { name: 'Libro 2', code: '002', price: 15.50, quantity: 2 }
    ];

    // Function to render products in the table
    function renderProducts() {
        productTableBody.innerHTML = '';
        products.forEach((product, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${product.name}</td>
                <td>${product.code}</td>
                <td>${product.price.toFixed(2)}</td>
                <td><input type="number" value="${product.quantity}" min="1" class="form-control quantity-input" data-index="${index}"></td>
                <td>
                    <button class="btn btn-danger btn-sm delete-button" data-index="${index}">Eliminar</button>
                </td>
            `;
            productTableBody.appendChild(row);
        });
    }

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
                products[index].quantity = newQuantity;
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
