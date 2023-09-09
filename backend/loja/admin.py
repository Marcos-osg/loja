from django.contrib import admin
from backend.loja.models import Header, Camisetas, Blusas, Calcas

excluded_fields = [ field.name for field in Header._meta.fields]

@admin.register(Camisetas)
class CamisetaAdmin(admin.ModelAdmin):
    fields = [field.name for field in Camisetas._meta.fields if field.name not in excluded_fields]

@admin.register(Blusas)
class BlusaAdmin(admin.ModelAdmin):
    fields = [field.name for field in Blusas._meta.fields if field.name not in excluded_fields]

@admin.register(Calcas)
class CalcaAdmin(admin.ModelAdmin):
    fields = [field.name for field in Calcas._meta.fields if field.name not in excluded_fields]