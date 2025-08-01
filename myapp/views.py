
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .serializer import (
  UniversidadSerializer, 
  CampusSerializer,
  FacultadSerializer, 
  EscuelaSerializer,
  TipoDocenteSerializer,
  CategoriaDocenteSerializer,
  DocenteSerializer,
  PeriodoAcademicoSerializer,
  AsignacionDocenteSerializer,
  AsignacionDocenteSerializer_frontend,
  UserSerializer,
  RegistroUsuarioSerializer,
  APILogSerializer
)
from .models import (
    Universidad, 
    Campus,
    Facultad, 
    Escuela,  
    TipoDocente,
    CategoriaDocente, 
    Docente, 
    PeriodoAcademico,
    AsignacionDocente,
    APILog
    )
from .handles import createHandle, getAllHandle, deleteHandler,getAllHandle_asignacion, getAll, updateHandle
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
import pandas as pd
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from django.shortcuts import redirect
from datetime import datetime

# Create your views here.
def index(request):
    return redirect('/admin/')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vista_protegida(request):
    return Response({"mensaje": f"Hola {request.user.username}, estás autenticado"})

class CustomUserPagination(PageNumberPagination):
    page_size = 10  # Valor por defecto
    page_size_query_param = 'page_size'  # Permite usar ?page_size=25 o 50 desde el frontend
    max_page_size = 100
    allowed_page_sizes = [10, 25, 50, 100]  # Tamaños de página permitidos


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = CustomUserPagination
    permission_classes = [IsAuthenticated]



# @permission_classes([AllowAny])
# class UserListView(APIView):
    
    def get(self, request):
        try:
            users = User.objects.all()
            paginator = CustomUserPagination()
            paginated_users = paginator.paginate_queryset(users, request)
            serializer = UserSerializer(paginated_users, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class RegistroUsuarioAPI(APIView):
#     def post(self, request):
#         try:
#             serializer = RegistroUsuarioSerializer(data=request.data)
#             if serializer.is_valid():
#                 user = serializer.save()
#                 return Response({
#                     "id": user.id,
#                     "username": user.username,
#                     "email": user.email,
#                     "first_name": user.first_name,
#                     "last_name": user.last_name,
#                     "is_staff": user.is_staff,
#                     "is_active": user.is_active,
#                     "groups": [group.name for group in user.groups.all()]
#                 }, status=201)
#             return Response(serializer.errors, status=400)
#         except Exception as e:
#             print("❌ Error en el registro:", str(e))
#             return Response({'error': str(e)}, status=500)

# @permission_classes([AllowAny])
# class EditarUsuarioAPI(APIView):
#     def patch(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk)

#             # No forzamos nada, usamos los datos que vienen del request
#             serializer = RegistroUsuarioSerializer(user, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=200)
#             return Response(serializer.errors, status=400)
#         except User.DoesNotExist:
#             return Response({"error": "Usuario no encontrado"}, status=404)
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)
        
class LogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    allowed_page_sizes = [10, 25, 50]

    def get_page_size(self, request):
        try:
            page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))
        except (TypeError, ValueError):
            page_size = self.page_size

        if page_size not in self.allowed_page_sizes:
            raise NotFound(detail=f"page_size debe ser uno de {self.allowed_page_sizes}")

        return page_size

@permission_classes([IsAuthenticated])
class APILogList(ListAPIView):
    queryset = APILog.objects.all().order_by('-timestamp')
    serializer_class = APILogSerializer
    pagination_class = LogPagination
    filter_backends = [SearchFilter]
    search_fields = ['user__username', 'path', 'method']

# HERE IS ALL THE ENDPOINTS OF THE API

#region CREATE

@api_view(['POST'])
def create_Universidad(request):
  return createHandle(request, UniversidadSerializer)

@api_view(['POST'])
def create_Campus(request):
  return createHandle(request, CampusSerializer)

@api_view(['POST'])
def create_Facultad(request):
  return createHandle(request, FacultadSerializer)

@api_view(['POST'])
def create_Escuela(request):
  return createHandle(request ,EscuelaSerializer)

@api_view(['POST'])
def create_TipoDocente(request):
  return createHandle(request, TipoDocenteSerializer)


@api_view(['POST'])
def create_CategoriaDocente(request):
  return createHandle(request, CategoriaDocenteSerializer)

@api_view(['POST'])
def create_Docente(request):
  return createHandle(request, DocenteSerializer)

@api_view(['POST'])
def create_PeriodoAcademico(request):
  return createHandle(request, PeriodoAcademicoSerializer)

@api_view(['POST'])
def create_asignacion(request):
  return createHandle(request, AsignacionDocenteSerializer)
#endregion

