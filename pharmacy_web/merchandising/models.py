from django.db import models
from django.utils import timezone
import json

class Laboratory(models.Model):
    """Modèle représentant un laboratoire pharmaceutique"""
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to='laboratories/', blank=True, null=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Laboratoire"
        verbose_name_plural = "Laboratoires"

class Product(models.Model):
    """Modèle représentant un produit pharmaceutique"""
    name = models.CharField(max_length=200)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    ean = models.CharField(max_length=13, blank=True, null=True)
    
    @property
    def margin(self):
        """Calcule la marge du produit"""
        return self.price - self.cost
        
    @property
    def margin_percentage(self):
        """Calcule le pourcentage de marge du produit"""
        if self.price == 0:
            return 0
        return (self.margin / self.price) * 100
        
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

class Pharmacy(models.Model):
    """Modèle représentant une pharmacie"""
    name = models.CharField(max_length=100)
    width = models.IntegerField(default=1200)
    height = models.IntegerField(default=800)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Pharmacie"
        verbose_name_plural = "Pharmacies"

class PharmacyElement(models.Model):
    """Modèle pour les éléments de la pharmacie"""
    ELEMENT_TYPES = [
        ('SHELF', 'Rayon'),
        ('TG', 'Tête de Gondole'),
        ('BAC', 'Bac Soldeur'),
        ('ENTRANCE', 'Entrée'),
        ('EXIT', 'Sortie'),
        ('COUNTER', 'Comptoir'),
    ]
    
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="elements")
    name = models.CharField(max_length=100)
    element_type = models.CharField(max_length=20, choices=ELEMENT_TYPES)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    orientation = models.CharField(max_length=20, default="horizontal", 
                                   choices=[("horizontal", "Horizontal"), ("vertical", "Vertical")])
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    
    # Données de vente stockées en JSON
    sales_data = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def revenue(self):
        data = self.sales_data or {}
        return data.get('revenue', 0)
        
    @property
    def profit(self):
        data = self.sales_data or {}
        return data.get('profit', 0)
        
    @property
    def units_sold(self):
        data = self.sales_data or {}
        return data.get('units_sold', 0)
        
    @property
    def margin_percentage(self):
        if self.revenue == 0:
            return 0
        return (self.profit / self.revenue) * 100
        
    def __str__(self):
        return f"{self.name} ({self.get_element_type_display()})"
        
    class Meta:
        verbose_name = "Élément de pharmacie"
        verbose_name_plural = "Éléments de pharmacie"