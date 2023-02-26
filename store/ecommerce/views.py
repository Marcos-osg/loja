from django.shortcuts import render
from django.http import HttpResponse
from .models import Products

# Create your views here.

def products(request):
    products = Products.objects.all()

    context = {'products':products}
    return render(request, 'ecommerce/products.html', context)