#region RETRIEVE OR READ
@api_view(['GET'])
@permission_classes([AllowAny])
def getAllUniversidad(request):
  return getAllHandle(request, Universidad, UniversidadSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllCampus(request):
    return getAllHandle(request, Campus, CampusSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllFacultad(request):
  return getAllHandle(request, Facultad, FacultadSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllEscuela(request):
  return getAllHandle(request, Escuela, EscuelaSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllTipoDocente(request):
  return getAllHandle(request, TipoDocente, TipoDocenteSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllCategoriaDocente(request):
  return getAllHandle(request, CategoriaDocente, CategoriaDocenteSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllDocente(request):
  return getAllHandle(request, Docente, DocenteSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllPeriodoAcademico(request):
  return getAllHandle(request, PeriodoAcademico, PeriodoAcademicoSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllAsignacion(request):
  return getAllHandle_asignacion(request, AsignacionDocente, AsignacionDocenteSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllAsignacion_frontend(request):
  return getAllHandle_asignacion(request,AsignacionDocente,AsignacionDocenteSerializer_frontend)



# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_Universidad(request):
#     return getAll(request, Universidad, UniversidadSerializer)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_Universidad(request):
    try:
        search = request.GET.get("search", "").strip()
        limit = int(request.GET.get("limit", 50))  # Límite configurable
        offset = int(request.GET.get("offset", 0))  # Soporte para paginación

        # Optimización con only
        queryset = Universidad.objects.only("UniversidadID", "UniversidadNombre")

        if search:
            queryset = queryset.filter(
                Q(UniversidadNombre__icontains=search)
            )

        total = queryset.count()  # Total antes de paginar
        queryset = queryset[offset:offset + limit]

        serializer = UniversidadSerializer(queryset, many=True)
        return Response({
            "results": serializer.data,
            "total": total
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(['GET'])
@permission_classes([AllowAny])
def get_Campus(request):
    return getAll(request, Campus, CampusSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_Facultad(request):
    return getAll(request, Facultad, FacultadSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_Escuela(request):
    return getAll(request, Escuela, EscuelaSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_TipoDocente(request):
    return getAll(request, TipoDocente, TipoDocenteSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_CategoriaDocente(request):
    return getAll(request, CategoriaDocente, CategoriaDocenteSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_Docente(request):
    return getAll(request, Docente, DocenteSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_PeriodoAcademico(request):
    return getAll(request, PeriodoAcademico, PeriodoAcademicoSerializer)
#endregion


#region UPDATE


@api_view(['PUT', 'PATCH'])
def update_universidad(request, codigo):
    try:
        universidad = Universidad.objects.get(UniversidadCodigo=codigo)
    except Universidad.DoesNotExist:
        return JsonResponse({'error': 'Universidad not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH']:
        ser = UniversidadSerializer(universidad, data=request.data, partial=(request.method == 'PATCH'))
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=status.HTTP_200_OK)
        return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])
@api_view(['PUT', 'PATCH'])
def update_campus(request, codigo):
    try:
        campus = Campus.objects.get(CampusCodigo=codigo)
    except Campus.DoesNotExist:
        return JsonResponse({'error': 'Campus not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method in ['PUT', 'PATCH']:
        ser = CampusSerializer(campus, data=request.data, partial=(request.method == 'PATCH'))
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=status.HTTP_200_OK)
        return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])
@api_view(['PUT', 'PATCH'])
def update_facultad(request, codigo):
  try:
    facultad = Facultad.objects.get(FacultadCodigo=codigo)
  except Facultad.DoesNotExist:
    return JsonResponse({'error': 'Facultad not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = FacultadSerializer(facultad, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_escuela(request, codigo):
  try:
    escuela = Escuela.objects.get(EscuelaCodigo=codigo)
  except Escuela.DoesNotExist:
    return JsonResponse({'error': 'Escuela not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = EscuelaSerializer(escuela, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_tipoDocente(request, codigo):
  try:
    tipoDocente = TipoDocente.objects.get(TipoDocenteCodigo=codigo)
  except TipoDocente.DoesNotExist:
    return JsonResponse({'error': 'Tipo docente not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = TipoDocenteSerializer(tipoDocente, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_categoriaDocente(request, codigo):
  try:
    categoriaDocente = CategoriaDocente.objects.get(categoriaCodigo=codigo)
  except CategoriaDocente.DoesNotExist:
    return JsonResponse({'error': 'Categoria docente not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = CategoriaDocenteSerializer(categoriaDocente, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_docente(request, codigo):
  try:
    docente = Docente.objects.get(DocenteCodigo=codigo)
  except Docente.DoesNotExist:
    return JsonResponse({'error': 'Tipo docente not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = DocenteSerializer(docente, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_periodoAcademico(request, codigo):
  try:
    periodo = PeriodoAcademico.objects.get(PeriodoCodigo=codigo)
  except PeriodoAcademico.DoesNotExist:
    return JsonResponse({'error': 'Periodo academico not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = PeriodoAcademicoSerializer(periodo, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_asignacion(request, pk):
    try:
        asignacion = AsignacionDocente.objects.get(pk=pk)
    except AsignacionDocente.DoesNotExist:
        return JsonResponse({'error': "Asignacion Docente No encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH']:
        # Exclude 'docente_nombre_completo' from the request data (since it's read-only)
        request_data = request.data.copy()
        request_data.pop('docente_nombre_completo', None)  # Remove 'docente_nombre_completo' if it exists

        ser = AsignacionDocenteSerializer(asignacion, data=request_data, partial=(request.method == 'PATCH'))

        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=status.HTTP_200_OK)
        return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)


#endregion

#region DELETE
@api_view(['DELETE'])
def delete_universidad(request, pk):
    try:
        universidad = Universidad.objects.get(pk=pk)
        universidad.delete()  # Delete the specific university
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Universidad.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_facultad(request, pk):
    try:
        facultad = Facultad.objects.get(pk=pk)
        facultad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Facultad.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_escuela(request, pk):
    try:
        escuela = Escuela.objects.get(pk=pk)
        escuela.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Escuela.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_tipoDocente(request, pk):
    try:
        tipoDocente = TipoDocente.objects.get(pk=pk)
        tipoDocente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except TipoDocente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_categoriaDocente(request, pk):
    try:
        categoriaDocente = CategoriaDocente.objects.get(pk=pk)
        categoriaDocente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except CategoriaDocente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_docente(request, pk):
    try:
        docente = Docente.objects.get(pk=pk)
        docente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Docente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_periodoAcademico(request, pk):
    try:
        periodo = PeriodoAcademico.objects.get(pk=pk)
        periodo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except PeriodoAcademico.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_asignacionDocente(request, pk):
    try:
        asignacion = AsignacionDocente.objects.get(pk=pk)
        asignacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except AsignacionDocente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_asignacion_by_period(request):
    period = request.GET.get('period')
    if not period:
        return Response({"error": "Missing period"}, status=status.HTTP_400_BAD_REQUEST)
    deleted_count, _ = AsignacionDocente.objects.filter(period=period).delete()
    
    if deleted_count == 0:
        return Response({"error": "No records found"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"message": "Records deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_campus(request, pk):
    try:
        campus = Campus.objects.get(pk=pk)
        campus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Campus.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

#endregion

#region DETAILTS


@permission_classes([AllowAny])
@api_view(['GET'])
def details_universidad(request, codigo):
    universidad = Universidad.objects.filter(UniversidadCodigo=codigo).first()

    if universidad is None:
        return Response({'error': 'Universidad not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UniversidadSerializer(universidad)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_campus(request, codigo):
    campus = Campus.objects.filter(CampusCodigo=codigo).first()
    if campus is None:
        return Response({'error': 'Campus not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CampusSerializer(campus)
    return Response(serializer.data)


@api_view(['GET'])
def details_facultad(request, codigo):
    facultad = Facultad.objects.filter(FacultadCodigo=codigo).first()
    if facultad is None:
        return Response({'error': 'Facultad not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = FacultadSerializer(facultad)

    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
def details_escuela(request, codigo):
    escuela = Escuela.objects.filter(EscuelaCodigo=codigo).first()
    if escuela is None:
        return Response({'error': 'Escuela not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EscuelaSerializer(escuela)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_tipoDocente(request, codigo):
    tipoDocente = TipoDocente.objects.filter(TipoDocenteCodigo=codigo).first()
    if tipoDocente is None:
        return Response({'error': 'Tipo docente not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TipoDocenteSerializer(tipoDocente)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_categoriaDocente(request, codigo):
    categoriaDocente = CategoriaDocente.objects.filter(categoriaCodigo=codigo).first()
    if categoriaDocente is None:
        return Response({'error': 'Categoria docente not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CategoriaDocenteSerializer(categoriaDocente)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_docente(request, codigo):
    docente = Docente.objects.filter(DocenteCodigo=codigo).first()
    if docente is None:
        return Response({'error': 'Docente not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DocenteSerializer(docente)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_periodoAcademico(request, codigo):
    periodo = PeriodoAcademico.objects.filter(PeriodoCodigo=codigo).first()
    if periodo is None:
        return Response({'error': 'Periodo academico not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PeriodoAcademicoSerializer(periodo)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_Asignacion(request, pk):
    asignacion = AsignacionDocente.objects.filter(pk=pk).first()
    if asignacion is None:
        return Response({'error': 'Asignacion not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = AsignacionDocenteSerializer(asignacion)

    return Response(serializer.data, status=status.HTTP_200_OK)
#endregion

#region Auth
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        # Retrieve the refresh token from the request data
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the RefreshToken instance and blacklist it
        token = RefreshToken(refresh_token)
        token.blacklist()  # This will invalidate the token
        
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    
    except TokenError as e:  # Handles invalid or expired token
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#endregion

#region export


# CAMBIAR PARA QUE SEA NECESARIO LA AUTORIZACION PARA EXPORTAR
@api_view(["GET"])
@permission_classes([AllowAny])
def UniversidadExport(request):
    queryset = Universidad.objects.all()
    data = []

    for universidad in queryset:
        data.append({
            'Codigo': universidad.UniversidadCodigo,
            'Nombre': universidad.UniversidadNombre,
            'Direccion': universidad.UniversidadDireccion,
            'Telefono': universidad.UniversidadTelefono,
            'Email': universidad.UniversidadEmail,
            'Sitio Web': universidad.UniversidadSitioWeb,
            'Rector': universidad.UniversidadRector,
        })

    columns = [
        'Codigo',
        'Nombre',
        'Direccion',
        'Telefono',
        'Email',
        'Sitio Web',
        'Rector',
    ]

    df = pd.DataFrame(data, columns=columns)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato: 2025-07-22
    filename = f"universidades_{fecha_actual}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Universidades', index=False)

    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def CampusExport(request):
    queryset = Campus.objects.select_related("Campus_UniversidadFK").all()
    data = []

    for campus in queryset:
        data.append({
            "Codigo": campus.CampusCodigo,
            "Nombre": campus.CampusNombre,
            "Direccion": campus.CampusDireccion,
            "Pais": campus.CampusPais,
            "Provincia": campus.CampusProvincia,
            "Ciudad": campus.CampusCiudad,
            "Telefono": campus.CampusTelefono,
            "Correo Contacto": campus.CampusCorreoContacto,
            "Universidad": campus.Campus_UniversidadFK.UniversidadNombre if campus.Campus_UniversidadFK else "---",
        })

    columns = [
        "Codigo",
        "Nombre",
        "Direccion",
        "Pais",
        "Provincia",
        "Ciudad",
        "Telefono",
        "Correo Contacto",
        "Universidad"
    ]

    df = pd.DataFrame(data, columns=columns)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato: 2025-07-22
    filename = f"campus_{fecha_actual}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'



    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Campus', index=False)

    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def FacultadExport(request):
    queryset = Facultad.objects.select_related("Facultad_UniversidadFK", "Facultad_CampusFK").all()
    data = []

    for facultad in queryset:
        data.append({
            "Codigo": facultad.FacultadCodigo,
            "Nombre": facultad.FacultadNombre,
            "Decano": facultad.FacultadDecano,
            "Direccion": facultad.FacultadDireccion,
            "Telefono": facultad.FacultadTelefono,
            "Email": facultad.FacultadEmail,
            "Universidad": facultad.Facultad_UniversidadFK.UniversidadNombre if facultad.Facultad_UniversidadFK else "—",
            "Campus": facultad.Facultad_CampusFK.CampusNombre if facultad.Facultad_CampusFK else "—",
        })

    columns = [
        "Codigo",
        "Nombre",
        "Decano",
        "Direccion",
        "Telefono",
        "Email",
        "Universidad",
        "Campus"
    ]

    df = pd.DataFrame(data, columns=columns)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato: 2025-07-22
    filename = f"facultades_{fecha_actual}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Facultades', index=False)

    return response



@api_view(["GET"])
@permission_classes([AllowAny])
def EscuelaExport(request):
    queryset = Escuela.objects.select_related("Escuela_UniversidadFK", "Escuela_facultadFK").all()
    data = []

    for escuela in queryset:
        data.append({
            'Codigo': escuela.EscuelaCodigo,
            'Nombre': escuela.EscuelaNombre,
            'Directora': escuela.EscuelaDirectora,
            'Telefono': escuela.EscuelaTelefono,
            'Correo': escuela.EscuelaCorreo,
            'Universidad': escuela.Escuela_UniversidadFK.UniversidadNombre if escuela.Escuela_UniversidadFK else "—",
            'Facultad': escuela.Escuela_facultadFK.FacultadNombre if escuela.Escuela_facultadFK else "—",
        })

    columns = [
        'Codigo',
        'Nombre',
        'Directora',
        'Telefono',
        'Correo',
        'Universidad',
        'Facultad',
    ]

    df = pd.DataFrame(data, columns=columns)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato: 2025-07-22
    filename = f"escuelas_{fecha_actual}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Escuelas', index=False)

    return response

@api_view(["GET"])
@permission_classes([AllowAny])
def DocenteExport(request):
    queryset = Docente.objects.select_related(
        "Docente_UniversidadFK",
        "Docente_TipoDocenteFK",
        "Docente_CategoriaDocenteFK"
    ).all()

    data = []

    for d in queryset:
        data.append({
            "Codigo": d.DocenteCodigo,
            "Nombre": d.DocenteNombre,
            "Apellido": d.DocenteApellido,
            "Sexo": d.DocenteSexo,
            "EstadoCivil": d.DocenteEstadoCivil,
            "FechaNacimiento": d.DocenteFechaNacimiento,
            "LugarNacimiento": d.DocenteLugarNacimiento,
            "FechaIngreso": d.DocenteFechaIngreso,
            "Nacionalidad": d.DocenteNacionalidad,
            "TipoIdentificacion": d.DocenteTipoIdentificacion,
            "NumeroIdentificacion": d.DocenteNumeroIdentificacion,
            "Telefono": d.DocenteTelefono,
            "CorreoElectronico": d.DocenteCorreoElectronico,
            "Direccion": d.DocenteDireccion,
            "Observaciones": d.DocenteObservaciones,
            "Universidad": d.Docente_UniversidadFK.UniversidadNombre if d.Docente_UniversidadFK else "",
            "TipoDocente": d.Docente_TipoDocenteFK.TipoDocenteDescripcion if d.Docente_TipoDocenteFK else "",
            "CategoriaDocente": d.Docente_CategoriaDocenteFK.CategoriaNombre if d.Docente_CategoriaDocenteFK else "",
        })

    columns = [
        "Codigo",
        "Nombre",
        "Apellido",
        "Sexo",
        "EstadoCivil",
        "FechaNacimiento",
        "LugarNacimiento",
        "FechaIngreso",
        "Nacionalidad",
        "TipoIdentificacion",
        "NumeroIdentificacion",
        "Telefono",
        "CorreoElectronico",
        "Direccion",
        "Observaciones",
        "Universidad",
        "TipoDocente",
        "CategoriaDocente"
    ]

    df = pd.DataFrame(data, columns=columns)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato: 2025-07-22
    filename = f"docentes_{fecha_actual}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Docentes', index=False)

    return response

@api_view(["GET"])
@permission_classes([AllowAny])
def CategoriaDocenteExport(request):
    try:
        queryset = CategoriaDocente.objects.select_related("Categoria_UniversidadFK").all()
        data = []

        for categoria in queryset:
            data.append({
                'Codigo': categoria.categoriaCodigo,
                'Nombre': categoria.CategoriaNombre,
                'Universidad': categoria.Categoria_UniversidadFK.UniversidadNombre if categoria.Categoria_UniversidadFK else "—"
            })

        columns = ['Codigo', 'Nombre', 'Universidad']
        df = pd.DataFrame(data, columns=columns)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"categoria_docente_{fecha_hora}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Categorías', index=False)

        return response

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    
@api_view(["GET"])
@permission_classes([AllowAny])
def TipoDocenteExport(request):
    queryset = TipoDocente.objects.select_related("TipoDocente_UniversidadFK").all()
    data = []

    for tipo in queryset:
        data.append({
            'Codigo': tipo.TipoDocenteCodigo,
            'Descripcion': tipo.TipoDocenteDescripcion,
            'Universidad': tipo.TipoDocente_UniversidadFK.UniversidadNombre if tipo.TipoDocente_UniversidadFK else '—'
        })

    columns = [
        'Codigo',
        'Descripcion',
        'Universidad',
    ]

    df = pd.DataFrame(data, columns=columns)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato: 2025-07-22
    filename = f"tipo_docente_{fecha_actual}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='TipoDocente', index=False)

    return response

@api_view(["GET"])
@permission_classes([AllowAny])
def PeriodoAcademicoExport(request):
    queryset = PeriodoAcademico.objects.select_related('Periodo_UniversidadFK').all()
    data = []

    for periodo in queryset:
        data.append({
            'ID': periodo.PeriodoID,
            'Código': periodo.PeriodoCodigo,
            'Nombre': periodo.PeriodoNombre,
            'Tipo': periodo.PeriodoTipo,
            'Año': periodo.PeriodoAnio,
            'Fecha Inicio': periodo.PeriodoFechaInicio,
            'Fecha Fin': periodo.PeriodoFechaFin,
            'Estado': periodo.PeriodoEstado,
            'Universidad Nombre': periodo.Periodo_UniversidadFK.UniversidadNombre if periodo.Periodo_UniversidadFK else ''
        })

    columns = [
        'ID',
        'Código',
        'Nombre',
        'Tipo',
        'Año',
        'Fecha Inicio',
        'Fecha Fin',
        'Estado',
        'Universidad Nombre'
    ]

    df = pd.DataFrame(data, columns=columns)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato: 2025-07-22
    filename = f"periodo_academico_{fecha_actual}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Periodos', index=False)

    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def asignacionDocenteExport(request):
    # Obtener el periodo desde la solicitud
    period = request.GET.get("period")

    # Obtener datos relacionados
    queryset = AsignacionDocente.objects.select_related(
        "facultadFk", "escuelaFk", "docenteFk", "campusFk"
    )

    # Filtrar por periodo si se proporciona
    if period:
        queryset = queryset.filter(periodoFk__PeriodoNombre=period)

    data = []

    for asignacion in queryset:
        data.append({
            "NRC": asignacion.nrc,
            "Clave": asignacion.clave,
            "Asignatura": asignacion.nombre,
            "Codigo": asignacion.codigo,
            "Profesor": f"{asignacion.docenteFk.DocenteNombre} {asignacion.docenteFk.DocenteApellido}" if asignacion.docenteFk else None,
            "Seccion": asignacion.seccion,
            "Modalidad": asignacion.modalidad,
            "Campus": asignacion.campusFk.CampusNombre if asignacion.campusFk else None,
            "Facultad": asignacion.facultadFk.FacultadNombre if asignacion.facultadFk else None,
            "Escuela": asignacion.escuelaFk.EscuelaNombre if asignacion.escuelaFk else None,
            "Tipo": asignacion.tipo,
            "Cupo": asignacion.cupo,
            "Inscripto": asignacion.inscripto,
            "Horario": asignacion.horario,
            "Dias": asignacion.dias,
            "Aula": asignacion.aula,
            "Creditos": asignacion.creditos,
        })

    columns = [
        "NRC",
        "Clave",
        "Asignatura",
        "Codigo",
        "Profesor",
        "Seccion",
        "Modalidad",
        "Campus",
        "Facultad",
        "Escuela",
        "Tipo",
        "Cupo",
        "Inscripto",
        "Horario",
        "Dias",
        "Aula",
        "Creditos",
    ]

    df = pd.DataFrame(data, columns=columns)

    # Crear respuesta en Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato: 2025-07-22
    filename = f'Asignacion_{period if period else "todos"}_{fecha_actual}.xlsx'
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Asignaciones", index=False)

    return response
#endregion

#region Import
class ImportEscuela(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No se envió ningún archivo Excel"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)
            df = df.dropna(how='all')  # Ignorar filas totalmente vacías

            required_columns = [
                'Codigo', 'Nombre', 'Directora', 'Telefono',
                'Correo', 'Universidad', 'Facultad'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas requeridas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()}
            facultades = {f.FacultadNombre.strip().lower(): f for f in Facultad.objects.all()}

            records_to_create = []
            failed_rows = []
            duplicated_rows = []
            duplicated_names = set()
            duplicated_directoras = set()

            # Precargar códigos existentes para evitar repetidos
            existing_codigos = set(Escuela.objects.values_list('EscuelaCodigo', flat=True))
            existing_nombres = set(Escuela.objects.values_list('EscuelaNombre', flat=True))
            existing_directoras = set(Escuela.objects.values_list('EscuelaDirectora', flat=True))

            for index, row in df.iterrows():
                fila = index + 2
                try:
                    codigo = str(row.get('Codigo', '')).strip()
                    nombre = str(row.get('Nombre', '')).strip()
                    directora = str(row.get('Directora', '')).strip()
                    telefono = str(row.get('Telefono', '')).strip()
                    correo = str(row.get('Correo', '')).strip()
                    universidad_nombre = str(row.get('Universidad', '')).strip().lower()
                    facultad_nombre = str(row.get('Facultad', '')).strip().lower()

                    # Validar campos vacíos
                    required_fields = {
                        "Codigo": codigo,
                        "Nombre": nombre,
                        "Directora": directora,
                        "Telefono": telefono,
                        "Correo": correo,
                        "Universidad": universidad_nombre,
                        "Facultad": facultad_nombre,
                    }

                    for field, value in required_fields.items():
                        if not value:
                            failed_rows.append(f"Fila {fila}: El campo '{field}' está vacío.")
                            raise ValueError("Campo vacío")

                    universidad = universidades.get(universidad_nombre)
                    facultad = facultades.get(facultad_nombre)

                    if not universidad:
                        failed_rows.append(f"Fila {fila}: Universidad '{row.get('Universidad')}' no encontrada.")
                        continue

                    if not facultad:
                        failed_rows.append(f"Fila {fila}: Facultad '{row.get('Facultad')}' no encontrada.")
                        continue

                    if codigo in existing_codigos:
                        duplicated_rows.append(f"Fila {fila}: El código '{codigo}' ya existe.")
                        continue
                    existing_codigos.add(codigo)

                    if nombre.lower() in (n.lower() for n in existing_nombres):
                        duplicated_rows.append(f"Fila {fila}: El nombre '{nombre}' ya existe.")
                        duplicated_names.add(nombre)
                        continue
                    existing_nombres.add(nombre)

                    if directora.lower() in (d.lower() for d in existing_directoras):
                        duplicated_rows.append(f"Fila {fila}: La directora '{directora}' ya existe.")
                        duplicated_directoras.add(directora)
                        continue
                    existing_directoras.add(directora)

                    escuela = Escuela(
                        EscuelaCodigo=codigo,
                        EscuelaNombre=nombre,
                        EscuelaDirectora=directora,
                        EscuelaTelefono=telefono,
                        EscuelaCorreo=correo,
                        EscuelaEstado='Activo',
                        Escuela_UniversidadFK=universidad,
                        Escuela_facultadFK=facultad,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(escuela)

                except ValueError:
                    continue
                except Exception as e:
                    failed_rows.append(f"Error inesperado en fila {fila}: {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Escuela.objects.bulk_create(records_to_create)

                return Response({
                    "message": f"{len(records_to_create)} escuelas importadas exitosamente. "
                               f"{len(duplicated_rows)} duplicados omitidos. "
                               f"{len(failed_rows)} filas fallaron.",
                    "errores": failed_rows,
                    "duplicados": duplicated_rows,
                    "nombres_duplicados": list(duplicated_names),
                    "directoras_duplicadas": list(duplicated_directoras)
                }, status=status.HTTP_201_CREATED)

            # Sin registros creados
            message = "No se importó ninguna escuela."
            if duplicated_rows and failed_rows:
                message += " Todos los registros eran duplicados o contenían errores."
            elif duplicated_rows:
                message += " Todos los registros eran duplicados."
            elif failed_rows:
                message += " Todos los registros tenían errores."
            else:
                message += " Causa desconocida."

            return Response({
                "message": message,
                "errores": failed_rows,
                "duplicados": duplicated_rows,
                "nombres_duplicados": list(duplicated_names),
                "directoras_duplicadas": list(duplicated_directoras)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            
class ImportDocente(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No se envió ningún archivo Excel"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)
            df = df.dropna(how='all')  # Eliminar filas vacías completas

            required_columns = [
                'Codigo', 'Nombre', 'Apellido', 'Sexo', 'EstadoCivil', 'FechaNacimiento',
                'LugarNacimiento', 'FechaIngreso', 'Nacionalidad', 'TipoIdentificacion',
                'NumeroIdentificacion', 'Telefono', 'CorreoElectronico', 'Direccion',
                'Observaciones', 'Universidad', 'TipoDocente', 'CategoriaDocente'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas requeridas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()}
            tipos_docente = {t.TipoDocenteDescripcion.strip().lower(): t for t in TipoDocente.objects.all()}
            categorias_docente = {c.CategoriaNombre.strip().lower(): c for c in CategoriaDocente.objects.all()}

            records_to_create = []
            failed_rows = []
            duplicated_rows = []

            # Precargar códigos existentes para evitar duplicados en batch
            existing_codigos = set(Docente.objects.values_list('DocenteCodigo', flat=True))

            for index, row in df.iterrows():
                fila = index + 2
                try:
                    # Limpiar y mapear datos
                    codigo = str(row.get('Codigo', '')).strip()
                    nombre = str(row.get('Nombre', '')).strip()
                    apellido = str(row.get('Apellido', '')).strip()
                    sexo = str(row.get('Sexo', '')).strip()
                    estado_civil = str(row.get('EstadoCivil', '')).strip()
                    fecha_nacimiento = pd.to_datetime(row.get('FechaNacimiento', ''), errors='coerce')
                    lugar_nacimiento = str(row.get('LugarNacimiento', '')).strip()
                    fecha_ingreso = pd.to_datetime(row.get('FechaIngreso', ''), errors='coerce')
                    nacionalidad = str(row.get('Nacionalidad', '')).strip()
                    tipo_id = str(row.get('TipoIdentificacion', '')).strip()
                    num_id = str(row.get('NumeroIdentificacion', '')).strip()
                    telefono = str(row.get('Telefono', '')).strip()
                    correo = str(row.get('CorreoElectronico', '')).strip()
                    direccion = str(row.get('Direccion', '')).strip()
                    observaciones = str(row.get('Observaciones', '')).strip() if pd.notna(row.get('Observaciones')) else ''
                    universidad_nombre = str(row.get('Universidad', '')).strip().lower()
                    tipo_nombre = str(row.get('TipoDocente', '')).strip().lower()
                    categoria_nombre = str(row.get('CategoriaDocente', '')).strip().lower()

                    # Validar campos requeridos vacíos
                    required_fields = {
                        "Codigo": codigo, "Nombre": nombre, "Apellido": apellido,
                        "Sexo": sexo, "EstadoCivil": estado_civil, "FechaNacimiento": fecha_nacimiento,
                        "LugarNacimiento": lugar_nacimiento, "FechaIngreso": fecha_ingreso,
                        "Nacionalidad": nacionalidad, "TipoIdentificacion": tipo_id,
                        "NumeroIdentificacion": num_id, "Telefono": telefono, "CorreoElectronico": correo,
                        "Direccion": direccion, "Universidad": universidad_nombre,
                        "TipoDocente": tipo_nombre, "CategoriaDocente": categoria_nombre
                    }

                    for field, value in required_fields.items():
                        if value in [None, ""] or (isinstance(value, float) and pd.isna(value)):
                            failed_rows.append(f"Fila {fila}: El campo '{field}' está vacío.")
                            raise ValueError("Campo vacío")

                    universidad = universidades.get(universidad_nombre)
                    tipo = tipos_docente.get(tipo_nombre)
                    categoria = categorias_docente.get(categoria_nombre)

                    if not universidad:
                        failed_rows.append(f"Fila {fila}: Universidad '{row.get('Universidad')}' no encontrada.")
                        continue
                    if not tipo:
                        failed_rows.append(f"Fila {fila}: TipoDocente '{row.get('TipoDocente')}' no encontrado.")
                        continue
                    if not categoria:
                        failed_rows.append(f"Fila {fila}: CategoriaDocente '{row.get('CategoriaDocente')}' no encontrada.")
                        continue

                    if codigo in existing_codigos:
                        duplicated_rows.append(f"Fila {fila}: Código de docente '{codigo}' ya existe.")
                        continue
                    existing_codigos.add(codigo)  # Añadir para evitar duplicados en batch

                    docente = Docente(
                        DocenteCodigo=codigo,
                        DocenteNombre=nombre,
                        DocenteApellido=apellido,
                        DocenteSexo=sexo,
                        DocenteEstadoCivil=estado_civil,
                        DocenteFechaNacimiento=fecha_nacimiento,
                        DocenteLugarNacimiento=lugar_nacimiento,
                        DocenteFechaIngreso=fecha_ingreso,
                        DocenteNacionalidad=nacionalidad,
                        DocenteTipoIdentificacion=tipo_id,
                        DocenteNumeroIdentificacion=num_id,
                        DocenteTelefono=telefono,
                        DocenteCorreoElectronico=correo,
                        DocenteDireccion=direccion,
                        DocenteEstado="Activo",
                        DocenteObservaciones=observaciones,
                        Docente_UniversidadFK=universidad,
                        Docente_TipoDocenteFK=tipo,
                        Docente_CategoriaDocenteFK=categoria,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(docente)

                except ValueError:
                    continue
                except Exception as e:
                    failed_rows.append(f"Fila {fila}: Error inesperado: {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Docente.objects.bulk_create(records_to_create)

                return Response({
                    "message": f"{len(records_to_create)} docentes importados exitosamente. "
                               f"{len(duplicated_rows)} duplicados omitidos. "
                               f"{len(failed_rows)} errores encontrados.",
                    "errores": failed_rows,
                    "duplicados": duplicated_rows
                }, status=status.HTTP_201_CREATED)

            # Sin registros creados
            message = "No se importó ningún docente."
            if duplicated_rows and failed_rows:
                message += " Todos los registros eran duplicados o contenían errores."
            elif duplicated_rows:
                message += " Todos los registros eran duplicados."
            elif failed_rows:
                message += " Todos los registros tenían errores."

            return Response({
                "message": message,
                "errores": failed_rows,
                "duplicados": duplicated_rows
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class ImportAsignacion(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        period = request.data.get("period")
        if not period:
            return Response({"error": "Periodo es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            return Response({"error": "No se envió ningún archivo Excel."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)
            df = df.dropna(how='all')  # Eliminar filas totalmente vacías

            required_columns = [
                "NRC", "Clave", "Asignatura", "Codigo", "Profesor", "Seccion", "Modalidad",
                "Campus", "Facultad", "Escuela", "Tipo", "Cupo", "Inscripto", "Horario", "Dias",
                "Aula", "Creditos"
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas requeridas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Precargar datos para evitar consultas en el loop
            facultades = {f.FacultadNombre.strip().lower(): f for f in Facultad.objects.all()}
            escuelas = {e.EscuelaNombre.strip().lower(): e for e in Escuela.objects.all()}
            docentes = {
                f"{d.DocenteNombre.strip()} {d.DocenteApellido.strip()}".lower(): d
                for d in Docente.objects.all()
            }
            campus_list = {c.CampusNombre.strip().lower(): c for c in Campus.objects.all()}
            universidad = Universidad.objects.first()
            periodo = PeriodoAcademico.objects.filter(pk=period).first()
            if not periodo:
                return Response({"error": "Periodo no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

            records_to_create = []
            failed_rows = []
            duplicates = []

            # Precargar NRC existentes para evitar duplicados en batch
            existing_nrcs = set(
                AsignacionDocente.objects.filter(periodoFk=periodo).values_list('nrc', flat=True)
            )

            for index, row in df.iterrows():
                fila = index + 2  # Número real de fila Excel

                try:
                    facultad = facultades.get(str(row["Facultad"]).strip().lower())
                    escuela = escuelas.get(str(row["Escuela"]).strip().lower())
                    campus = campus_list.get(str(row["Campus"]).strip().lower())

                    profesor_str = str(row["Profesor"]).strip()
                    full_name = profesor_str.split()
                    if len(full_name) < 2:
                        failed_rows.append(f"Fila {fila}: Nombre de docente inválido: '{profesor_str}'")
                        continue

                    nombre = " ".join(full_name[:-1]).strip()
                    apellidos = full_name[-1].strip()
                    docente = docentes.get(f"{nombre} {apellidos}".lower())

                    # Validar existencia de relaciones
                    if not facultad or not escuela or not campus or not docente:
                        if not facultad:
                            failed_rows.append(f"Fila {fila}: Facultad no encontrada: '{row['Facultad']}'")
                        if not escuela:
                            failed_rows.append(f"Fila {fila}: Escuela no encontrada: '{row['Escuela']}'")
                        if not campus:
                            failed_rows.append(f"Fila {fila}: Campus no encontrado: '{row['Campus']}'")
                        if not docente:
                            failed_rows.append(f"Fila {fila}: Docente no encontrado: '{profesor_str}'")
                        continue

                    nrc = str(row["NRC"]).strip()
                    if nrc in existing_nrcs:
                        duplicates.append(f"Fila {fila}: Duplicado NRC {nrc}")
                        continue
                    existing_nrcs.add(nrc)  # Agregar para evitar duplicados en batch

                    asignacion = AsignacionDocente(
                        nrc=nrc,
                        clave=str(row["Clave"]).strip(),
                        nombre=str(row["Asignatura"]).strip(),
                        codigo=str(row["Codigo"]).strip(),
                        docenteFk=docente,
                        seccion=str(row["Seccion"]).strip(),
                        modalidad=str(row["Modalidad"]).strip(),
                        campusFk=campus,
                        universidadFk=universidad,
                        facultadFk=facultad,
                        escuelaFk=escuela,
                        tipo=str(row["Tipo"]).strip(),
                        cupo=int(row["Cupo"]),
                        inscripto=int(row["Inscripto"]),
                        horario=str(row["Horario"]).strip(),
                        dias=str(row["Dias"]).strip(),
                        aula=str(row["Aula"]).strip(),
                        creditos=int(row["Creditos"]),
                        periodoFk=periodo,
                        usuario_registro=request.user.username if request.user.is_authenticated else "sistema"
                    )
                    records_to_create.append(asignacion)

                except Exception as e:
                    failed_rows.append(f"Fila {fila}: Error inesperado: {str(e)}")

            if failed_rows:
                return Response({
                    "error": "Errores en filas.",
                    "failed_records": failed_rows
                }, status=status.HTTP_400_BAD_REQUEST)

            if records_to_create:
                with transaction.atomic():
                    AsignacionDocente.objects.bulk_create(records_to_create)

            return Response({
                "message": f"{len(records_to_create)} registros importados exitosamente.",
                "duplicados": duplicates
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImportUniversidad(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No se envió ningún archivo Excel"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)
            df = df.dropna(how='all')  # Elimina filas totalmente vacías

            required_columns = [
                'Codigo', 'Nombre', 'Direccion', 'Telefono',
                'Email', 'Sitio Web', 'Rector'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            total_filas_excel = len(df)
            records_to_create = []
            failed_rows = []
            filas_incompletas = 0
            duplicados_omitidos = 0

            # Precargar códigos y nombres existentes para evitar consultas repetidas
            existing_codes = set(Universidad.objects.values_list('UniversidadCodigo', flat=True))
            existing_names = set(name.lower() for name in Universidad.objects.values_list('UniversidadNombre', flat=True))

            for index, row in df.iterrows():
                fila = index + 2  # Número de fila real en Excel

                try:
                    codigo = str(row.get('Codigo', '')).strip()
                    nombre = str(row.get('Nombre', '')).strip()
                    direccion = str(row.get('Direccion', '')).strip()
                    telefono = str(row.get('Telefono', '')).strip()
                    email = str(row.get('Email', '')).strip()
                    sitio_web = str(row.get('Sitio Web', '')).strip()
                    rector = str(row.get('Rector', '')).strip()

                    # Validar campos vacíos
                    if not all([codigo, nombre, direccion, telefono, email, sitio_web, rector]):
                        filas_incompletas += 1
                        failed_rows.append(f"Datos incompletos en fila {fila}: {row.to_dict()}")
                        continue

                    # Validar duplicados con sets
                    if codigo in existing_codes or nombre.lower() in existing_names:
                        duplicados_omitidos += 1
                        continue

                    # Añadir a sets para evitar duplicados en batch
                    existing_codes.add(codigo)
                    existing_names.add(nombre.lower())

                    universidad = Universidad(
                        UniversidadCodigo=codigo,
                        UniversidadNombre=nombre,
                        UniversidadDireccion=direccion,
                        UniversidadTelefono=telefono,
                        UniversidadEmail=email,
                        UniversidadSitioWeb=sitio_web,
                        UniversidadRector=rector,
                        UniversidadEstado='Activo',
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(universidad)

                except Exception as e:
                    failed_rows.append(f"Error inesperado en fila {fila}: {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Universidad.objects.bulk_create(records_to_create)

            return Response({
                "message": f"{len(records_to_create)} universidades importadas exitosamente.",
                "total_filas_excel": total_filas_excel,
                "filas_importadas": len(records_to_create),
                "filas_incompletas": filas_incompletas,
                "duplicados_omitidos": duplicados_omitidos,
                "errores": failed_rows,
            }, status=status.HTTP_201_CREATED if records_to_create else status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ImportCampus(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No se envió ningún archivo Excel"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)

            required_columns = [
                'Codigo', 'Nombre', 'Direccion', 'Pais', 'Provincia',
                'Ciudad', 'Telefono', 'Correo Contacto', 'Universidad'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas requeridas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {
                u.UniversidadNombre.strip().lower(): u
                for u in Universidad.objects.all()
            }

            # Cargar códigos y nombres existentes para evitar consultas repetidas
            existing_codes = set(Campus.objects.values_list('CampusCodigo', flat=True))
            existing_names = set(name.lower() for name in Campus.objects.values_list('CampusNombre', flat=True))

            records_to_create = []
            failed_rows = []
            duplicated_rows = []
            duplicated_names = []

            for index, row in df.iterrows():
                fila = index + 2  # Número de fila real en Excel (incluyendo encabezado)
                try:
                    # Extraer y limpiar campos
                    codigo = str(row.get('Codigo', '')).strip()
                    nombre = str(row.get('Nombre', '')).strip()
                    direccion = str(row.get('Direccion', '')).strip()
                    pais = str(row.get('Pais', '')).strip()
                    provincia = str(row.get('Provincia', '')).strip()
                    ciudad = str(row.get('Ciudad', '')).strip()
                    telefono = str(row.get('Telefono', '')).strip()
                    correo = str(row.get('Correo Contacto', '')).strip()
                    universidad_nombre = str(row.get('Universidad', '')).strip().lower()

                    # Validar campos vacíos de forma dinámica
                    required_fields = {
                        "Codigo": codigo,
                        "Nombre": nombre,
                        "Direccion": direccion,
                        "Pais": pais,
                        "Provincia": provincia,
                        "Ciudad": ciudad,
                        "Telefono": telefono,
                        "Correo Contacto": correo,
                        "Universidad": universidad_nombre,
                    }

                    for field_name, value in required_fields.items():
                        if not value:
                            failed_rows.append(f"Fila {fila}: El campo '{field_name}' está vacío.")
                            raise ValueError("Campo vacío")

                    universidad = universidades.get(universidad_nombre)
                    if not universidad:
                        failed_rows.append(f"Fila {fila}: La universidad '{row.get('Universidad', '')}' no existe.")
                        continue

                    # Validar duplicados usando sets para evitar consultas
                    if codigo in existing_codes:
                        duplicated_rows.append(f"Fila {fila}: El código '{codigo}' ya existe.")
                        continue
                    if nombre.lower() in existing_names:
                        duplicated_rows.append(f"Fila {fila}: El nombre '{nombre}' ya existe.")
                        duplicated_names.append(nombre)
                        continue

                    # Agregar código y nombre a sets para evitar duplicados dentro del batch actual
                    existing_codes.add(codigo)
                    existing_names.add(nombre.lower())

                    campus = Campus(
                        CampusCodigo=codigo,
                        CampusNombre=nombre,
                        CampusDireccion=direccion,
                        CampusPais=pais,
                        CampusProvincia=provincia,
                        CampusCiudad=ciudad,
                        CampusTelefono=telefono,
                        CampusCorreoContacto=correo,
                        CampusEstado='Activo',
                        Campus_UniversidadFK=universidad,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(campus)

                except ValueError:
                    # Ya registramos error arriba
                    continue
                except Exception as e:
                    failed_rows.append(f"Error inesperado en fila {fila}: {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Campus.objects.bulk_create(records_to_create)

                return Response({
                    "message": f"{len(records_to_create)} campus importados exitosamente. "
                               f"{len(duplicated_rows)} duplicados fueron omitidos. "
                               f"{len(failed_rows)} filas fallaron.",
                    "errores": failed_rows,
                    "duplicados": duplicated_rows,
                    "nombres_duplicados": duplicated_names
                }, status=status.HTTP_201_CREATED)

            # No se importó ningún registro
            if duplicated_rows and failed_rows:
                message = "No se importó ningún campus. Todos los registros eran duplicados o contenían errores."
            elif duplicated_rows:
                message = "No se importó ningún campus. Todos los registros eran duplicados."
            elif failed_rows:
                message = "No se importó ningún campus. Todos los registros tenían errores."
            else:
                message = "No se importó ningún campus. Causa desconocida."

            return Response({
                "message": message,
                "errores": failed_rows,
                "duplicados": duplicated_rows,
                "nombres_duplicados": duplicated_names
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImportData(APIView):
    """
    APIView for importing data from an uploaded Excel file.
    This class provides a POST endpoint that accepts an Excel file containing records to be imported into the database.
    It expects the Excel file to have the columns: 'Nombre', 'Estado', and 'Universidad'. For each row, it checks if the
    referenced university exists and skips duplicate records based on 'nombre' and 'UniversidadCodigo'. Valid records are
    bulk created in a single database transaction.
    Attributes:
        parser_classes (list): Parsers to handle multipart/form-data requests.
        model_class (Model): The Django model class to which the data will be imported. Should be set in subclasses.
    Methods:
        post(request, *args, **kwargs):
            Handles POST requests to import data from the uploaded Excel file.
            Returns a success message with the number of records imported, or an error message if the import fails.
    """
    parser_classes = [MultiPartParser, FormParser]

    model_class = None  # To be defined in subclasses

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No excel enviado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)

            required_columns = ['Nombre', 'Estado', 'Universidad']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Falta la columna: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            records_to_create = []
            for _, row in df.iterrows():
                try:
                    nombre = str(row.get('Nombre', '')).strip()
                    estado = str(row.get('Estado', '')).strip()
                    universidad_nombre = str(row.get('Universidad', '')).strip()

                    universidad = Universidad.objects.filter(nombre=universidad_nombre).first()
                    if not universidad:
                        return Response(
                            {"error": f"Universidad con nombre '{universidad_nombre}' no existe."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # Check if record already exists
                    if self.model_class.objects.filter(nombre=nombre, UniversidadCodigo=universidad).exists():
                        continue  # Skip duplicates

                    # Prepare the object for bulk creation
                    records_to_create.append(self.model_class(
                        nombre=nombre,
                        estado=estado,
                        UniversidadCodigo=universidad
                    ))

                except KeyError as e:
                    return Response(
                        {"error": f"Falta los datos de la columna: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Exception as e:
                    return Response(
                        {"error": f"Error processing row: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Bulk create in a single transaction
            if records_to_create:
                with transaction.atomic():
                    self.model_class.objects.bulk_create(records_to_create)

            return Response(
                {"message": f"Se han importado {len(records_to_create)} registros."},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImportFacultad(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No se envió ningún archivo Excel"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)
            df = df.dropna(how='all')  # Ignorar filas vacías

            required_columns = [
                'Codigo', 'Nombre', 'Decano', 'Direccion', 'Telefono',
                'Email', 'Universidad', 'Campus'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas requeridas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()}
            campus_map = {c.CampusNombre.strip().lower(): c for c in Campus.objects.all()}

            records_to_create = []
            failed_rows = []
            duplicated_rows = []
            duplicated_names = set()

            # Cargar códigos y nombres existentes para evitar duplicados repetidos
            existing_codigos = set(Facultad.objects.values_list('FacultadCodigo', flat=True))
            existing_nombres = set(Facultad.objects.values_list('FacultadNombre', flat=True))

            for index, row in df.iterrows():
                fila = index + 2
                try:
                    codigo = str(row.get('Codigo', '')).strip()
                    nombre = str(row.get('Nombre', '')).strip()
                    decano = str(row.get('Decano', '')).strip()
                    direccion = str(row.get('Direccion', '')).strip()
                    telefono = str(row.get('Telefono', '')).strip()
                    email = str(row.get('Email', '')).strip()
                    universidad_nombre = str(row.get('Universidad', '')).strip().lower()
                    campus_nombre = str(row.get('Campus', '')).strip().lower()

                    required_fields = {
                        "Codigo": codigo,
                        "Nombre": nombre,
                        "Decano": decano,
                        "Direccion": direccion,
                        "Telefono": telefono,
                        "Email": email,
                        "Universidad": universidad_nombre,
                        "Campus": campus_nombre,
                    }

                    for field, value in required_fields.items():
                        if not value:
                            failed_rows.append(f"Fila {fila}: El campo '{field}' está vacío.")
                            raise ValueError("Campo vacío")

                    universidad = universidades.get(universidad_nombre)
                    campus = campus_map.get(campus_nombre)

                    if not universidad:
                        failed_rows.append(f"Fila {fila}: Universidad '{row.get('Universidad')}' no encontrada.")
                        continue
                    if not campus:
                        failed_rows.append(f"Fila {fila}: Campus '{row.get('Campus')}' no encontrado.")
                        continue

                    if codigo in existing_codigos:
                        duplicated_rows.append(f"Fila {fila}: El código '{codigo}' ya existe.")
                        continue
                    existing_codigos.add(codigo)

                    if nombre.lower() in (n.lower() for n in existing_nombres):
                        duplicated_rows.append(f"Fila {fila}: El nombre '{nombre}' ya existe.")
                        duplicated_names.add(nombre)
                        continue
                    existing_nombres.add(nombre)

                    facultad = Facultad(
                        FacultadCodigo=codigo,
                        FacultadNombre=nombre,
                        FacultadDecano=decano,
                        FacultadDireccion=direccion,
                        FacultadTelefono=telefono,
                        FacultadEmail=email,
                        FacultadEstado="Activo",
                        Facultad_UniversidadFK=universidad,
                        Facultad_CampusFK=campus,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(facultad)

                except ValueError:
                    continue
                except Exception as e:
                    failed_rows.append(f"Error inesperado en fila {fila}: {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Facultad.objects.bulk_create(records_to_create)

                return Response({
                    "message": f"{len(records_to_create)} facultades importadas exitosamente. "
                               f"{len(duplicated_rows)} duplicados omitidos. "
                               f"{len(failed_rows)} filas fallaron.",
                    "errores": failed_rows,
                    "duplicados": duplicated_rows,
                    "nombres_duplicados": list(duplicated_names)
                }, status=status.HTTP_201_CREATED)

            message = "No se importó ninguna facultad."
            if duplicated_rows and failed_rows:
                message += " Todos los registros eran duplicados o contenían errores."
            elif duplicated_rows:
                message += " Todos los registros eran duplicados."
            elif failed_rows:
                message += " Todos los registros tenían errores."
            else:
                message += " Causa desconocida."

            return Response({
                "message": message,
                "errores": failed_rows,
                "duplicados": duplicated_rows,
                "nombres_duplicados": list(duplicated_names)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImportCategoriaDocente(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response(
                {"error": "No se envió ningún archivo Excel"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_excel(excel_file)
            df = df.dropna(how='all')  # Ignorar filas totalmente vacías

            required_columns = ['Codigo', 'Nombre', 'Universidad']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas requeridas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {
                u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()
            }

            records_to_create = []
            failed_rows = []
            duplicated_rows = []
            duplicated_names = set()

            # Cargar códigos y nombres existentes para evitar duplicados múltiples
            existing_codigos = set(CategoriaDocente.objects.values_list('categoriaCodigo', flat=True))
            existing_nombres = set(CategoriaDocente.objects.values_list('CategoriaNombre', flat=True))

            for index, row in df.iterrows():
                fila = index + 2
                try:
                    codigo = str(row.get('Codigo', '')).strip()
                    nombre = str(row.get('Nombre', '')).strip()
                    universidad_nombre = str(row.get('Universidad', '')).strip().lower()

                    required_fields = {
                        "Codigo": codigo,
                        "Nombre": nombre,
                        "Universidad": universidad_nombre,
                    }

                    for field, value in required_fields.items():
                        if not value:
                            failed_rows.append(f"Fila {fila}: El campo '{field}' está vacío.")
                            raise ValueError("Campo vacío")

                    universidad = universidades.get(universidad_nombre)
                    if not universidad:
                        failed_rows.append(f"Fila {fila}: Universidad '{row.get('Universidad')}' no encontrada.")
                        continue

                    if codigo in existing_codigos:
                        duplicated_rows.append(f"Fila {fila}: El código '{codigo}' ya existe.")
                        continue
                    existing_codigos.add(codigo)

                    if nombre.lower() in (n.lower() for n in existing_nombres):
                        duplicated_rows.append(f"Fila {fila}: El nombre '{nombre}' ya existe.")
                        duplicated_names.add(nombre)
                        continue
                    existing_nombres.add(nombre)

                    categoria = CategoriaDocente(
                        categoriaCodigo=codigo,
                        CategoriaNombre=nombre,
                        CategoriaEstado="Activo",
                        Categoria_UniversidadFK=universidad,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(categoria)

                except ValueError:
                    continue
                except Exception as e:
                    failed_rows.append(f"Error inesperado en fila {fila}: {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    CategoriaDocente.objects.bulk_create(records_to_create)

                return Response({
                    "message": f"{len(records_to_create)} categorías importadas exitosamente. "
                               f"{len(duplicated_rows)} duplicados omitidos. "
                               f"{len(failed_rows)} filas fallaron.",
                    "errores": failed_rows,
                    "duplicados": duplicated_rows,
                    "nombres_duplicados": list(duplicated_names)
                }, status=status.HTTP_201_CREATED)

            message = "No se importó ninguna categoría."
            if duplicated_rows and failed_rows:
                message += " Todos los registros eran duplicados o contenían errores."
            elif duplicated_rows:
                message += " Todos los registros eran duplicados."
            elif failed_rows:
                message += " Todos los registros tenían errores."
            else:
                message += " Causa desconocida."

            return Response({
                "message": message,
                "errores": failed_rows,
                "duplicados": duplicated_rows,
                "nombres_duplicados": list(duplicated_names)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class ImportTipoDocente(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No se envió ningún archivo Excel"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)

            required_columns = ['Codigo', 'Descripcion', 'Universidad']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas requeridas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Crear diccionario de universidades (para acceso rápido sin hits a la base repetidos)
            universidades = {
                u.UniversidadNombre.strip().lower(): u
                for u in Universidad.objects.all()
            }

            records_to_create = []
            failed_rows = []
            duplicated_rows = []
            duplicated_codigos = []

            for index, row in df.iterrows():
                fila = index + 2  # +2 porque los índices en pandas comienzan en 0 y la fila 1 es el encabezado
                try:
                    codigo = str(row.get('Codigo', '')).strip()
                    descripcion = str(row.get('Descripcion', '')).strip()
                    universidad_nombre = str(row.get('Universidad', '')).strip().lower()

                    # Validación de campos obligatorios vacíos
                    campos_obligatorios = {
                        "Codigo": codigo,
                        "Descripcion": descripcion,
                        "Universidad": universidad_nombre,
                    }

                    for campo, valor in campos_obligatorios.items():
                        if not valor:
                            failed_rows.append(f"Fila {fila}: El campo '{campo}' está vacío.")
                            raise ValueError("Campo vacío")

                    universidad = universidades.get(universidad_nombre)
                    if not universidad:
                        failed_rows.append(f"Fila {fila}: Universidad '{row.get('Universidad')}' no encontrada.")
                        continue

                    # Verificar si ya existe el código en la base de datos
                    if TipoDocente.objects.filter(TipoDocenteCodigo=codigo).exists():
                        duplicated_rows.append(f"Fila {fila}: El código '{codigo}' ya existe.")
                        duplicated_codigos.append(codigo)
                        continue

                    tipo_docente = TipoDocente(
                        TipoDocenteCodigo=codigo,
                        TipoDocenteDescripcion=descripcion,
                        TipoDocenteEstado="Activo",
                        TipoDocente_UniversidadFK=universidad,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(tipo_docente)

                except ValueError:
                    continue  # Ya fue registrado en failed_rows
                except Exception as e:
                    failed_rows.append(f"Error inesperado en fila {fila}: {str(e)}")

            # Crear en bloque si hay registros válidos
            if records_to_create:
                with transaction.atomic():
                    TipoDocente.objects.bulk_create(records_to_create)

                return Response({
                    "message": f"{len(records_to_create)} tipos de docente importados exitosamente. "
                               f"{len(duplicated_rows)} duplicados fueron omitidos. "
                               f"{len(failed_rows)} filas fallaron.",
                    "errores": failed_rows,
                    "duplicados": duplicated_rows,
                    "codigos_duplicados": duplicated_codigos
                }, status=status.HTTP_201_CREATED)

            # Si no se importó ningún registro
            if duplicated_rows and failed_rows:
                message = "No se importó ningún tipo de docente. Todos los registros eran duplicados o tenían errores."
            elif duplicated_rows:
                message = "No se importó ningún tipo de docente. Todos los registros eran duplicados."
            elif failed_rows:
                message = "No se importó ningún tipo de docente. Todos los registros tenían errores."
            else:
                message = "No se importó ningún tipo de docente. Causa desconocida."

            return Response({
                "message": message,
                "errores": failed_rows,
                "duplicados": duplicated_rows,
                "codigos_duplicados": duplicated_codigos
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
#endregion

@api_view(['GET'])
def resumen_asignaciones_docente(request):
    docente_id = request.query_params.get('docente')
    periodo_nombre = request.query_params.get('periodo')

    if not docente_id or not periodo_nombre:
        return Response({"error": "Parámetros 'docente' y 'periodo' son requeridos"}, status=400)

    try:
        periodo = PeriodoAcademico.objects.filter(PeriodoNombre=periodo_nombre).first()
        docente = Docente.objects.filter(pk=docente_id).first()

        if not periodo or not docente:
            return Response({
                "docente": docente_id,
                "periodo": periodo_nombre,
                "total_creditos": 0,
                "total_materias": 0,
                "asignaturas": [],
                "mensaje": "Periodo o docente no encontrado"
            }, status=200)

        asignaciones = AsignacionDocente.objects.filter(
            docenteFk=docente,
            periodoFk=periodo
        )

        resumen = asignaciones.aggregate(
            total_creditos=Sum('creditos'),
            total_materias=Count('AsignacionID')
        )

        asignaturas_info = list(asignaciones.values(
            'nrc', 'clave', 'codigo', 'nombre'
        ))

        # Obtenemos facultad y escuela desde la primera asignación (se asume que son las mismas para todas)
        primera_asignacion = asignaciones.first()
        facultad_nombre = primera_asignacion.facultadFk.FacultadNombre if primera_asignacion else ''
        escuela_nombre = primera_asignacion.escuelaFk.EscuelaNombre if primera_asignacion else ''

        return Response({
            "docente": docente.get_nombre_completo,
            "periodo": periodo.PeriodoNombre,
            "total_creditos": resumen['total_creditos'] or 0,
            "total_materias": resumen['total_materias'],
            "facultad": facultad_nombre,
            "escuela": escuela_nombre,
            "asignaturas": asignaturas_info
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
def copiar_asignaciones(request):
    from_period = request.data.get('from_period')
    to_period = request.data.get('to_period')

    if not from_period or not to_period:
        return Response({"error": "Parámetros inválidos"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Buscar los objetos de periodo
        from_period_obj = PeriodoAcademico.objects.filter(PeriodoNombre=from_period).first()
        to_period_obj = PeriodoAcademico.objects.filter(PeriodoNombre=to_period).first()

        if not from_period_obj or not to_period_obj:
            return Response({"error": "Período no encontrado."}, status=404)

        # Buscar asignaciones del período origen y ordenarlas por orden de creación
        asignaciones_origen = AsignacionDocente.objects.filter(
            periodoFk=from_period_obj
        ).order_by('AsignacionID')

        if not asignaciones_origen.exists():
            return Response({
                "message": f"No hay asignaciones en el período {from_period}"
            }, status=200)

        # Verificar duplicados por nrc + periodoFk destino
        nrc_existentes = set(
            AsignacionDocente.objects
            .filter(periodoFk=to_period_obj)
            .values_list('nrc', flat=True)
        )

        nuevas_asignaciones = []

        for a in asignaciones_origen:
            if a.nrc in nrc_existentes:
                continue  # evita duplicados solo dentro del periodo destino

            nuevas_asignaciones.append(AsignacionDocente(
                nrc=a.nrc,
                clave=a.clave,
                nombre=a.nombre,
                codigo=a.codigo,
                seccion=a.seccion,
                modalidad=a.modalidad,
                cupo=a.cupo,
                inscripto=a.inscripto,
                horario=a.horario,
                dias=a.dias,
                aula=a.aula,
                creditos=a.creditos,
                tipo=a.tipo,
                accion='nuevo',
                usuario_registro='admin',
                docenteFk=a.docenteFk,
                campusFk=a.campusFk,
                universidadFk=a.universidadFk,
                facultadFk=a.facultadFk,
                escuelaFk=a.escuelaFk,
                periodoFk=to_period_obj
            ))

        if not nuevas_asignaciones:
            return Response({
                "message": f"Todas las asignaciones del período {from_period} ya existen en el período {to_period} y fueron omitidas."
            }, status=200)

        # Inserta manteniendo el orden
        AsignacionDocente.objects.bulk_create(nuevas_asignaciones)

        return Response({
            "message": f"{len(nuevas_asignaciones)} asignaciones copiadas exitosamente de {from_period} a {to_period}"
        }, status=201)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)
    
    
    
# @permission_classes([IsAuthenticated])    
@api_view(["GET"])
def dashboard_data(request):
    # Último período académico
    periodo_actual = PeriodoAcademico.objects.order_by("-PeriodoID").first()
    if not periodo_actual:
        return Response({"error": "No hay períodos registrados."}, status=404)

    # Asignaciones filtradas por el período actual
    asignaciones = AsignacionDocente.objects.filter(periodoFk=periodo_actual)

    # Métricas generales
    data = {
        "periodoActual": periodo_actual.PeriodoNombre,
        "totalAsignaciones": asignaciones.count(),
        "totalDocentes": asignaciones.values("docenteFk").distinct().count(),
        "totalErrores": asignaciones.filter(accion__in=["Error", "Incompleto", "Pendiente"]).count(),

        # Totales globales del sistema (para DashboardCard)
        "totalFacultades": Facultad.objects.count(),
        "totalEscuelas": Escuela.objects.count(),
        "totalUniversidades": Universidad.objects.count(),
        "totalCampus": Campus.objects.count(),
        "totalCategorias": CategoriaDocente.objects.count(),
        "totalTiposDocente": TipoDocente.objects.count(),
    }

    # Gráfico: Asignaciones por Facultad
    asignaciones_por_facultad = asignaciones.values(
        "facultadFk__FacultadNombre"
    ).annotate(total=Count("AsignacionID"))

    data["asignacionesPorFacultad"] = {
        "labels": [f["facultadFk__FacultadNombre"] for f in asignaciones_por_facultad],
        "datasets": [{
            "label": "Asignaciones",
            "data": [f["total"] for f in asignaciones_por_facultad],
            "backgroundColor": "#3B82F6"
        }]
    }

    # Gráfico: Docentes por categoría
    docentes_categoria = Docente.objects.values(
        "Docente_CategoriaDocenteFK__CategoriaNombre"
    ).annotate(total=Count("DocenteID"))

    data["docentesPorCategoria"] = {
        "labels": [d["Docente_CategoriaDocenteFK__CategoriaNombre"] or "No definida" for d in docentes_categoria],
        "datasets": [{
            "label": "Docentes",
            "data": [d["total"] for d in docentes_categoria],
            "backgroundColor": ["#10B981", "#60A5FA", "#F59E0B", "#EF4444", "#A855F7"]
        }]
    }

    return Response(data)