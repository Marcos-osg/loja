from django.db import models
from backend.loja.models import Pedido

# Create your models here.
class Pagamento(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100, null=True, blank=True)
    status_mp = models.CharField(max_length=100, null=True, blank=True)
    tipo_pagamento = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.pedido} {self.status} -- {self.status_mp}"
    
    
    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"