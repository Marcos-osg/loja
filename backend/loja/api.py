from typing import List
from ninja import NinjaAPI
import uuid

from backend.loja.schemas import PedidoSchema, CarrinhoSchema, ItensCarrinhoSchema, ProdutoSchema, Error, CarrinhoPayload, ProdutoInfoSchema
from backend.loja.models import Produtos, ItensCarrinho, Carrinho, Pedido



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

@api.post("/remove-item-carrinho", response={200:dict, 404:Error, 500:Error})
def remove_item_carrinho(request, payload:CarrinhoPayload):
    carrinho = get_cart()
    try:
        produto = Produtos.objects.get(pk=payload.id_produto)
        
        """ verifica se o produto já existe no carrinho se existente altera a quantidade, caso contrario exclui """
        item = ItensCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()

        if item:
            if item.quantidade <= 1 or item.quantidade <= payload.quantidade:
                item.delete()
                return ({"sucesso":f"O produto {produto._name_product()} foi removido do carrinho"})
            else:
                item.quantidade -= payload.quantidade
                item.save()
                return ({"sucesso":f"O produto {produto._name_product()} foi removido do carrinho"})

    except Exception as e:
        print(e)
        return 500, ({"message": str(e)})
    except Produtos.DoesNotExist:
        print("produto não encontrado")
        return 404, ({"message": "Produto não encontrado"})
        

@api.get("carrinho/", response={200:CarrinhoSchema, 404:Error, 500:Error})
def carrinho(request):
    try:
        carrinho = Carrinho.objects.get(pk="7360abc7-1bf5-41de-9c79-1048f8809271", finalizado=False)
        itens_carrinho = ItensCarrinho.objects.filter(carrinho=carrinho)
        
        lista_itens = []
        for item in itens_carrinho:
            itens = ItensCarrinhoSchema(
                produto = ProdutoInfoSchema(**item.produto.__dict__),
                quantidade = item.quantidade,
                valor_unitario = item.valor_unitario,
                valor_total_produto = item.valor_total_produto
            )
            lista_itens.append(itens)
        
        carrinho = CarrinhoSchema(
            itens=lista_itens,
            valor_total=carrinho._get_total_cart()
        )

        return 200, carrinho
    except Carrinho.DoesNotExist:
        return 404, ({"message": "Carrinho nao localizado"})
    except Exception as e:
        return 500, ({"message": str(e)})
    

@api.post("limpar-carrinho", response={200:dict, 404:Error, 500:Error})
def limpa_carrinho(request):
    try:
        carrinho = Carrinho.objects.get(pk="7360abc7-1bf5-41de-9c79-1048f8809271", finalizado=False)
        itens_carrinho = ItensCarrinho.objects.filter(carrinho=carrinho)
        for itens in itens_carrinho:
            itens.delete()
        return 200, ({"sucesso":"carrinho esvaziado"})
    except Carrinho.DoesNotExist:
        return 404, ({"message": "Carrinho nao localizado"})
    except Exception as e:
        return 500, {"message": str(e)}


@api.post("fechar-pedido", response={200:dict, 404:Error, 500:Error})
def finalizar_carrinho(request, id_carrinho:str):
    try:
        carrinho = Carrinho.objects.get(pk=id_carrinho, finalizado=False)
        carrinho.pedido = str(uuid.uuid4())
        carrinho.finalizado = True
        carrinho.save()
        
        valor_final = carrinho._get_total_cart()
        """ Cria o pedido """
        # TODO: conectar com mercado pago para obter cod de pagamento e status
        Pedido(carrinho_pedido=carrinho.pedido, total_pedido=valor_final).save()
        return 200, ({"sucesso":"pedido criado"})
    except Carrinho.DoesNotExist:
        return 404, ({"message":"carrinho nao localizado"})
    except Exception as e:
        return 500, {"message": str(e)}
        