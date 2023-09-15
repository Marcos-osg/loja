from typing import List
from ninja import NinjaAPI
from uuid import uuid4

from backend.loja.schemas import ProdutosSchema, ItemCarrinhoIn, ItemCarrinhoOut
from backend.loja.models import Produtos, ItensCarrinho, Carrinho


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
            carrinho = Carrinho.objects.get(pedido=session)
        cart_itens = ItensCarrinho.objects.filter(carrinho=carrinho).all()
        if cart_itens:
            valor_final = 0
            for i in cart_itens:
                if _produto == i.produto:
                    i.quantidade = payload.quantidade + i.quantidade
                    i.valor_produtos = _produto.preco + i.valor_produtos
                    i.save()
                    valor_final += i.valor_produtos
            carrinho.valor_final = valor_final
            carrinho.save()
            item = ItensCarrinho(produto=_produto, quantidade=payload.quantidade, carrinho=carrinho)
            item.save()
        else:
            item = ItensCarrinho(produto=_produto, quantidade=payload.quantidade, carrinho=carrinho)
            item.save()
            carrinho.valor_final = carrinho.valor_final + item.valor_produtos
            carrinho.save()
        data["sucesso"] = "Produto adicionado ao carrinho"
    except Exception as e:
        print(e)
        data["erro"] = "Ocorreu um erro ao adicionar o produto ao carrinho"

    return data

@api.post("/remove-item-carrinho")
def remove_item_carrinho(request, payload: ItemCarrinhoOut):
    data = {}
    try:
        session = request.session["cart"]

        produto = Produtos.objects.get(id=payload.produto)
        carrinho = Carrinho.objects.filter(pedido=session).first()
        if not carrinho:
            carrinho = Carrinho(
                pedido=session
            ).save()
        cart_itens = ItensCarrinho.objects.filter(carrinho=carrinho).all()
        if cart_itens:
            valor_final = 0
            for i in cart_itens:
                if i.produto == produto:
                    if i.quantidade == payload.quantidade:
                        item_delete = ItensCarrinho.objects.get(carrinho=carrinho, produto=i.produto)
                        print("item para deletar",item_delete)
                        item_delete.delete()
                        produto.estoque = produto.estoque + payload.quantidade
                        produto.save()
                    else:
                        i.quantidade -= payload.quantidade
                        i.valor_produtos = produto.preco - i.valor_produtos
                        i.save()
                        produto.estoque = produto.estoque + payload.quantidade
                        produto.save()
                        valor_final -= i.valor_produtos
            carrinho.valor_final = valor_final
            carrinho.save() 

        carrinho.valor_final = carrinho.valor_final - (produto.preco * payload.quantidade)
        carrinho.save()
        data["sucesso"] = "Produto removido do carrinho"
    except Exception as e:
        print(e)
        data["erro"] = "Ocorreu um erro ao remover o produto do carrinho"

    return data

@api.get("/carrinho")
def render_cart(request):
    try:
        itens_carrinho = {}
        session = request.session["cart"]
        _cart = Carrinho.objects.get(pedido=session)
        items = ItensCarrinho.objects.filter(carrinho=_cart)

        if not items:
            itens_carrinho["vazio"] = "Seu carrinho de compras está vazio"
        count = 0
        for i in items:
            count += 1
            itens_carrinho[f"produto_{count}"] = {
                "produto":f"{i.produto.tipo} {i.produto.marca} {i.produto.cor}",
                "tamanho": i.produto.tamanho,
                "valor_produto":i.produto.preco, 
                "quantidade":i.quantidade,
                "valor_total_produto":i.valor_produtos,
            }
        
        return itens_carrinho
    except:
        return {"erro":"Carrinho de compras não localizado"}