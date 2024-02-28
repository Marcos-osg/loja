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
        db_table = f'{__package__.split(".")[-1]}"."'

    def __str__(self):
        return f"{self.id}, {self.created_at}"

class Produtos(Header):
    """ Generico para roupas """
    tipo = models.CharField(max_length=64, choices=choices.tipo)
    cor = models.CharField(max_length=64, choices=choices.lista_de_cores)
    tamanho = models.CharField(max_length=64, choices=choices.tamanhos_camisetas)
    marca = models.CharField(max_length=64, choices=choices.marcas)
    preco = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    preco_promo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque = models.PositiveIntegerField(default=0)
    # imagem = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        db_table = Header._meta.db_table + verbose_name.lower()
        
    def _get_price_product(self):
        """ Retorna o preço do produto sendo ele promocional ou não """
        if self.preco_promo:
            return self.preco_promo
        else:
            return self.preco
    
    def _name_product(self):
        return f"{self.tipo} {self.marca} {self.tamanho} {self.cor}"

    def __str__(self):
        return f"{self.tipo} {self.marca} - {self.tamanho} - {self.cor} -- R${self._get_price_product()}"
    

class Carrinho(Header):
    pedido = models.CharField(max_length=50, null=True, blank=True)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    finalizado = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        return super(Carrinho, self).save(*args, **kwargs)
    
    def _get_total_cart(self):
        valor_final = 0
        itens_carrinho = ItensCarrinho.objects.filter(carrinho=self)
        for item in itens_carrinho:
            valor_final += item.valor_total_produto
        
        """ salva o valor final no carrinho """
        self.valor_final = valor_final
        self.save()
        
        """ retorna o valor final para uso no front """
        return valor_final

    class Meta:
        verbose_name = "Carrinho de compra"
        verbose_name_plural = "Carrinhos de compras"
        db_table = Header._meta.db_table + verbose_name.lower()
        

    def __str__(self):
        return f"{self.pedido} - Finalizado: {'Sim' if self.finalizado == True else 'Não'} x {self.valor_final}"


class ItensCarrinho(Header):
    produto = models.ForeignKey(Produtos, on_delete=models.DO_NOTHING)
    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total_produto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.DO_NOTHING)
    
    def save(self, *args, **kwargs):
        valor_unitario = self.produto._get_price_product()
        self.valor_unitario = valor_unitario
        self.valor_total_produto = self.quantidade * valor_unitario
        return super(ItensCarrinho, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
        db_table = Header._meta.db_table + verbose_name.lower()
        

    def __str__(self):
        return f"{self.produto} x {self.quantidade} - R$ {self.valor_total_produto}"


class Pedido(Header):
    carrinho_pedido = models.CharField(max_length=50)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cod_pagamento = models.CharField(max_length=50, null=True, blank=True)
    status_pagamento = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.carrinho_pedido} R$ {self.total_pedido}"
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = Header._meta.db_table + verbose_name.lower()
        
