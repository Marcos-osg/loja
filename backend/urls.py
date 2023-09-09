from django.contrib import admin
from django.urls import path

from backend.loja.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loja/v1/', api.urls),
]
