"""
Resolwe-integrated API views to replace mock data endpoints
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.db.models import Q
from datetime import datetime
import json
import uuid
from pathlib import Path

# Resolwe imports
from resolwe.flow.models import Data, DescriptorSchema, Collection, Process, Entity, Storage, RelationPartition, Relation
from resolwe.flow.views import DataViewSet, DescriptorSchemaViewSet, RelationViewSet, StorageViewSet, ProcessViewSet
from resolwe_bio.kb.views import FeatureViewSet
from django.contrib.auth import get_user_model

# In-memory storage for baskets (will be reset on server restart)
BASKETS = {}


@api_view(["POST"])
def upload_file(request):
    """
    Minimal upload endpoint: accepts multipart/form-data with a 'file' field.
    Saves to RESOLWE_STORAGE 'upload' bucket and returns the stored filename.
    """
    up = request.FILES.get("file")
    if not up:
        return Response({"error": "Missing 'file' field"}, status=400)

    # Where Resolwe stores uploads (local connector + 'upload' mapping)
    base = Path(settings.RESOLWE_STORAGE["connectors"]["local"]["config"]["path"])
    upload_dir = base / "upload"
    upload_dir.mkdir(parents=True, exist_ok=True)

    dest = upload_dir / up.name
    with dest.open("wb+") as fh:
        for chunk in up.chunks():
            fh.write(chunk)

    # Return the relative filename; you'll use this under input.exp / input.rc
    return Response({"filename": up.name})



@api_view(["GET"])
def health_check(request):
    """Health check endpoint"""
    return Response({"status": "ok", "timestamp": datetime.now().isoformat()})


@api_view(["GET"])
@ensure_csrf_cookie
def csrf_view(request):
    """CSRF token endpoint"""
    csrf_token = get_token(request)
    return Response({"csrfToken": csrf_token})


@api_view(["GET"])
def descriptor_schema_api(request):
    view = DescriptorSchemaViewSet.as_view({"get": "list"})
    return view(request._request)


@api_view(["GET", "POST"])
def relation_api(request):
    view = RelationViewSet.as_view({"get": "list"})
    return view(request._request)


@api_view(["GET", "POST"])
def process_api(request):
    view = ProcessViewSet.as_view({"get": "list"})
    return view(request._request)

        
# Simplified Data API - shorter version of what works
@api_view(["GET", "POST"])
def data_api(request, *args, **kwargs):
    if request.method == "GET":
        view = DataViewSet.as_view({"get": "list"})
        response = view(request._request, *args, **kwargs)
        return Response(response.data['results'])
    elif request.method == "POST":
        # Convert process slug to ID if needed
        process_ref = request.data.get('process')
        
        # Handle different process reference formats
        if isinstance(process_ref, dict):
            # If process_ref is a dict like {'slug': 'upload-expression'}
            if 'slug' in process_ref:
                process_slug = process_ref['slug']
                try:
                    process = Process.objects.get(slug=process_slug)
                except Process.DoesNotExist:
                    return Response({"process": [f"Process '{process_slug}' not found."]}, 
                                  status=status.HTTP_400_BAD_REQUEST)
            elif 'id' in process_ref:
                process_id = process_ref['id']
                try:
                    process = Process.objects.get(id=process_id)
                except Process.DoesNotExist:
                    return Response({"process": [f"Process ID {process_id} not found."]}, 
                                  status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"process": ["Invalid process reference format."]}, 
                              status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(process_ref, str):
            try:
                process = Process.objects.get(slug=process_ref)
            except Process.DoesNotExist:
                return Response({"process": [f"Process '{process_ref}' not found."]}, 
                              status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(process_ref, int):
            try:
                process = Process.objects.get(id=process_ref)
            except Process.DoesNotExist:
                return Response({"process": [f"Process ID {process_ref} not found."]}, 
                              status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"process": ["Process reference must be a string (slug), integer (ID), or dict with 'slug' or 'id' key."]}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Get admin user and create data object
        User = get_user_model()
        admin_user, _ = User.objects.get_or_create(username="admin", 
                                                  defaults={"email": "admin@example.com"})
        
        # Handle file inputs properly for Resolwe
        input_data = request.data.get('input', {})
        
        # For upload-expression process, we need to handle the 'exp' file input
        if 'exp' in input_data and isinstance(input_data['exp'], dict) and 'file' in input_data['exp']:
            file_name = input_data['exp']['file']
            # Create a simple file reference that Resolwe can work with
            # In a real implementation, files should be uploaded to Resolwe storage first
            input_data['exp'] = {
                'file': file_name,
                'file_temp': f'/app/resolwe_data/upload/{file_name}'  # Use Docker volume path
            }
        
        # Create data object and trigger processing 
        try:
            from resolwe.flow.models import Data
            from resolwe.flow.managers import manager
            
            data_obj = Data.objects.create(
                name=request.data.get('name', 'Unnamed'),
                process=process,
                contributor=admin_user,
                input=input_data,
                tags=request.data.get('tags', [])
            )
            
            # Note: The worker should automatically pick up new data objects in 'RE' status
            print(f"Data {data_obj.id} created and ready for processing")
                
        except Exception as e:
            return Response({"error": f"Data creation failed: {e}"}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Note: Data starts in 'RE' (Resolving) status and will be processed by the worker
        # Make sure Docker services are running: docker compose up -d worker listener
        
        return Response({
            "id": data_obj.id,
            "name": data_obj.name,
            "process": {"slug": process.slug, "name": process.name},
            "status": data_obj.status,
            "created": data_obj.created.isoformat()
        }, status=status.HTTP_201_CREATED)
    
@api_view(["POST"])
def upload_api(request):
    # Use the underlying Django HttpRequest and make POST mutable
    req = request._request
    if hasattr(req, "POST"):
        req.POST = req.POST.copy()
    view = UploadViewSet.as_view({"post": "create"})
    return view(req)

@api_view(["GET"])
def storage_api(request, pk):
    view = StorageViewSet.as_view({"get": "retrieve"})
    return view(request._request, pk=pk)


@api_view(["POST"])
def basket_add_samples(request):
    """Basket API using Resolwe Data objects"""
    samples = request.data.get("samples", [])
    
    if not samples:
        return Response(
            {"error": "No samples provided"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get organisms and sources from Entity data using Resolwe ORM
        entities_qs = Entity.objects.filter(
            id__in=samples
        ).prefetch_related('data')
        
        organisms, sources = _extract_metadata_from_entities(entities_qs)
        
        # Create basket with clean structure
        basket_data = _create_basket_response(samples, organisms, sources)
        BASKETS[basket_data["id"]] = basket_data
        
        return Response(basket_data)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to add samples to basket: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _extract_metadata_from_entities(entities_qs):
    """Extract species and source metadata from entity data objects"""
    organisms = set()
    sources = set()
    
    for entity in entities_qs:
        for data_obj in entity.data.all():
            if data_obj.output:
                organisms.add(data_obj.output.get('species'))
                sources.add(data_obj.output.get('source'))
    
    # Filter out None values and provide defaults
    organisms = [org for org in organisms if org] or ["Dictyostelium discoideum", "Dictyostelium purpureum"]
    sources = [src for src in sources if src] or ["DICTYBASE"]
    
    return organisms, sources


def _create_basket_response(samples, organisms, sources):
    """Create clean basket response structure"""
    return {
        "id": str(uuid.uuid4()),
        "modified": datetime.now().isoformat(),
        "ignored": [],
        "duplicated": [],
        "samples": samples,
        "permitted_organisms": organisms,
        "permitted_sources": sources,
        "conflict_organisms": [],
        "conflict_sources": [],
    }


@api_view(["GET"])
def basket_expressions(request):
    """Get expression data for basket samples"""
    basket_id = request.GET.get("basket")
    
    if not basket_id or basket_id not in BASKETS:
        return Response(
            {"error": "Invalid or missing basket ID"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        basket = BASKETS[basket_id]
        sample_ids = basket["samples"]
        
        # Get Data objects with exp_type from entity samples
        expressions = Data.objects.filter(
            entity__id__in=sample_ids
        ).values('id', 'output__exp_type')
        
        # Format response to match expected structure
        result = [
            {"id": expr["id"], "exp_type": expr["output__exp_type"]} 
            for expr in expressions 
            if expr["output__exp_type"]
        ]
        
        return Response(result)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to get basket expressions: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def differential_expression_list(request):
    """List differential expression data with tag filtering"""
    # Use same pattern as data_api but with supported filtering
    view = DataViewSet.as_view({"get": "list"})
    
    # Create a mutable copy of GET parameters
    get_params = request._request.GET.copy()
    get_params['type'] = 'data:differentialexpression'  # Use supported parameter
    
    # Apply tag filtering if provided
    tags = request.GET.get("tags")
    if tags:
        get_params['tags'] = tags  # Use supported parameter
    
    # Replace the GET params
    request._request.GET = get_params
    
    response = view(request._request)
    
    # Transform the data to flatten nested descriptor fields
    if hasattr(response, 'data') and isinstance(response.data, dict) and 'results' in response.data:
        transformed_results = []
        for item in response.data['results']:
            # Create a copy of the item
            transformed_item = dict(item)
            
            # Extract nested descriptor fields and flatten them
            if 'descriptor' in item and isinstance(item['descriptor'], dict):
                descriptor = item['descriptor']
                
                # Extract thresholds if they exist
                if 'thresholds' in descriptor and isinstance(descriptor['thresholds'], dict):
                    thresholds = descriptor['thresholds']
                    
                    # Map nested fields to expected flat structure
                    if 'prob_field' in thresholds:
                        transformed_item['prob_field'] = thresholds['prob_field']
                    if 'prob' in thresholds:
                        transformed_item['prob_threshold'] = thresholds['prob']
                    if 'logfc' in thresholds:
                        transformed_item['logfc_threshold'] = thresholds['logfc']
                
                # Add additional fields that might be directly in descriptor
                if 'up_regulated' in descriptor:
                    transformed_item['up_regulated'] = descriptor['up_regulated']
                elif 'output' in item and 'up_regulated' in item['output']:
                    transformed_item['up_regulated'] = item['output']['up_regulated']
                else:
                    # Default value if not found
                    transformed_item['up_regulated'] = 0
                
                if 'down_regulated' in descriptor:
                    transformed_item['down_regulated'] = descriptor['down_regulated']
                elif 'output' in item and 'down_regulated' in item['output']:
                    transformed_item['down_regulated'] = item['output']['down_regulated']
                else:
                    # Default value if not found
                    transformed_item['down_regulated'] = 0
            
            transformed_results.append(transformed_item)
        
        return Response(transformed_results)
    else:
        return Response(response.data if hasattr(response, 'data') else [])


@api_view(["POST"])
def gene_list_by_ids(request):
    """Get features by IDs using Resolwe Bio FeatureViewSet"""
    # Extract feature IDs from request body (handle both 'gene_ids' and 'feature_ids')
    feature_ids = request.data.get('gene_ids', request.data.get('feature_ids', []))
    if not feature_ids:
        return Response([], status=status.HTTP_200_OK)
    
    # Use FeatureViewSet with feature_id__in filtering
    view = FeatureViewSet.as_view({"get": "list"})
    
    # Create GET request with feature ID filtering
    from django.test import RequestFactory
    factory = RequestFactory()
    get_request = factory.get(
        f'/features/?feature_id__in={",".join(feature_ids)}',
        HTTP_HOST=request.META.get('HTTP_HOST', 'localhost')
    )
    
    response = view(get_request)
    
    # Return results from FeatureViewSet
    if hasattr(response, 'data') and isinstance(response.data, dict) and 'results' in response.data:
        return Response(response.data['results'])
    else:
        return Response(response.data if hasattr(response, 'data') else [])





@api_view(["GET"])
def user_api(request):
    """User API"""
    try:
        current_only = request.GET.get("current_only")
        
        if current_only == "1":
            if request.user.is_authenticated:
                return Response([{
                    "id": request.user.id,
                    "username": request.user.username,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                    "email": request.user.email,
                }])
            else:
                # Return demo user data for unauthenticated requests
                return Response([{
                    "id": 1,
                    "username": "demo_user",
                    "first_name": "Demo",
                    "last_name": "User",
                    "email": "demo@example.com",
                }])
        else:
            return Response([])
            
    except Exception as e:
        return Response(
            {"error": f"Failed to fetch user data: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def api_root(request):
    """API root endpoint that resdk expects."""
    return Response({
        "version": "1.0",
        "description": "DictyExpress Resolwe API",
        "endpoints": {
            "data": "/api/data/",
            "process": "/api/process/",
            "user": "/api/user/",
        }
    })


@api_view(["GET"])
def resdk_version(request):
    """Return the minimal supported resdk version."""
    return Response({
        "version": "1.0.0"
    })

