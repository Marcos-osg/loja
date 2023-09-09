from ninja.orm import create_schema

from backend.loja.models import Header, Camisetas, Blusas, Calcas

excluded = [field.name for field in Header._meta.fields]

CamisasSchema = create_schema(
    Camisetas,
    fields = [field.name for field in Camisetas._meta.fields if  field.name not in excluded]
)

BlusasSchema = create_schema(
    Blusas,
    fields = [field.name for field in Blusas._meta.fields if  field.name not in excluded]
)

CalcasSchema = create_schema(
    Calcas,
    fields = [field.name for field in Calcas._meta.fields if  field.name not in excluded]
)