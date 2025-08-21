"""
URL configuration for API endpoints
"""
from django.urls import path
from . import resolwe_views

urlpatterns = [
    # Health check (keep using views for non-resolwe functionality)
    path('health/', resolwe_views.health_check, name='health_check'),
    
    # CSRF token endpoint
    path('base/csrf', resolwe_views.csrf_view, name='csrf_view'),
    path('base/csrf/', resolwe_views.csrf_view, name='csrf_view'),

    # Descriptor Schema API (using Resolwe database)
    path('descriptorschema/', resolwe_views.descriptor_schema_api, name='descriptor_schema_api'),
    
    # Time Series Relations API (using Resolwe)
    path('relation/', resolwe_views.relation_api, name='relation_api'),
    
    
    # Basket APIs (using Resolwe)
    path('basket/_/add_samples', resolwe_views.basket_add_samples, name='basket_add_samples'),
    path('_modules/visualizations/basket_expressions', resolwe_views.basket_expressions, name='basket_expressions'),
    
    # Differential Expression API (using Resolwe)
    path('_modules/differential_expression/list', resolwe_views.differential_expression_list, name='differential_expression_list'),
    
    # Gene List API (using Resolwe Bio)
    path('_modules/gene_list/list_by_ids', resolwe_views.gene_list_by_ids, name='gene_list_by_ids'),
    
    # User API (using Resolwe)
    path('user/', resolwe_views.user_api, name='user_api'),

    # Data API (using Resolwe with django-filter)
    path('data/', resolwe_views.data_api, name='data_api'),
    # Alternative: Use ViewSet directly in DRF router for even cleaner code

    #Storage API (using Resolwe)
    path('storage/<int:pk>', resolwe_views.storage_api, name='storage_api'),
    
    
]
