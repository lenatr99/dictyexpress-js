"""
URL configuration for API endpoints
"""
from django.urls import path
from . import resolwe_views

urlpatterns = [
    # API root endpoint (required by resdk)
    path('', resolwe_views.api_root, name='api_root'),
    
    # Version endpoint (required by resdk)
    path('resdk_minimal_supported_version', resolwe_views.resdk_version, name='resdk_version'),
    
    # Health check (keep using views for non-resolwe functionality)
    path('health/', resolwe_views.health_check, name='health_check'),

    path("upload/", resolwe_views.upload_file, name="upload_file"),
    
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
    
    # User API (using Resolwe) - both with and without trailing slash for compatibility
    path('user/', resolwe_views.user_api, name='user_api'),
    path('user', resolwe_views.user_api, name='user_api_no_slash'),

    # Data API (using Resolwe with django-filter) - supports both GET and POST
    path('data/', resolwe_views.data_api, name='data_api'),
    path('data', resolwe_views.data_api, name='data_api'),
    # Alternative: Use ViewSet directly in DRF router for even cleaner code

    #Storage API (using Resolwe)
    path('storage/<int:pk>', resolwe_views.storage_api, name='storage_api'),

    #process API (using Resolwe)
    path('process/', resolwe_views.process_api, name='process_api'),
    path('process', resolwe_views.process_api, name='process_api'),
    
    
]
