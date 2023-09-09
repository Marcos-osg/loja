from typing import List
from ninja import NinjaAPI

from backend.loja.schemas import CamisasSchema, CalcasSchema, BlusasSchema
from backend.loja.models import Camisetas, Blusas, Calcas

api = NinjaAPI()

@api.get("/camisetas", response=List[CamisasSchema])
def camisetas(request):
    camisetas = Camisetas.objects.all()
    return camisetas

@api.get("/blusas", response=List[BlusasSchema])
def blusas(request):
    blusas = Blusas.objects.all()
    return blusas

@api.get("/calcas", response=List[CalcasSchema])
def calcas(request):
    calcas = Calcas.objects.all()
    return calcas


@api.get("/todos_produtos")
def todos_produtos(request):
    data = {}
    excluded_fields = ("id", "created_at", "updated_at")
    calcas = Calcas.objects.all().values()
    blusas = Blusas.objects.all().defer(excluded_fields).values()
    camisetas = Camisetas.objects.all().defer(excluded_fields).values()

    data["blusas"] = []
    data["camisetas"] = []
    data["calcas"] = []

    for item in camisetas:
        for field in excluded_fields:
            item.pop(field, None)
        data["camisetas"] += [item]
    
    for item in blusas:
        for field in excluded_fields:
            item.pop(field, None)
        data["blusas"] += [item]

    for item in calcas:
        for field in excluded_fields:
            item.pop(field, None)
        data["calcas"] += [item]

    return data
