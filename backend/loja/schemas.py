from ninja import Schema

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
    estoque: str
    

class ProdutoInfoSchema(Schema):
    """ Schema de info para o produto do carrinho """
    tipo: str
    cor: str
    tamanho: str
    marca: str


class CarrinhoSchema(Schema):
    """ Schema de carrinho """
    pedido: str
    valor_final: float
    finalizado: bool
    
    
class ItensCarrinhoSchema(Schema):
    """ Schema de itens do carrinho """
    produto: ProdutoInfoSchema
    quantidade: int
    valor_unitario: float
    valor_total_produto: float


class PedidoSchema(Schema):
    """ Schema de pedidos """
    carrinho_pedido: str
    total_pedido: float
    cod_pagamento: str
    status_pagamento: str