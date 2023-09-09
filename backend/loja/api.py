from typing import List
from ninja import NinjaAPI

from backend.loja.schemas import CamisasSchema
from backend.loja.models import Camisetas

api = NinjaAPI()

@api.get("/camisetas", response=List[CamisasSchema])
def camisetas(request):
    camisetas = Camisetas.objects.all()
    return camisetas
