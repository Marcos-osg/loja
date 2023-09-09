from django.db import models
from abc import ABCMeta
from backend.loja import choices

import uuid

class Header(models.Model):
    __metaclass__ = ABCMeta

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}, {self.created_at}"

class Camisetas(Header):
    cor = models.CharField(max_length=64, choices=choices.lista_de_cores)
    tamanho = models.CharField(max_length=64, choices=choices.tamanhos_camisetas)
    marca = models.CharField(max_length=64, choices=choices.marcas)
    preco = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    preco_promo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Camiseta"
        verbose_name_plural = "Camisetas"

    def __str__(self):
        return f"{self.marca} - {self.tamanho} - {self.cor} -- R${self.preco}"
    
