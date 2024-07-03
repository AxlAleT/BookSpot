document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('boton-crear-apartado').addEventListener('click', function() {
        // Suponiendo que los valores de fecha_limite, monto y nombre_acreedor se recogen de inputs
        const fecha_limite = document.getElementById('fecha_limite').value;
        const monto = parseFloat(document.getElementById('monto').value);
        const nombre_acreedor = document.getElementById('nombre_acreedor').value;
      
        const productTableBody = document.getElementById('product-table-body');
        const rows = productTableBody.querySelectorAll('tr');
        const items = [];
      
        rows.forEach(row => {
          const id_libro = parseInt(row.cells[1].textContent, 10);
          const cantidad = parseInt(row.querySelector('.quantity-input').value, 10);
          const precio_apartado = parseFloat(row.cells[2].textContent);
      
          items.push({
            id_libro,
            cantidad,
            precio_apartado
          });
        });
      
        const apartadoData = {
          fecha_limite,
          monto,
          nombre_acreedor,
          items
        };
      
        crearApartado(apartadoData);

      });
});

async function crearApartado(apartadoData) {
  // Validar los datos del apartado con el esquema definido
  const esquemaApartado = {
    fecha_limite: new Date(apartadoData.fecha_limite), // Asegurarse de que es una fecha válida
    monto: parseFloat(apartadoData.monto), // Convertir a float para validar el monto
    nombre_acreedor: apartadoData.nombre_acreedor,
    items: apartadoData.items.map(item => ({
      id_libro: parseInt(item.id_libro), // Convertir a entero el ID del libro
      cantidad: parseInt(item.cantidad), // Convertir a entero la cantidad
      precio_apartado: parseFloat(item.precio_apartado) // Convertir a float el precio
    }))
  };

  // Verificar si todos los campos requeridos están presentes y son válidos
  // Esta es una simplificación. En un caso real, se debería usar una librería como Joi o Yup para validar esquemas
  if (!esquemaApartado.fecha_limite || isNaN(esquemaApartado.monto) || !esquemaApartado.nombre_acreedor || !Array.isArray(esquemaApartado.items) || esquemaApartado.items.some(item => isNaN(item.id_libro) || isNaN(item.cantidad) || isNaN(item.precio_apartado))) {
    console.error('Los datos del apartado son inválidos');
    return;
  }

  try {
    // Enviar la solicitud al servidor
    const response = await fetch('/ruta/a/crear_apartado', { // Reemplazar '/ruta/a/crear_apartado' con la ruta real del servidor
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(esquemaApartado),
    });

    if (!response.ok) {
      throw new Error(`Error en la solicitud: ${response.statusText}`);
    }

    const responseData = await response.json();
    console.log('Apartado creado con éxito:', responseData);
  } catch (error) {
    console.error('Error al crear el apartado:', error);
  }
}


// document.addEventListener('DOMContentLoaded', () => {
//     const formSections = document.querySelectorAll('.form-section');
//     const buttons = {
//         'btn-crear': 'section-crear',
//         'btn-concretar': 'section-concretar',
//         'btn-cancelar': 'section-cancelar',
//         'btn-modificar': 'section-modificar'
//     };

//     Object.keys(buttons).forEach(buttonId => {
//         document.getElementById(buttonId).addEventListener('click', () => {
//             formSections.forEach(section => section.style.display = 'none');
//             document.getElementById(buttons[buttonId]).style.display = 'block';
//         });
//     });

//     document.getElementById('form-crear-apartado').addEventListener('submit', async (event) => {
//         event.preventDefault();

//         const data = {
//             fecha_limite: document.getElementById('fecha_limite').value,
//             monto: parseFloat(document.getElementById('monto').value),
//             nombre_acreedor: document.getElementById('nombre_acreedor').value,
//             items: document.getElementById('items').value.split('\n').map(item => {
//                 const [id_libro, cantidad, precio] = item.split(',');
//                 return { id_libro: parseInt(id_libro), cantidad: parseInt(cantidad), precio_apartado: parseFloat(precio) };
//             })
//         };

//         try {
//             const response = await fetch('/crear_apartado/', {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify(data)
//             });
//             const result = await response.json();
//             if (response.ok) {
//                 alert('Apartado creado exitosamente.');
//             } else {
//                 alert(`Error: ${result.error}`);
//             }
//         } catch (error) {
//             console.error('Error:', error);
//         }
//     });

//     document.getElementById('form-concretar-venta').addEventListener('submit', async (event) => {
//         event.preventDefault();

//         const data = {
//             id_apartado: parseInt(document.getElementById('id_apartado').value)
//         };

//         try {
//             const response = await fetch('/concretar_venta_apartado/', {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify(data)
//             });
//             const result = await response.json();
//             if (response.ok) {
//                 alert('Venta concretada exitosamente.');
//             } else {
//                 alert(`Error: ${result.error}`);
//             }
//         } catch (error) {
//             console.error('Error:', error);
//         }
//     });

//     document.getElementById('form-cancelar-apartado').addEventListener('submit', async (event) => {
//         event.preventDefault();

//         const data = {
//             id_apartado: parseInt(document.getElementById('id_apartado_cancelar').value)
//         };

//         try {
//             const response = await fetch('/cancelar_apartado/', {
//                 method: 'DELETE',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify(data)
//             });
//             const result = await response.json();
//             if (response.ok) {
//                 alert('Apartado cancelado exitosamente.');
//             } else {
//                 alert(`Error: ${result.error}`);
//             }
//         } catch (error) {
//             console.error('Error:', error);
//         }
//     });

//     document.getElementById('form-modificar-apartado').addEventListener('submit', async (event) => {
//         event.preventDefault();

//         const data = {
//             id_apartado: parseInt(document.getElementById('id_apartado_modificar').value),
//             fecha_limite: document.getElementById('fecha_limite_modificar').value,
//             monto: parseFloat(document.getElementById('monto_modificar').value),
//             nombre_acreedor: document.getElementById('nombre_acreedor_modificar').value,
//             detalles: document.getElementById('detalles').value.split('\n').map(item => {
//                 const [id_libro, cantidad, precio] = item.split(',');
//                 return { id_libro: parseInt(id_libro), cantidad: parseInt(cantidad), precio_apartado: parseFloat(precio) };
//             })
//         };

//         try {
//             const response = await fetch('/modificar_apartado/', {
//                 method: 'PUT',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify(data)
//             });
//             const result = await response.json();
//             if (response.ok) {
//                 alert('Apartado modificado exitosamente.');
//             } else {
//                 alert(`Error: ${result.error}`);
//             }
//         } catch (error) {
//             console.error('Error:', error);
//         }
//     });

//     // Inicialmente mostrar solo el primer formulario
//     formSections.forEach(section => section.style.display = 'none');
//     document.getElementById('section-crear').style.display = 'block';
// });
