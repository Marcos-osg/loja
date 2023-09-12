from ninja.orm import create_schema
from ninja import Schema
from pydantic import UUID4

from backend.loja.models import Header, Produtos

excluded = [field.name for field in Header._meta.fields]

ProdutosSchema = create_schema(
    Produtos,
    fields = [field.name for field in Produtos._meta.fields if  field.name not in excluded]
)

class ItemCarrinhoIn(Schema):
    produto: UUID4
    quantidade: int