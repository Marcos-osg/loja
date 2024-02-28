# Generated by Django 4.2.10 on 2024-02-24 16:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql="""CREATE SCHEMA IF NOT EXISTS loja"""
        ),
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pedido', models.CharField(blank=True, max_length=50, null=True)),
                ('valor_final', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('finalizado', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Carrinho de compra',
                'verbose_name_plural': 'Carrinhos de compras',
                'db_table': 'loja"."carrinho de compra',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('carrinho_pedido', models.CharField(max_length=50)),
                ('total_pedido', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('cod_pagamento', models.CharField(blank=True, max_length=50, null=True)),
                ('status_pagamento', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'loja"."pedido',
            },
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tipo', models.CharField(choices=[('Calcas', 'Calças'), ('Camiseta', 'Camiseta'), ('Blusa', 'Blusa'), ('Shorts', 'Shorts')], max_length=64)),
                ('cor', models.CharField(choices=[('Branco', 'Branco'), ('Preto', 'Preto'), ('Vermelho', 'Vermelho'), ('Azul', 'Azul'), ('Verde', 'Verde'), ('Amarelo', 'Amarelo'), ('Laranja', 'Laranja'), ('Rosa', 'Rosa'), ('Roxo', 'Roxo'), ('Marrom', 'Marrom'), ('Cinza', 'Cinza')], max_length=64)),
                ('tamanho', models.CharField(choices=[('PP', 'Pequeno'), ('P', 'Pequeno'), ('M', 'Médio'), ('G', 'Grande'), ('GG', 'Extra Grande')], max_length=64)),
                ('marca', models.CharField(choices=[('Nike', 'Nike'), ('Adidas', 'Adidas'), ('Puma', 'Puma'), ('Reebok', 'Reebok'), ('Converse', 'Converse'), ('New Balance', 'New Balance'), ('Vans', 'Vans'), ('Under Armour', 'Under Armour'), ('Fila', 'Fila'), ('ASICS', 'ASICS')], max_length=64)),
                ('preco', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('preco_promo', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('estoque', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'db_table': 'loja"."produto',
            },
        ),
        migrations.CreateModel(
            name='ItensCarrinho',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('valor_unitario', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('valor_total_produto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.carrinho')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.produtos')),
            ],
            options={
                'verbose_name': 'Item do Carrinho',
                'verbose_name_plural': 'Itens do Carrinho',
                'db_table': 'loja"."item do carrinho',
            },
        ),
    ]
