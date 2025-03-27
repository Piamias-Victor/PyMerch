from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.index, name='index'),
    path('pharmacy/create/', views.create_pharmacy, name='create_pharmacy'),
    path('pharmacy/<int:pharmacy_id>/', views.pharmacy_map, name='pharmacy_map'),
    path('pharmacy/<int:pharmacy_id>/analytics/', views.analytics, name='analytics'),
    path('pharmacy/<int:pharmacy_id>/products/', views.pharmacy_products, name='pharmacy_products'),
    path('pharmacy/<int:pharmacy_id>/settings/', views.pharmacy_settings, name='pharmacy_settings'),
    
    # Vues spéciales
    path('pharmacy/<int:pharmacy_id>/revenue/', views.revenue_view, name='revenue_view'),
    path('pharmacy/<int:pharmacy_id>/margin/', views.margin_view, name='margin_view'),
    path('pharmacy/<int:pharmacy_id>/labs/', views.lab_distribution, name='lab_distribution'),
    
    # Export
    path('pharmacy/<int:pharmacy_id>/export/', views.export_plan, name='export_plan'),
    path('pharmacy/<int:pharmacy_id>/export-data/', views.export_data, name='export_data'),
    
    # Gestion des éléments
    path('element/<int:element_id>/', views.element_details, name='element_details'),
    path('element/<int:element_id>/products/', views.element_products, name='element_products'),
    
    # Gestion des laboratoires et produits
    path('laboratories/', views.laboratories, name='laboratories'),
    path('laboratory/<int:laboratory_id>/', views.laboratory_details, name='laboratory_details'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    
    # API pour les opérations AJAX
    path('api/pharmacy/<int:pharmacy_id>/elements/', views.get_pharmacy_elements, name='api_pharmacy_elements'),
    path('api/element/<int:element_id>/', views.get_element_data, name='api_element_data'),
    path('api/element/<int:element_id>/update/', views.update_element, name='api_update_element'),
    path('api/pharmacy/<int:pharmacy_id>/stats/by-type/', views.get_stats_by_type, name='api_stats_by_type'),
    path('api/pharmacy/<int:pharmacy_id>/stats/by-lab/', views.get_stats_by_lab, name='api_stats_by_lab'),
]