from django.urls import path
from store.ecommerce import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.products, name='products'),
]