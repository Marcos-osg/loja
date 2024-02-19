from typing import List
from ninja import NinjaAPI
from uuid import uuid4

from backend.loja.schemas import PedidoSchema, CarrinhoSchema, ItensCarrinhoSchema, ProdutoSchema, Error, CarrinhoPayload
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
    
def get_cart():
    carrinho, _ = Carrinho.objects.get_or_create(pk="daeb9760-4d21-1234-bd1e-c3997e81731e", finalizado=False)
    return carrinho
    

@api.post("/adiciona-item-carrinho", response={200:dict, 404:Error, 500:Error})
def adiciona_item_carrinho(request, payload:CarrinhoPayload):
    carrinho = get_cart()
    try:
        itens_carrinho = ItensCarrinho()
        produto = Produtos.objects.get(pk=payload.id_produto)
        
        """ verifica se o produto já existe no carrinho se existente altera a quantidade, caso contrario adiciona """
        item = ItensCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()

        if item:
            item.quantidade += payload.quantidade
            item.save()
            return ({"sucesso":f"O produto {produto._name_product()} foi adicionado ao carrinho"})
        else:
            itens_carrinho.carrinho = carrinho
            itens_carrinho.produto = produto
            itens_carrinho.quantidade = payload.quantidade
            itens_carrinho.save()
            return ({"sucesso":f"O produto {produto._name_product()} foi adicionado ao carrinho"})
        
    except Exception as e:
        print(e)
        return 500, ({"message": str(e)})
    except Produtos.DoesNotExist:
        print("produto não encontrado")
        return 404, ({"message": "Produto não encontrado"})

@api.post("/remove-item-carrinho")
def remove_item_carrinho(request):
    ...