from django.contrib import admin
from .models import Pharmacy, PharmacyElement, Laboratory, Product

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', 'created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'

@admin.register(PharmacyElement)
class PharmacyElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'element_type', 'pharmacy', 'laboratory', 'revenue', 'profit')
    list_filter = ('element_type', 'pharmacy', 'laboratory')
    search_fields = ('name',)
    date_hierarchy = 'created_at'

@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')
    search_fields = ('name', 'contact')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'laboratory', 'price', 'cost', 'margin', 'margin_percentage', 'stock')
    list_filter = ('laboratory',)
    search_fields = ('name', 'ean')