document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('payment-method').style.display = 'none';
  document.getElementById('payment-method-label').style.display = 'none';

    document.getElementById('completar-apartado').addEventListener('click', function() {
        const monto = parseFloat(document.getElementById('monto').value);
        const nombre_acreedor = document.getElementById('nombre-acreedor').value;
      
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
          monto,
          nombre_acreedor,
          items
        };
      
        crearApartado(apartadoData);

      });
});

async function crearApartado(apartadoData) {
  const esquemaApartado = {
    monto: parseFloat(apartadoData.monto),
    nombre_acreedor: apartadoData.nombre_acreedor,
    items: apartadoData.items.map(item => ({
      id_libro: parseInt(item.id_libro),
      cantidad: parseInt(item.cantidad),
      precio_apartado: parseFloat(item.precio_apartado)
    }))
  };

  if ( isNaN(esquemaApartado.monto) || !esquemaApartado.nombre_acreedor || !Array.isArray(esquemaApartado.items) || esquemaApartado.items.some(item => isNaN(item.id_libro) || isNaN(item.cantidad) || isNaN(item.precio_apartado))) {
    console.error('Los datos del apartado son inválidos');
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/apartados/crear_apartado/', {
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

    // Verificar si la respuesta incluye un id_apartado para confirmar el éxito
    if (responseData.id_apartado) {
      alert('Apartado creado con éxito');
    }
  } catch (error) {
    console.error('Error al crear el apartado:', error);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // Asignar controladores de eventos a cada botón
  document.getElementById('btn-crear').addEventListener('click', function() {
    mostrarSeccion('crear-apartado');
  });

  document.getElementById('btn-concretar').addEventListener('click', function() {
    mostrarSeccion('concretar-venta');
  });

  document.getElementById('btn-cancelar').addEventListener('click', function() {
    mostrarSeccion('cancelar-apartado');
  });

  document.getElementById('btn-modificar').addEventListener('click', function() {
    mostrarSeccion('modificar-apartado');
  });

  // Función para mostrar una sección y ocultar el resto
  function mostrarSeccion(idSeccion) {
    // Lista de todas las secciones
    const secciones = ['crear-apartado', 'concretar-venta', 'cancelar-apartado', 'modificar-apartado'];

    // Ocultar todas las secciones
    secciones.forEach(seccion => {
      document.getElementById(seccion).style.display = 'none';
    });

    // Mostrar la sección seleccionada
    document.getElementById(idSeccion).style.display = 'block';
  }
  
});

document.addEventListener('DOMContentLoaded', function() {
  // Asignar evento al botón de cancelar
  document.getElementById('btn-cancelar').addEventListener('click', function() {
      cancelarApartado();
  });

  // Función para cancelar el apartado
  async function cancelarApartado() {
      // Aquí debes obtener el ID del apartado que deseas cancelar
      const idApartado = prompt("Ingrese el ID del apartado que desea cancelar:");

      try {
          const response = await fetch(`http://127.0.0.1:5000/apartados/cancelar_apartado/${idApartado}`, {
              method: 'DELETE',  // Suponiendo que DELETE es el método adecuado para cancelar
              headers: {
                  'Content-Type': 'application/json',
              },
          });

          if (!response.ok) {
              throw new Error(`Error en la solicitud: ${response.statusText}`);
          }

          const responseData = await response.json();
          console.log('Apartado cancelado con éxito:', responseData);

          // Aquí puedes manejar cómo actualizar la interfaz después de cancelar
          alert('Apartado cancelado con éxito');
      } catch (error) {
          console.error('Error al cancelar el apartado:', error);
          alert('Error al cancelar el apartado. Consulte la consola para más detalles.');
      }
  }
});

