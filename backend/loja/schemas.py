from ninja import Schema
from typing import List

class Error(Schema):
    message: str

class ProdutoSchema(Schema):
    """ Schema de produto """
    tipo: str
    cor: str
    tamanho: str
    marca: str
    preco: float
    preco_promo: float
    estoque: int
    

class ProdutoInfoSchema(Schema):
    """ Schema de info para o produto do carrinho """
    tipo: str
    cor: str
    tamanho: str
    marca: str




class CarrinhoPayload(Schema):
    """ Schema para adicionar/excluir item via POST """
    id_produto: str
    quantidade: int
    
class ItensCarrinhoSchema(Schema):
    """ Schema de itens do carrinho """
    produto: ProdutoInfoSchema
    quantidade: int
    valor_unitario: float
    valor_total_produto: float

class CarrinhoSchema(Schema):
    """ Schema de carrinho """
    itens: List[ItensCarrinhoSchema]
    valor_total: float

class PedidoSchema(Schema):
    """ Schema de pedidos """
    carrinho_pedido: str
    total_pedido: float
    cod_pagamento: str
    status_pagamento: str