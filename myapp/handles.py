from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

def createHandle(request, serializers):
    serializer = serializers(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"error": "Este registro ya existe."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def getAllHandle(request, modelData, serializer_class):
    
    try:
        # Fetch all objects
        queryset = modelData.objects.all() 

        # Search filter (optional)
        search_query = request.query_params.get('search', None)
        if search_query:
            # Create a dynamic query to search across all fields, but only text fields
            query = Q()
            for field in modelData._meta.get_fields():
                # Check if the field is a text-based field (CharField, TextField, etc.)
                if hasattr(field, 'get_internal_type') and field.get_internal_type() in ['CharField', 'TextField']:
                    query |= Q(**{f"{field.name}__icontains": search_query})
            queryset = queryset.filter(query)

        # Filter by other query parameters (example: name, state)
        filters = {}
        for key, value in request.query_params.items():
            if hasattr(modelData, key):  # Ensure the filter key exists in the model
                filters[f"{key}__icontains"] = value  # Case-insensitive contains filter
        if filters:
            queryset = queryset.filter(**filters)

        # Sort by a field (default is "id")
        sort_by = request.query_params.get('sort_by', 'id')
        if hasattr(modelData, sort_by.lstrip('-')):
            queryset = queryset.order_by(sort_by)

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 30  # Default items per page
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialize paginated data
        serializer = serializer_class(paginated_queryset, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
        
    except Exception as e:
        # Handle exceptions (e.g., database errors)
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



def getAll(request, modelData, serializer_class):
    try:
        # Fetch all objects
        queryset = modelData.objects.all()

        # Serialize data
        serializer = serializer_class(queryset, many=True)

        # Return response with serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions (e.g., database errors)
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def getAllHandle_asignacion(request, modelData, serializer_class):
    try:
        # Fetch all objects
        queryset = modelData.objects.all()

        # Search filter (optional)
        search_query = request.query_params.get('search', None)
        if search_query:
            query = Q()
            # Loop over the fields of the model
            for field in modelData._meta.get_fields():
                if hasattr(field, 'get_internal_type'):
                    field_type = field.get_internal_type()
                    if field_type in ['CharField', 'TextField']:  # Only consider CharField and TextField
                        query |= Q(**{f"{field.name}__icontains": search_query})
                    elif field_type == 'ForeignKey':  # Handle ForeignKey fields
                        related_model = field.related_model
                        # Search by related field's text fields (e.g., `nombre` or `apellidos` for `Docente`)
                        for related_field in related_model._meta.get_fields():
                            if hasattr(related_field, 'get_internal_type') and related_field.get_internal_type() in ['CharField', 'TextField']:
                                query |= Q(**{f"{field.name}__{related_field.name}__icontains": search_query})
            queryset = queryset.filter(query)

        # Filter by other query parameters (e.g., name, state)
        filters = {}
        for key, value in request.query_params.items():
            if hasattr(modelData, key):  # Ensure the filter key exists in the model
                filters[f"{key}__icontains"] = value  # Case-insensitive contains filter
        if filters:
            queryset = queryset.filter(**filters)

        # Sort by a field (default is "id")
        sort_by = request.query_params.get('sort_by', 'ADIDcodigo')
        if hasattr(modelData, sort_by.lstrip('-')):  # Ensure sort field exists in the model
            queryset = queryset.order_by(sort_by)

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 30  # Default items per page
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialize paginated data
        serializer = serializer_class(paginated_queryset, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        # Handle exceptions (e.g., database errors)
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
def updateHandle(request, modelData, serializers, pk):
    try:
        universidad = modelData.objects.get(pk=pk)
    except modelData.DoesNotExist:
        return JsonResponse({'error': 'Universidad not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH']:
        ser = serializers(universidad, data=request.data, partial=(request.method == 'PATCH'))
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=status.HTTP_200_OK)
        return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

def deleteHandler(request, pk, modelData):
    try:
        deleteItem= modelData.objects.get(pk=pk)
        deleteItem.delete()  #
        return Response(status=status.HTTP_204_NO_CONTENT)
    except modelData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

def testhandler(request):
    return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)