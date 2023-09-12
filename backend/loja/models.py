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

class Produtos(Header):
    tipo = models.CharField(max_length=64, choices=choices.tipo)
    cor = models.CharField(max_length=64, choices=choices.lista_de_cores)
    tamanho = models.CharField(max_length=64, choices=choices.tamanhos_camisetas)
    marca = models.CharField(max_length=64, choices=choices.marcas)
    preco = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    preco_promo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"{self.tipo} {self.marca} - {self.tamanho} - {self.cor} -- R${self.preco}"
    

class ItensCarrinho(Header):
    produto = models.ForeignKey(Produtos, on_delete=models.DO_NOTHING)
    quantidade = models.PositiveIntegerField()
    valor_produtos = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    
    def save(self, *args, **kwargs):
        self.valor_produtos = self.soma_produtos()
        return super(ItensCarrinho, self).save(*args, **kwargs)
    
    def soma_produtos(self):
        valor_produtos = self.produto.preco * self.quantidade
        return valor_produtos


    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"

    def __str__(self):
        return f"{self.produto} x {self.quantidade}"


class Carrinho(Header):
    item = models.ForeignKey(ItensCarrinho, on_delete=models.CASCADE, name="Itens")
    valor_final = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    pago = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"

    def __str__(self):
        return f"{self.produto} x {self.quantidade}"
