from typing import List
from ninja import NinjaAPI
from uuid import uuid4

from backend.loja.schemas import PedidoSchema, CarrinhoSchema, ItensCarrinhoSchema, ProdutoSchema, Error
from backend.loja.models import Produtos, ItensCarrinho, Carrinho



api = NinjaAPI(title="API Loja Virtual")

@api.get("/todos-os-produtos", response={200:List[ProdutoSchema], 404:Error, 500:Error})
def produtos(request):
    try:
        produtos = Produtos.objects.all().values()
        prod = [ProdutoSchema(**produto) for produto in produtos]

        return prod
    except Exception as e:
        return 500, ({"message": str(e)})

@api.post("/adiciona-item-carrinho")
def adiciona_item_carrinho(request):
    ...
    
@api.post("/remove-item-carrinho")
def remove_item_carrinho(request):
    ...