from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count

from .models import Pharmacy, PharmacyElement, Laboratory, Product
from .forms import PharmacyForm, PharmacyElementForm

def index(request):
    """Page d'accueil"""
    pharmacies = Pharmacy.objects.all()
    context = {
        'pharmacies': pharmacies,
    }
    return render(request, 'pharmacy/index.html', context)

def pharmacy_map(request, pharmacy_id):
    """Affichage du plan de la pharmacie"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.all()
    laboratories = Laboratory.objects.all()
    
    context = {
        'pharmacy': pharmacy,
        'elements': elements,
        'laboratories': laboratories,
    }
    return render(request, 'pharmacy/pharmacy_map.html', context)

def element_details(request, element_id):
    """Détails d'un élément de la pharmacie"""
    element = get_object_or_404(PharmacyElement, id=element_id)
    laboratories = Laboratory.objects.all()
    products = Product.objects.all()
    
    # Si l'élément a un laboratoire, récupérer ses produits
    lab_products = []
    if element.laboratory:
        lab_products = element.laboratory.products.all()
    
    context = {
        'element': element,
        'laboratories': laboratories,
        'products': products,
        'lab_products': lab_products,
    }
    return render(request, 'pharmacy/element_details.html', context)

def analytics(request, pharmacy_id):
    """Affichage des analyses et statistiques"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.all()
    
    # Statistiques par type d'élément
    stats_by_type = elements.values('element_type').annotate(
        total_revenue=Sum('sales_data__revenue'),
        total_profit=Sum('sales_data__profit'),
        avg_margin=Avg('sales_data__profit') / Avg('sales_data__revenue') * 100,
        count=Count('id')
    )
    
    # Statistiques par laboratoire
    stats_by_lab = elements.exclude(laboratory=None).values('laboratory__name').annotate(
        total_revenue=Sum('sales_data__revenue'),
        total_profit=Sum('sales_data__profit'),
        avg_margin=Avg('sales_data__profit') / Avg('sales_data__revenue') * 100,
        count=Count('id')
    )
    
    context = {
        'pharmacy': pharmacy,
        'elements': elements,
        'stats_by_type': stats_by_type,
        'stats_by_lab': stats_by_lab,
    }
    return render(request, 'pharmacy/analytics.html', context)

# API pour les opérations AJAX
def get_element_data(request, element_id):
    """API pour récupérer les données d'un élément au format JSON"""
    element = get_object_or_404(PharmacyElement, id=element_id)
    
    data = {
        'id': element.id,
        'name': element.name,
        'type': element.element_type,
        'x': element.x,
        'y': element.y,
        'width': element.width,
        'height': element.height,
        'laboratory': element.laboratory.name if element.laboratory else None,
        'revenue': element.revenue,
        'profit': element.profit,
        'margin_percentage': element.margin_percentage,
        'units_sold': element.units_sold,
        'products': [{'id': p.id, 'name': p.name} for p in element.products.all()]
    }
    
    return JsonResponse(data)

def update_element(request, element_id):
    """API pour mettre à jour un élément via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    element = get_object_or_404(PharmacyElement, id=element_id)
    
    try:
        data = json.loads(request.body)
        
        # Mise à jour des propriétés
        if 'name' in data:
            element.name = data['name']
        if 'x' in data and 'y' in data:
            element.x = data['x']
            element.y = data['y']
        if 'width' in data and 'height' in data:
            element.width = data['width']
            element.height = data['height']
        if 'laboratory_id' in data:
            lab_id = data['laboratory_id']
            if lab_id:
                element.laboratory = get_object_or_404(Laboratory, id=lab_id)
            else:
                element.laboratory = None
                
        # Mise à jour des données de vente
        if 'sales_data' in data:
            element.sales_data = data['sales_data']
            
        element.save()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)