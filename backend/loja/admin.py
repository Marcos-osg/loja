from django.contrib import admin
from backend.loja.models import Header, Produtos, Carrinho, ItensCarrinho, Pedido

excluded_fields = [ field.name for field in Header._meta.fields]

@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    fields = [field.name for field in Produtos._meta.fields if field.name not in excluded_fields]

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    fields = [field.name for field in Carrinho._meta.fields if field.name not in excluded_fields]


@admin.register(ItensCarrinho)
class ItensCarrinhoAdmin(admin.ModelAdmin):
    fields = [field.name for field in ItensCarrinho._meta.fields if field.name not in excluded_fields]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    fields = [field.name for field in Pedido._meta.fields if field.name not in excluded_fields]
