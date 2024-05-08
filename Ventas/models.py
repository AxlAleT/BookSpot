from django.db import models

class Libro(models.Model):
    ID = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    Cantidad = models.DecimalField(max_digits=5, decimal_places=0)
    Precio = models.DecimalField(max_digits=5, decimal_places=2)
    Titulo = models.CharField(max_length=100)
    Autor  = models.CharField(max_length=100)
    Editorial = models.CharField(max_length=100)

    class Lib:
        db_table = "Libro"
