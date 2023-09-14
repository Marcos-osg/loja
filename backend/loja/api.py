from typing import List
from ninja import NinjaAPI
from uuid import uuid4

from backend.loja.schemas import ProdutosSchema, ItemCarrinhoIn, ItemCarrinhoOut
from backend.loja.models import Produtos, ItensCarrinho, Carrinho
from backend.loja import utils


api = NinjaAPI(title="API Loja Virtual")

@api.get("/todos-os-produtos", response=List[ProdutosSchema])
def produtos(request):        
    produtos = Produtos.objects.all()
    return produtos

@api.post("/adiciona-item-carrinho")
def adiciona_item_carrinho(request, payload: ItemCarrinhoIn):
    data = {}
    try:
        session = request.session["cart"]
    except:
        session = uuid4()
        request.session["cart"] = str(session)
    
    _produto = Produtos.objects.get(id=payload.produto)

    try:
        carrinho = Carrinho.objects.filter(pedido=session).first()
        if not carrinho:
            carrinho = Carrinho(
                pedido=session
            ).save()
        
        item = ItensCarrinho(produto=_produto, quantidade=payload.quantidade, carrinho=carrinho)
        item.save()
        carrinho.valor_final = carrinho.valor_final + item.valor_produtos
        carrinho.save()
        data["sucesso"] = "Produto adicionado ao carrinho"
    except Exception as e:
        data["erro"] = "Ocorreu um erro ao adicionar o produto ao carrinho"

    return data

@api.post("/remove-item-carrinho")
def remove_item_carrinho(request, payload: ItemCarrinhoOut):
    data = {}
    try:
        session = request.session["cart"]
    except:
        session = uuid4()
        request.session["cart"] = str(session)
    
    produto = Produtos.objects.get(id=payload.produto)

    try:
        carrinho = Carrinho.objects.filter(pedido=session).first()
        if not carrinho:
            carrinho = Carrinho(
                pedido=session
            ).save()
        item = ItensCarrinho.objects.get(carrinho=carrinho)
        item.quantidade = item.quantidade - payload.quantidade
        item.save()
        carrinho.valor_final = carrinho.valor_final - (produto.preco * payload.quantidade)
        carrinho.save()
        data["sucesso"] = "Produto removido do carrinho"
    except Exception as e:
        data["erro"] = "Ocorreu um erro ao remover o produto do carrinho"

    return data
