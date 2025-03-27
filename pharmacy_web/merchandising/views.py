from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count
import json
import csv
from .models import Pharmacy, PharmacyElement, Laboratory, Product
from .forms import PharmacyForm, PharmacyElementForm

def index(request):
    """Page d'accueil"""
    pharmacies = Pharmacy.objects.all()
    context = {
        'pharmacies': pharmacies,
    }
    return render(request, 'pharmacy/index.html', context)

def create_pharmacy(request):
    """Création d'une nouvelle pharmacie"""
    if request.method == 'POST':
        form = PharmacyForm(request.POST)
        if form.is_valid():
            pharmacy = form.save()
            return redirect('pharmacy_map', pharmacy_id=pharmacy.id)
    else:
        form = PharmacyForm()
    
    context = {
        'form': form,
    }
    return render(request, 'pharmacy/create_pharmacy.html', context)

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
    
    context = {
        'pharmacy': pharmacy,
        'elements': elements,
    }
    return render(request, 'pharmacy/analytics.html', context)

def pharmacy_products(request, pharmacy_id):
    """Gestion des produits de la pharmacie"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    products = Product.objects.all()
    
    context = {
        'pharmacy': pharmacy,
        'products': products,
    }
    return render(request, 'pharmacy/pharmacy_products.html', context)

def pharmacy_settings(request, pharmacy_id):
    """Paramètres de la pharmacie"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    
    if request.method == 'POST':
        form = PharmacyForm(request.POST, instance=pharmacy)
        if form.is_valid():
            form.save()
            return redirect('pharmacy_map', pharmacy_id=pharmacy.id)
    else:
        form = PharmacyForm(instance=pharmacy)
    
    context = {
        'pharmacy': pharmacy,
        'form': form,
    }
    return render(request, 'pharmacy/pharmacy_settings.html', context)

def revenue_view(request, pharmacy_id):
    """Vue spéciale: Chiffre d'affaires"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.all()
    
    context = {
        'pharmacy': pharmacy,
        'elements': elements,
        'view_type': 'revenue',
    }
    return render(request, 'pharmacy/special_view.html', context)

def margin_view(request, pharmacy_id):
    """Vue spéciale: Taux de marge"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.all()
    
    context = {
        'pharmacy': pharmacy,
        'elements': elements,
        'view_type': 'margin',
    }
    return render(request, 'pharmacy/special_view.html', context)

def lab_distribution(request, pharmacy_id):
    """Vue spéciale: Répartition par laboratoire"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.exclude(laboratory=None)
    
    context = {
        'pharmacy': pharmacy,
        'elements': elements,
        'view_type': 'lab',
    }
    return render(request, 'pharmacy/special_view.html', context)

def element_products(request, element_id):
    """Gestion des produits d'un élément"""
    element = get_object_or_404(PharmacyElement, id=element_id)
    
    if request.method == 'POST':
        product_ids = request.POST.getlist('products')
        element.products.clear()
        for product_id in product_ids:
            product = get_object_or_404(Product, id=product_id)
            element.products.add(product)
        return redirect('element_details', element_id=element.id)
    
    all_products = Product.objects.all()
    
    context = {
        'element': element,
        'all_products': all_products,
    }
    return render(request, 'pharmacy/element_products.html', context)

def laboratories(request):
    """Liste des laboratoires"""
    labs = Laboratory.objects.all()
    
    context = {
        'laboratories': labs,
    }
    return render(request, 'pharmacy/laboratories.html', context)

def laboratory_details(request, laboratory_id):
    """Détails d'un laboratoire"""
    lab = get_object_or_404(Laboratory, id=laboratory_id)
    products = lab.products.all()
    
    context = {
        'laboratory': lab,
        'products': products,
    }
    return render(request, 'pharmacy/laboratory_details.html', context)

def products(request):
    """Liste des produits"""
    products_list = Product.objects.all()
    
    context = {
        'products': products_list,
    }
    return render(request, 'pharmacy/products.html', context)

def product_details(request, product_id):
    """Détails d'un produit"""
    product = get_object_or_404(Product, id=product_id)
    
    context = {
        'product': product,
    }
    return render(request, 'pharmacy/product_details.html', context)

def export_plan(request, pharmacy_id):
    """Export du plan de la pharmacie"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.all()
    
    # Format JSON
    data = {
        'pharmacy': {
            'id': pharmacy.id,
            'name': pharmacy.name,
            'width': pharmacy.width,
            'height': pharmacy.height,
        },
        'elements': []
    }
    
    for element in elements:
        element_data = {
            'id': element.id,
            'name': element.name,
            'type': element.element_type,
            'x': element.x,
            'y': element.y,
            'width': element.width,
            'height': element.height,
            'orientation': element.orientation,
            'laboratory': element.laboratory.name if element.laboratory else None,
        }
        data['elements'].append(element_data)
    
    response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="pharmacy_{pharmacy.id}_plan.json"'
    return response

def export_data(request, pharmacy_id):
    """Export des données de vente"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="pharmacy_{pharmacy.id}_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nom', 'Type', 'Laboratoire', 'CA (€)', 'Marge (€)', 'Taux de marge (%)', 'Unités vendues'])
    
    for element in elements:
        writer.writerow([
            element.id,
            element.name,
            element.get_element_type_display(),
            element.laboratory.name if element.laboratory else 'Aucun',
            element.revenue,
            element.profit,
            element.margin_percentage,
            element.units_sold,
        ])
    
    return response

# API pour les opérations AJAX
def get_pharmacy_elements(request, pharmacy_id):
    """API pour récupérer les éléments d'une pharmacie au format JSON"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.all()
    
    elements_data = []
    for element in elements:
        element_data = {
            'id': element.id,
            'name': element.name,
            'element_type': element.element_type,
            'x': element.x,
            'y': element.y,
            'width': element.width,
            'height': element.height,
            'laboratory': element.laboratory.name if element.laboratory else None,
            'sales_data': element.sales_data,
        }
        elements_data.append(element_data)
    
    data = {
        'pharmacy_id': pharmacy.id,
        'pharmacy_name': pharmacy.name,
        'elements': elements_data,
    }
    
    return JsonResponse(data)

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

def get_stats_by_type(request, pharmacy_id):
    """API pour obtenir les statistiques par type d'élément"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.all()
    
    # Préparation des données par type
    stats = {}
    for element in elements:
        element_type = element.element_type
        if element_type not in stats:
            stats[element_type] = {
                'element_type': element_type,
                'total_revenue': 0,
                'total_profit': 0,
                'count': 0,
            }
        
        stats[element_type]['total_revenue'] += element.revenue
        stats[element_type]['total_profit'] += element.profit
        stats[element_type]['count'] += 1
    
    # Conversion en liste
    stats_list = list(stats.values())
    
    return JsonResponse(stats_list, safe=False)

def get_stats_by_lab(request, pharmacy_id):
    """API pour obtenir les statistiques par laboratoire"""
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    elements = pharmacy.elements.exclude(laboratory=None)
    
    # Préparation des données par laboratoire
    stats = {}
    for element in elements:
        lab_name = element.laboratory.name
        if lab_name not in stats:
            stats[lab_name] = {
                'laboratory__name': lab_name,
                'total_revenue': 0,
                'total_profit': 0,
                'count': 0,
            }
        
        stats[lab_name]['total_revenue'] += element.revenue
        stats[lab_name]['total_profit'] += element.profit
        stats[lab_name]['count'] += 1
    
    # Conversion en liste
    stats_list = list(stats.values())
    
    return JsonResponse(stats_list, safe=False)