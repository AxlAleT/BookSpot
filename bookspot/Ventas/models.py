from django.db import models

# Create your models here.
class Libro(models.Model):
    id_libro = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    Cantidad = models.DecimalField(max_digits=5, decimal_places=0)
    Precio = models.DecimalField(max_digits=5, decimal_places=2)
    Titulo = models.CharField(max_length=100)
    Autor  = models.CharField(max_length=100)
    Editorial = models.CharField(max_length=100)

    class Lib:
        db_table = "Libro"

class Venta(models.Model):
    id_venta = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    monto = models.DecimalField(max_digits=5, decimal_places=0)
    fecha_venta = models.DateField()

    class Ven:
        db_table = "Venta"


class detalle_venta(models.Model):
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=5,decimal_places=0)
    precio_venta = models.DecimalField(max_digits=5, decimal_places=2)

    class det:
        db_table = "Detalle-Venta"

class Metodo_pago(models.Model):
    id_metodo_pago = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=150)

