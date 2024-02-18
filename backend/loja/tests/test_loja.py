from unittest import TestCase

from ..models import *

class TesteLoja(TestCase):

    def setUp(self) -> None:
        self.id_produto = "af2ce333-2d22-4000-b9eb-dd5bc5d9a2a6"
        # self.id_produto = "f5ee01b3-984a-4aa8-b583-7ae6fc2748e2"
        self.id_carrinho = "7360abc7-1bf5-41de-9c74-1048f8809273"
        self.quantidade = 3
        self.quantidade_delete = 1

    
    def test_get_product(self):
        try:
            produto = Produtos.objects.get(pk=self.id_produto)
            print("Produto: ", produto)
        except Produtos.DoesNotExist:
            print("Produto não localizado ")

    def test_get_cart(self):
        carrinho, _ = Carrinho.objects.get_or_create(pk=self.id_carrinho)
        print("Carrinho: ", carrinho)

    
    def test_add_to_cart(self):
        carrinho, _ = Carrinho.objects.get_or_create(pk=self.id_carrinho)
        
        try:
            itens_carrinho = ItensCarrinho()
            produto = Produtos.objects.get(pk=self.id_produto)
            
            """ verifica se o produto já existe no carrinho se existente altera a quantidade, caso contrario adiciona """
            item = ItensCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()

            if item:
                item.quantidade += self.quantidade
                item.save()
            else:
                itens_carrinho.carrinho = carrinho
                itens_carrinho.produto = produto
                itens_carrinho.quantidade = self.quantidade
                itens_carrinho.save()
                print(f"O produto {produto._name_product()} foi adicionado ao carrinho")
            
        except Exception as e:
            print(e)
        except Produtos.DoesNotExist:
            print("produto não encontrado")
            
    def test_del_from_cart(self):
        carrinho, _ = Carrinho.objects.get_or_create(pk=self.id_carrinho)
        
        try:
            produto = Produtos.objects.get(pk=self.id_produto)
            
            """ verifica se o produto já existe no carrinho se existente altera a quantidade, caso contrario exclui """
            item = ItensCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()

            if item:
                if item.quantidade <= 1 or item.quantidade <= self.quantidade_delete:
                    item.delete()
                    print(f"O produto {produto._name_product()} foi removido do carrinho")
                else:
                    item.quantidade -= self.quantidade_delete
                    item.save()

        except Exception as e:
            print(e)
        except Produtos.DoesNotExist:
            print("produto não encontrado")
            
    def test_list_cart(self):
        carrinho, _ = Carrinho.objects.get_or_create(pk=self.id_carrinho)
        itens_carrinho = ItensCarrinho.objects.filter(carrinho=carrinho)
        print("itens do carrinho")
        for item in itens_carrinho:
            print(item)
        print("total do carrinho: ", carrinho._get_total_cart())
        