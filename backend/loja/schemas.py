from ninja.orm import create_schema

from backend.loja.models import Header, Camisetas

excluded = [field.name for field in Header._meta.fields]

CamisasSchema = create_schema(
    Camisetas,
    fields = [field.name for field in Camisetas._meta.fields if  field.name not in excluded]
)