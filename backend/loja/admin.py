from django.contrib import admin
from backend.loja.models import Camisetas, Header

excluded_fields = [ field.name for field in Header._meta.fields]

@admin.register(Camisetas)
class AuthorAdmin(admin.ModelAdmin):
    fields = [field.name for field in Camisetas._meta.fields if field.name not in excluded_fields]