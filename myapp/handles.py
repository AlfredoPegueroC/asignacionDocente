from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, ForeignKey, OneToOneField, ManyToManyField
from django.db.models.fields.related import ForeignKey

from django.db.models import Q, Value as V, CharField
from django.db.models.functions import Concat, Lower, Coalesce
from django.core.exceptions import FieldError


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
    max_page_size = 100  # Valor máximo permitido

    def get_page_size(self, request):
        try:
            page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))
            if page_size in [10, 25, 50, 75, 100]:
                return page_size
            return self.page_size  # Valor por defecto si no está en los permitidos
        except:
            return self.page_size


def getAllHandle(request, modelData, serializer_class):
    try:
        queryset = modelData.objects.all()

        # Diccionario de columnas que deben ir siempre ordenadas alfabéticamente
        # Clave = nombre del modelo o tabla / Valor = lista de campos a ordenar
        alphabetical_fields = {
            "Universidad": ["UniversidadNombre"],
            "Facultad": ["FacultadNombre"],
            "Escuela": ["EscuelaNombre"],
            "Docente": ["DocenteNombre", "DocenteApellido"],
            "Campus": ["CampusNombre"],
            "Asignatura": ["AsignaturaNombre"],
            "Periodo": ["PeriodoNombre"],
            "CategoriaDocente": ["CategoriaNombre"],
            "TipoDocenteDescripcion": ["TipoDocenteDescripcion"],
        }

        # Detectar relaciones (igual que antes)
        select_related_fields = []
        prefetch_related_fields = []
        for field in modelData._meta.get_fields():
            if isinstance(field, (ForeignKey, OneToOneField)):
                select_related_fields.append(field.name)
            elif isinstance(field, ManyToManyField) or field.auto_created:
                prefetch_related_fields.append(field.name)

        if select_related_fields:
            queryset = queryset.select_related(*select_related_fields)
        if prefetch_related_fields:
            queryset = queryset.prefetch_related(*prefetch_related_fields)

        # Filtro búsqueda (igual)
        search_query = request.query_params.get("search", None)
        if search_query:
            query = Q()
            for field in modelData._meta.get_fields():
                if hasattr(field, "get_internal_type") and field.get_internal_type() in ["CharField", "TextField"]:
                    query |= Q(**{f"{field.name}__icontains": search_query})
                elif isinstance(field, (ForeignKey, OneToOneField)):
                    related_model = field.related_model
                    for rel_field in related_model._meta.get_fields():
                        if hasattr(rel_field, "get_internal_type") and rel_field.get_internal_type() in ["CharField", "TextField"]:
                            query |= Q(**{f"{field.name}__{rel_field.name}__icontains": search_query})
            queryset = queryset.filter(query)

        # Filtros dinámicos simples
        filters = {}
        for key, value in request.query_params.items():
            if hasattr(modelData, key):
                filters[f"{key}__icontains"] = value
        if filters:
            queryset = queryset.filter(**filters)

        # Ordenamiento (aquí se agrega la lógica del diccionario)
        sort_by = request.query_params.get("sort_by", "id")
        if hasattr(modelData, sort_by.lstrip("-")):
            queryset = queryset.order_by(sort_by)
        else:
            # Si el modelo tiene campos definidos para orden alfabético, úsalos
            model_name = modelData.__name__
            if model_name in alphabetical_fields:
                queryset = queryset.order_by(*alphabetical_fields[model_name])

        # Paginación
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialización
        serializer = serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def getAll(request, modelData, serializer_class):
    try:
        # Obtener nombres de campos ForeignKey del modelo
        foreign_keys = [
            field.name
            for field in modelData._meta.fields
            if isinstance(field, ForeignKey)
        ]

        # Queryset base con select_related
        queryset = modelData.objects.select_related(*foreign_keys).all()

        # Aplicar filtros dinámicos: cualquier query param que coincida con un campo
        for param, value in request.GET.items():
            # Solo filtra si el modelo tiene ese campo (case-insensitive)
            if param in [f.name for f in modelData._meta.fields]:
                queryset = queryset.filter(**{param: value})

        # Serializar los datos
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def getAllHandle_asignacion(request, modelData, serializer_class):
    try:
        queryset = modelData.objects.select_related(
            'docenteFk', 'campusFk', 'universidadFk', 'facultadFk', 'escuelaFk', 'periodoFk'
        ).all()

        # --- Búsqueda global ---
        search_query = request.query_params.get('search')
        if search_query:
            query = Q()
            terms = search_query.split()
            for term in terms:
                term_q = Q()
                for field in modelData._meta.get_fields():
                    if hasattr(field, 'get_internal_type'):
                        t = field.get_internal_type()
                        if t in ['CharField', 'TextField']:
                            term_q |= Q(**{f"{field.name}__icontains": term})
                        elif t == 'ForeignKey':
                            rel_model = field.related_model
                            for rel_field in rel_model._meta.get_fields():
                                if hasattr(rel_field, 'get_internal_type') and rel_field.get_internal_type() in ['CharField', 'TextField']:
                                    term_q |= Q(**{f"{field.name}__{rel_field.name}__icontains": term})
                query &= term_q
            queryset = queryset.filter(query)

        # --- Filtros dinámicos ---
        filters = {}
        for key, value in request.query_params.items():
            if key in ["search", "page", "sort_by", "page_size"]:
                continue
            elif key == "periodo":
                filters["periodoFk__PeriodoNombre"] = value
            else:
                filters[key] = value
        if filters:
            queryset = queryset.filter(**filters)

        # --- Orden estable: por docente + desempates ---
        sort_by = (request.query_params.get('sort_by') or '').strip()

        # Si piden explícitamente docenteNombre (o nada), orden agrupado y estable:
        if sort_by in ('', 'docenteNombre', '-docenteNombre'):
            desc = (sort_by == '-docenteNombre')

            queryset = queryset.annotate(
                _docenteNombre_sort=Lower(
                    Concat(
                        Coalesce('docenteFk__DocenteNombre', V('')),
                        V(' '),
                        Coalesce('docenteFk__DocenteApellido', V('')),
                        output_field=CharField(),
                    )
                )
            ).order_by(
                '-_docenteNombre_sort' if desc else '_docenteNombre_sort',
                # Desempates dentro del mismo docente:
                '-nombre' if desc else 'nombre',
                '-seccion' if desc else 'seccion',
                '-nrc' if desc else 'nrc',
                # Tie-breaker final y único:
                '-AsignacionID' if desc else 'AsignacionID',
            )
        else:
            # Cualquier otro sort_by se respeta pero con tie-breaker estable
            try:
                queryset = queryset.order_by(
                    sort_by,
                    'AsignacionID' if not sort_by.startswith('-') else '-AsignacionID'
                )
            except FieldError:
                queryset = queryset.order_by('AsignacionID')

        # --- Paginación + Serialización ---
        paginator = CustomPagination()
        page_qs = paginator.paginate_queryset(queryset, request)
        serializer = serializer_class(page_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def updateHandle(request, modelData, serializerClass, pk):
    try:
        instance = get_object_or_404(modelData, pk=pk)
        partial = request.method == 'PATCH'
        serializer = serializerClass(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Esto ayuda a depurar si algo falla
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def deleteHandler(request, pk, modelData):
    try:
        deleteItem= modelData.objects.get(pk=pk)
        deleteItem.delete()  #
        return Response(status=status.HTTP_204_NO_CONTENT)
    except modelData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

def testhandler(request):
    return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)