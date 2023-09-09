from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/ola")
def home(request):
    return "Ola"