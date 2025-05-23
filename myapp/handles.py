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

class CustomPagination(PageNumberPagination):
    page_size = 10  # Valor por defecto
    page_size_query_param = 'page_size'  # Permite que el cliente lo cambie
    max_page_size = 50  # Valor máximo permitido

    def get_page_size(self, request):
        try:
            page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))
            if page_size in [10, 25, 50]:
                return page_size
            return self.page_size  # Valor por defecto si no está en los permitidos
        except:
            return self.page_size


def getAllHandle(request, modelData, serializer_class):
    try:
        queryset = modelData.objects.all()

        search_query = request.query_params.get('search', None)
        if search_query:
            query = Q()
            for field in modelData._meta.get_fields():
                if hasattr(field, 'get_internal_type') and field.get_internal_type() in ['CharField', 'TextField']:
                    query |= Q(**{f"{field.name}__icontains": search_query})
            queryset = queryset.filter(query)

        filters = {}
        for key, value in request.query_params.items():
            if hasattr(modelData, key):
                filters[f"{key}__icontains"] = value
        if filters:
            queryset = queryset.filter(**filters)

        sort_by = request.query_params.get('sort_by', 'id')
        if hasattr(modelData, sort_by.lstrip('-')):
            queryset = queryset.order_by(sort_by)

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
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
        queryset = modelData.objects.all()

        # Search filter
        search_query = request.query_params.get('search', None)
        if search_query:
            query = Q()
            for field in modelData._meta.get_fields():
                if hasattr(field, 'get_internal_type'):
                    field_type = field.get_internal_type()
                    if field_type in ['CharField', 'TextField']:
                        query |= Q(**{f"{field.name}__icontains": search_query})
                    elif field_type == 'ForeignKey':
                        related_model = field.related_model
                        for related_field in related_model._meta.get_fields():
                            if hasattr(related_field, 'get_internal_type') and related_field.get_internal_type() in ['CharField', 'TextField']:
                                query |= Q(**{f"{field.name}__{related_field.name}__icontains": search_query})
            queryset = queryset.filter(query)

        # Filter by custom parameters
        filters = {}
        for key, value in request.query_params.items():
            if key == "search" or key == "page" or key == "sort_by":
                continue
            elif key == "periodo":
                # Traduce 'periodo' a 'periodoFk__PeriodoNombre'
                filters["periodoFk__PeriodoNombre"] = value
            else:
                filters[key] = value  # permite filtros directos y anidados (campo__subcampo)

        if filters:
            queryset = queryset.filter(**filters)

        # Sort
        sort_by = request.query_params.get('sort_by', 'ADIDcodigo')
        if hasattr(modelData, sort_by.lstrip('-')):
            queryset = queryset.order_by(sort_by)

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 30
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
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