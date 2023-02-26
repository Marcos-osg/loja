from django.db import models

# Create your models here.

class Products(models.Model):
    marca = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_promo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)