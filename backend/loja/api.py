from typing import List
from ninja import NinjaAPI

from backend.loja.schemas import ProdutosSchema, ItemCarrinhoIn
from backend.loja.models import Produtos, ItensCarrinho, Carrinho

api = NinjaAPI(title="API Loja Virtual")

@api.get("/todos_produtos", response=List[ProdutosSchema])
def produtos(request):
    produtos = Produtos.objects.all()
    return produtos

@api.post("/adiciona_carrinho")
def adiciona_item_carrinho(request, payload: ItemCarrinhoIn):
    _produto = Produtos.objects.get(id=payload.produto)
    payload.produto = _produto
    ItensCarrinho.objects.create(**payload.dict())
    return {"sucesso":"Produto adicionado"}
