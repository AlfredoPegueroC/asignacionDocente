
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
  UserSerializer
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
    AsignacionDocente
    )
from .handles import createHandle, getAllHandle, deleteHandler,getAllHandle_asignacion, getAll
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
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


# Create your views here.
def index(request):
  return render(request, 'client/index.html')

class UserListView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500) 

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
def getAllUniversidad(request):
  return getAllHandle(request, Universidad, UniversidadSerializer)

@api_view(['GET'])
def getAllCampus(request):
    return getAllHandle(request, Campus, CampusSerializer)

@api_view(['GET'])
def getAllFacultad(request):
  return getAllHandle(request, Facultad, FacultadSerializer)

@api_view(['GET'])
def getAllEscuela(request):
  return getAllHandle(request, Escuela, EscuelaSerializer)

@api_view(['GET'])
def getAllTipoDocente(request):
  return getAllHandle(request, TipoDocente, TipoDocenteSerializer)

@api_view(['GET'])
def getAllCategoriaDocente(request):
  return getAllHandle(request, CategoriaDocente, CategoriaDocenteSerializer)

@api_view(['GET'])
def getAllDocente(request):
  return getAllHandle(request, Docente, DocenteSerializer)

@api_view(['GET'])
def getAllPeriodoAcademico(request):
  return getAllHandle(request, PeriodoAcademico, PeriodoAcademicoSerializer)

@api_view(['GET'])
def getAllAsignacion(request):
  return getAllHandle_asignacion(request, AsignacionDocente, AsignacionDocenteSerializer)

@api_view(['GET'])
def getAllAsignacion_frontend(request):
  return getAllHandle_asignacion(request,AsignacionDocente,AsignacionDocenteSerializer_frontend)



@api_view(['GET'])
def get_Universidad(request):
    return getAll(request, Universidad, UniversidadSerializer)

@api_view(['GET'])
def get_Facultad(request):
    return getAll(request, Facultad, FacultadSerializer)

@api_view(['GET'])
def get_Escuela(request):
    return getAll(request, Escuela, EscuelaSerializer)
@api_view(['GET'])
def get_TipoDocente(request):
    return getAll(request, TipoDocente, TipoDocenteSerializer)
@api_view(['GET'])
def get_CategoriaDocente(request):
    return getAll(request, CategoriaDocente, CategoriaDocenteSerializer)
@api_view(['GET'])
def get_Docente(request):
    return getAll(request, Docente, DocenteSerializer)
@api_view(['GET'])
def get_PeriodoAcademico(request):
    return getAll(request, PeriodoAcademico, PeriodoAcademicoSerializer)
#endregion



#region UPDATE

@api_view(['PUT', 'PATCH'])
def update_universidad(request, pk):
    try:
        universidad = Universidad.objects.get(pk=pk)
    except Universidad.DoesNotExist:
        return JsonResponse({'error': 'Universidad not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH']:
        ser = UniversidadSerializer(universidad, data=request.data, partial=(request.method == 'PATCH'))
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=status.HTTP_200_OK)
        return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_facultad(request, pk):
  try:
    facultad = Facultad.objects.get(pk=pk)
  except Facultad.DoesNotExist:
    return JsonResponse({'error': 'Facultad not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = FacultadSerializer(facultad, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_escuela(request, pk):
  try:
    escuela = Escuela.objects.get(pk=pk)
  except Escuela.DoesNotExist:
    return JsonResponse({'error': 'Escuela not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = EscuelaSerializer(escuela, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_tipoDocente(request, pk):
  try:
    tipoDocente = TipoDocente.objects.get(pk=pk)
  except TipoDocente.DoesNotExist:
    return JsonResponse({'error': 'Tipo docente not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = TipoDocenteSerializer(tipoDocente, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_categoriaDocente(request, pk):
  try:
    categoriaDocente = CategoriaDocente.objects.get(pk=pk)
  except CategoriaDocente.DoesNotExist:
    return JsonResponse({'error': 'Tipo docente not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = CategoriaDocenteSerializer(categoriaDocente, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_docente(request, pk):
  try:
    docente = Docente.objects.get(pk=pk)
  except Docente.DoesNotExist:
    return JsonResponse({'error': 'Tipo docente not found'}, status=status.HTTP_404_NOT_FOUND)
  if request.method in ['PUT', 'PATCH']:
      ser = DocenteSerializer(docente, data=request.data, partial=(request.method == 'PATCH'))
      if ser.is_valid():
          ser.save()
          return JsonResponse(ser.data, status=status.HTTP_200_OK)
      return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_periodoAcademico(request, pk):
  try:
    periodo = PeriodoAcademico.objects.get(pk=pk)
  except PeriodoAcademico.DoesNotExist:
    return JsonResponse({'error': 'Tipo docente not found'}, status=status.HTTP_404_NOT_FOUND)
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


#endregion

#region DETAILTS
@api_view(['GET'])
def details_universidad(request, pk):
    universidad = Universidad.objects.filter(pk=pk).first()

    if universidad is None:
        return Response({'error': 'Universidad not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UniversidadSerializer(universidad)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_facultad(request, pk):
    facultad = Facultad.objects.filter(pk=pk).first()
    if facultad is None:
        return Response({'error': 'Facultad not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = FacultadSerializer(facultad)

    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
def details_escuela(request, pk):
    escuela = Escuela.objects.filter(pk=pk).first()
    if escuela is None:
        return Response({'error': 'Escuela not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EscuelaSerializer(escuela)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_tipoDocente(request, pk):
    tipoDocente = TipoDocente.objects.filter(pk=pk).first()
    if tipoDocente is None:
        return Response({'error': 'Tipo docente not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TipoDocenteSerializer(tipoDocente)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_categoriaDocente(request, pk):
    categoriaDocente = CategoriaDocente.objects.filter(pk=pk).first()
    if categoriaDocente is None:
        return Response({'error': 'Categoria docente not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CategoriaDocenteSerializer(categoriaDocente)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_docente(request, pk):
    docente = Docente.objects.filter(pk=pk).first()
    if docente is None:
        return Response({'error': 'Docente not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DocenteSerializer(docente)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_periodoAcademico(request, pk):
    periodo = PeriodoAcademico.objects.filter(pk=pk).first()
    if periodo is None:
        return Response({'error': 'Periodo academico not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PeriodoAcademicoSerializer(periodo)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_Asignacion(request, pk):
    asignacion = AsignacionDocente.objects.filter(pk=pk).first()
    if asignacion is None:
        return Response({'error': 'Periodo academico not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = AsignacionDocenteSerializer(asignacion)

    return Response(serializer.data, status=status.HTTP_200_OK)
#endregion

#region Auth
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
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


@api_view(["GET"])
def UniversidadExport(request):
    queryset = Universidad.objects.all()
    data = []

    for universidad in queryset:
        data.append({
            'Código': universidad.UniversidadCodigo,
            'Nombre': universidad.UniversidadNombre,
            'Dirección': universidad.UniversidadDireccion,
            'Teléfono': universidad.UniversidadTelefono,
            'Email': universidad.UniversidadEmail,
            'Sitio Web': universidad.UniversidadSitioWeb,
            'Rector': universidad.UniversidadRector,
        })

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="universidades.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        pd.DataFrame(data).to_excel(writer, sheet_name='Universidades', index=False)

    return response

@api_view(["GET"])
def FacultadExport(request):
    queryset = Facultad.objects.select_related("Facultad_UniversidadFK").all()
    data = []

    for facultad in queryset:
        data.append({
            "Código": facultad.FacultadCodigo,
            "Nombre": facultad.FacultadNombre,
            "Decano": facultad.FacultadDecano,
            "Teléfono": facultad.FacultadTelefono,
            "Estado": facultad.FacultadEstado,
            "Universidad": facultad.Facultad_UniversidadFK.UniversidadNombre if facultad.Facultad_UniversidadFK else "—",
            "Dirección": facultad.FacultadDireccion,
        })

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="facultades.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        pd.DataFrame(data).to_excel(writer, sheet_name='Facultades', index=False)

    return response


@api_view(["GET"])
def EscuelaExport(request):
    queryset = Escuela.objects.select_related("Escuela_UniversidadFK", "Escuela_facultadFK").all()
    data = []

    for escuela in queryset:
        data.append({
            'Código': escuela.EscuelaCodigo,
            'Nombre': escuela.EscuelaNombre,
            'Directora': escuela.EscuelaDirectora,
            'Teléfono': escuela.EscuelaTelefono,
            'Correo': escuela.EscuelaCorreo,
            'Estado': escuela.EscuelaEstado,
            'Universidad': escuela.Escuela_UniversidadFK.UniversidadNombre if escuela.Escuela_UniversidadFK else "—",
            'Facultad': escuela.Escuela_facultadFK.FacultadNombre if escuela.Escuela_facultadFK else "—",
        })

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="escuelas.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        pd.DataFrame(data).to_excel(writer, sheet_name='Escuelas', index=False)

    return response

@api_view(["GET"])
def DocenteExport(request):
    queryset = Docente.objects.select_related(
        "Docente_UniversidadFK", 
        "Docente_TipoDocenteFK", 
        "Docente_CategoriaDocenteFK"
    ).all()

    data = []

    for d in queryset:
        data.append({
            "Código": d.DocenteCodigo,
            "Nombre": d.DocenteNombre,
            "Apellido": d.DocenteApellido,
            "Sexo": d.DocenteSexo,
            "Estado Civil": d.DocenteEstadoCivil,
            "Fecha Nacimiento": d.DocenteFechaNacimiento,
            "Lugar Nacimiento": d.DocenteLugarNacimiento,
            "Fecha Ingreso": d.DocenteFechaIngreso,
            "Nacionalidad": d.DocenteNacionalidad,
            "Tipo ID": d.DocenteTipoIdentificacion,
            "Número ID": d.DocenteNumeroIdentificacion,
            "Teléfono": d.DocenteTelefono,
            "Correo": d.DocenteCorreoElectronico,
            "Dirección": d.DocenteDireccion,
            "Estado": d.DocenteEstado,
            "Observaciones": d.DocenteObservaciones,
            "Usuario Registro": d.UsuarioRegistro,
            "Universidad": d.Docente_UniversidadFK.UniversidadNombre if d.Docente_UniversidadFK else "",
            "Tipo Docente": d.Docente_TipoDocenteFK.TipoDocenteDescripcion if d.Docente_TipoDocenteFK else "",
            "Categoría Docente": d.Docente_CategoriaDocenteFK.CategoriaNombre if d.Docente_CategoriaDocenteFK else "",
        })

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="docente_data.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        pd.DataFrame(data).to_excel(writer, sheet_name='Docentes', index=False)

    return response

@api_view(["GET"])
def CategoriaDocenteExport(request):
  queryset = CategoriaDocente.objects.all()
  data = []

  for categoria in queryset:
    data.append({
      'Nombre': categoria.nombre,
      'Estado': categoria.estado,
      'Universidad': categoria.UniversidadCodigo.nombre
    })

  response = HttpResponse(content_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename="CategoriaDocente_data.xlsx"'

  with pd.ExcelWriter(response, engine='openpyxl') as writer:
    pd.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)

  return response


@api_view(["GET"])
def TipoDocenteExport(request):
    queryset = TipoDocente.objects.all()
    data = []
    
    for tipo in queryset:
        data.append({
        'Nombre': tipo.nombre,
        'Estado': tipo.estado,
        'Universidad': tipo.UniversidadCodigo.nombre
        })
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="TipoDocente_data.xlsx"'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        pd.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)
    
    return response

@api_view(["GET"])
def PeriodoAcademicoExport(request):
    queryset = PeriodoAcademico.objects.all()
    data = []

    for periodo in queryset:
        data.append({
            'Nombre': periodo.nombre,
            'Estado': periodo.estado,
            'Universidad': periodo.UniversidadCodigo.nombre
        })
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PeriodoAcademico_data.xlsx"'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        pd.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)
    return response



@api_view(["GET"])
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

    # Crear respuesta en Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    filename = f'Asignacion_{period if period else "todos"}.xlsx'
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        pd.DataFrame(data).to_excel(writer, sheet_name="Sheet1", index=False)

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

            required_columns = [
                'Codigo', 'Nombre', 'Directora', 'Telefono',
                'Correo', 'Estado', 'Universidad', 'Facultad'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()}
            facultades = {f.FacultadNombre.strip().lower(): f for f in Facultad.objects.all()}

            records_to_create = []
            failed_rows = []

            for _, row in df.iterrows():
                try:
                    codigo = str(row['Codigo']).strip()
                    nombre = str(row['Nombre']).strip()
                    directora = str(row['Directora']).strip()
                    telefono = str(row['Telefono']).strip()
                    correo = str(row['Correo']).strip()
                    estado = str(row['Estado']).strip()
                    universidad_nombre = str(row['Universidad']).strip().lower()
                    facultad_nombre = str(row['Facultad']).strip().lower()

                    universidad = universidades.get(universidad_nombre)
                    facultad = facultades.get(facultad_nombre)

                    if not all([codigo, nombre, directora, telefono, correo, estado, universidad, facultad]):
                        failed_rows.append(f"Datos incompletos o entidades no encontradas en fila: {row.to_dict()}")
                        continue

                    if Escuela.objects.filter(EscuelaCodigo=codigo).exists():
                        failed_rows.append(f"Escuela duplicada (código): {codigo}")
                        continue

                    escuela = Escuela(
                        EscuelaCodigo=codigo,
                        EscuelaNombre=nombre,
                        EscuelaDirectora=directora,
                        EscuelaTelefono=telefono,
                        EscuelaCorreo=correo,
                        EscuelaEstado=estado,
                        Escuela_UniversidadFK=universidad,
                        Escuela_facultadFK=facultad,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(escuela)

                except Exception as e:
                    failed_rows.append(f"Error en fila: {row.to_dict()} => {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Escuela.objects.bulk_create(records_to_create)

            return Response({
                "message": f"{len(records_to_create)} escuelas importadas exitosamente.",
                "errores": failed_rows
            }, status=status.HTTP_201_CREATED)

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

            required_columns = [
                'Codigo', 'Nombre', 'Apellido', 'Sexo', 'EstadoCivil', 'FechaNacimiento',
                'LugarNacimiento', 'FechaIngreso', 'Nacionalidad', 'TipoIdentificacion',
                'NumeroIdentificacion', 'Telefono', 'CorreoElectronico', 'Direccion',
                'Estado', 'Observaciones', 'Universidad', 'TipoDocente', 'CategoriaDocente'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()}
            tipos_docente = {t.TipoDocenteDescripcion.strip().lower(): t for t in TipoDocente.objects.all()}
            categorias_docente = {c.CategoriaNombre.strip().lower(): c for c in CategoriaDocente.objects.all()}

            records_to_create = []
            failed_rows = []

            for _, row in df.iterrows():
                try:
                    universidad = universidades.get(str(row['Universidad']).strip().lower())
                    tipo = tipos_docente.get(str(row['TipoDocente']).strip().lower())
                    categoria = categorias_docente.get(str(row['CategoriaDocente']).strip().lower())

                    if not universidad:
                        failed_rows.append(f"Universidad no encontrada: {row['Universidad']}")
                        continue

                    if not tipo:
                        failed_rows.append(f"TipoDocente no encontrado: {row['TipoDocente']}")
                        continue

                    if not categoria:
                        failed_rows.append(f"CategoriaDocente no encontrada: {row['CategoriaDocente']}")
                        continue

                    codigo = str(row['Codigo']).strip()
                    if Docente.objects.filter(DocenteCodigo=codigo).exists():
                        failed_rows.append(f"Docente duplicado (código): {codigo}")
                        continue

                    docente = Docente(
                        DocenteCodigo=codigo,
                        DocenteNombre=str(row['Nombre']).strip(),
                        DocenteApellido=str(row['Apellido']).strip(),
                        DocenteSexo=str(row['Sexo']).strip(),
                        DocenteEstadoCivil=str(row['EstadoCivil']).strip(),
                        DocenteFechaNacimiento=pd.to_datetime(row['FechaNacimiento'], errors='coerce'),
                        DocenteLugarNacimiento=str(row['LugarNacimiento']).strip(),
                        DocenteFechaIngreso=pd.to_datetime(row['FechaIngreso'], errors='coerce'),
                        DocenteNacionalidad=str(row['Nacionalidad']).strip(),
                        DocenteTipoIdentificacion=str(row['TipoIdentificacion']).strip(),
                        DocenteNumeroIdentificacion=str(row['NumeroIdentificacion']).strip(),
                        DocenteTelefono=str(row['Telefono']).strip(),
                        DocenteCorreoElectronico=str(row['CorreoElectronico']).strip(),
                        DocenteDireccion=str(row['Direccion']).strip(),
                        DocenteEstado=str(row['Estado']).strip(),
                        DocenteObservaciones=str(row['Observaciones']).strip() if pd.notna(row['Observaciones']) else '',
                        Docente_UniversidadFK=universidad,
                        Docente_TipoDocenteFK=tipo,
                        Docente_CategoriaDocenteFK=categoria,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(docente)

                except Exception as e:
                    failed_rows.append(f"Error en fila: {row.to_dict()} => {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Docente.objects.bulk_create(records_to_create)

            return Response({
                "message": f"{len(records_to_create)} docentes importados exitosamente.",
                "errores": failed_rows
            }, status=status.HTTP_201_CREATED)

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

            facultades = {f.FacultadNombre.strip().lower(): f for f in Facultad.objects.all()}
            escuelas = {e.EscuelaNombre.strip().lower(): e for e in Escuela.objects.all()}
            docentes = {f"{d.DocenteNombre.strip()} {d.DocenteApellido.strip()}".lower(): d for d in Docente.objects.all()}
            campus_list = {c.CampusNombre.strip().lower(): c for c in Campus.objects.all()}
            universidad = Universidad.objects.first()
            periodo = PeriodoAcademico.objects.filter(pk=period).first()
            if not periodo:
                return Response({"error": "Periodo no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

            records_to_create = []
            failed_rows = []
            duplicates = []

            for _, row in df.iterrows():
                try:
                    facultad = facultades.get(row["Facultad"].strip().lower())
                    escuela = escuelas.get(row["Escuela"].strip().lower())
                    campus = campus_list.get(row["Campus"].strip().lower())

                    full_name = row["Profesor"].strip().split()
                    if len(full_name) < 2:
                        failed_rows.append(f"Nombre de docente inválido: '{row['Profesor']}'")
                        continue

                    nombre = " ".join(full_name[:-1]).strip()
                    apellidos = full_name[-1].strip()
                    docente = docentes.get(f"{nombre} {apellidos}".lower())

                    if not all([facultad, escuela, campus, docente]):
                        if not facultad:
                            failed_rows.append(f"Facultad no encontrada: '{row['Facultad']}'")
                        if not escuela:
                            failed_rows.append(f"Escuela no encontrada: '{row['Escuela']}'")
                        if not campus:
                            failed_rows.append(f"Campus no encontrado: '{row['Campus']}'")
                        if not docente:
                            failed_rows.append(f"Docente no encontrado: '{row['Profesor']}'")
                        continue

                    if AsignacionDocente.objects.filter(nrc=row["NRC"], periodoFk=periodo).exists():
                        duplicates.append(f"Duplicado: NRC {row['NRC']}")
                        continue

                    records_to_create.append(
                        AsignacionDocente(
                            nrc=row["NRC"],
                            clave=row["Clave"],
                            nombre=row["Asignatura"],
                            codigo=row["Codigo"],
                            docenteFk=docente,
                            seccion=row["Seccion"],
                            modalidad=row["Modalidad"],
                            campusFk=campus,
                            universidadFk=universidad,
                            facultadFk=facultad,
                            escuelaFk=escuela,
                            tipo=row["Tipo"],
                            cupo=row["Cupo"],
                            inscripto=row["Inscripto"],
                            horario=row["Horario"],
                            dias=row["Dias"],
                            aula=row["Aula"],
                            creditos=row["Creditos"],
                            periodoFk=periodo,
                            usuario_registro=request.user.username if request.user.is_authenticated else "sistema"
                        )
                    )

                except Exception as e:
                    failed_rows.append(f"Error en fila: {row.to_dict()} => {str(e)}")

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

            required_columns = [
                'Codigo', 'Nombre', 'Direccion', 'Telefono',
                'Email', 'SitioWeb', 'Rector', 'Estado'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            records_to_create = []
            failed_rows = []

            for _, row in df.iterrows():
                try:
                    codigo = str(row.get('Codigo', '')).strip()
                    nombre = str(row.get('Nombre', '')).strip()
                    direccion = str(row.get('Direccion', '')).strip()
                    telefono = str(row.get('Telefono', '')).strip()
                    email = str(row.get('Email', '')).strip()
                    sitio_web = str(row.get('SitioWeb', '')).strip()
                    rector = str(row.get('Rector', '')).strip()
                    estado = str(row.get('Estado', '')).strip()

                    if not all([codigo, nombre, direccion, telefono, email, sitio_web, rector, estado]):
                        failed_rows.append(f"Datos incompletos en fila: {row.to_dict()}")
                        continue

                    if Universidad.objects.filter(UniversidadCodigo=codigo).exists():
                        failed_rows.append(f"Duplicado: Código '{codigo}' ya existe")
                        continue

                    universidad = Universidad(
                        UniversidadCodigo=codigo,
                        UniversidadNombre=nombre,
                        UniversidadDireccion=direccion,
                        UniversidadTelefono=telefono,
                        UniversidadEmail=email,
                        UniversidadSitioWeb=sitio_web,
                        UniversidadRector=rector,
                        UniversidadEstado=estado,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(universidad)

                except Exception as e:
                    failed_rows.append(f"Error en fila: {row.to_dict()} => {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Universidad.objects.bulk_create(records_to_create)

            return Response({
                "message": f"{len(records_to_create)} universidades importadas exitosamente.",
                "errores": failed_rows
            }, status=status.HTTP_201_CREATED)

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
                'Ciudad', 'Telefono', 'CorreoContacto', 'Estado', 'Universidad'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()}

            records_to_create = []
            failed_rows = []

            for _, row in df.iterrows():
                try:
                    codigo = str(row['Codigo']).strip()
                    nombre = str(row['Nombre']).strip()
                    direccion = str(row['Direccion']).strip()
                    pais = str(row['Pais']).strip()
                    provincia = str(row['Provincia']).strip()
                    ciudad = str(row['Ciudad']).strip()
                    telefono = str(row['Telefono']).strip()
                    correo = str(row['CorreoContacto']).strip()
                    estado = str(row['Estado']).strip()
                    universidad_nombre = str(row['Universidad']).strip().lower()

                    universidad = universidades.get(universidad_nombre)

                    if not all([codigo, nombre, direccion, pais, provincia, ciudad, telefono, correo, estado, universidad]):
                        failed_rows.append(f"Datos incompletos o universidad no encontrada en fila: {row.to_dict()}")
                        continue

                    if Campus.objects.filter(CampusCodigo=codigo).exists():
                        failed_rows.append(f"Campus duplicado (código): {codigo}")
                        continue

                    campus = Campus(
                        CampusCodigo=codigo,
                        CampusNombre=nombre,
                        CampusDireccion=direccion,
                        CampusPais=pais,
                        CampusProvincia=provincia,
                        CampusCiudad=ciudad,
                        CampusTelefono=telefono,
                        CampusCorreoContacto=correo,
                        CampusEstado=estado,
                        Campus_UniversidadFK=universidad,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(campus)

                except Exception as e:
                    failed_rows.append(f"Error en fila: {row.to_dict()} => {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Campus.objects.bulk_create(records_to_create)

            return Response({
                "message": f"{len(records_to_create)} campus importados exitosamente.",
                "errores": failed_rows
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ImportData(APIView):
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

            required_columns = [
                'Codigo', 'Nombre', 'Decano', 'Direccion', 'Telefono',
                'Email', 'Estado', 'Universidad', 'Campus'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()}
            campus_map = {c.CampusNombre.strip().lower(): c for c in Campus.objects.all()}

            records_to_create = []
            failed_rows = []

            for _, row in df.iterrows():
                try:
                    codigo = str(row['Codigo']).strip()
                    nombre = str(row['Nombre']).strip()
                    decano = str(row['Decano']).strip()
                    direccion = str(row['Direccion']).strip()
                    telefono = str(row['Telefono']).strip()
                    email = str(row['Email']).strip()
                    estado = str(row['Estado']).strip()
                    universidad_nombre = str(row['Universidad']).strip().lower()
                    campus_nombre = str(row['Campus']).strip().lower()

                    universidad = universidades.get(universidad_nombre)
                    campus = campus_map.get(campus_nombre)

                    if not all([codigo, nombre, decano, direccion, telefono, email, estado, universidad, campus]):
                        failed_rows.append(f"Datos incompletos o entidades no encontradas en fila: {row.to_dict()}")
                        continue

                    if Facultad.objects.filter(FacultadCodigo=codigo).exists():
                        failed_rows.append(f"Facultad duplicada (código): {codigo}")
                        continue

                    facultad = Facultad(
                        FacultadCodigo=codigo,
                        FacultadNombre=nombre,
                        FacultadDecano=decano,
                        FacultadDireccion=direccion,
                        FacultadTelefono=telefono,
                        FacultadEmail=email,
                        FacultadEstado=estado,
                        Facultad_UniversidadFK=universidad,
                        Facultad_CampusFK=campus,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(facultad)

                except Exception as e:
                    failed_rows.append(f"Error en fila: {row.to_dict()} => {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    Facultad.objects.bulk_create(records_to_create)

            return Response({
                "message": f"{len(records_to_create)} facultades importadas exitosamente.",
                "errores": failed_rows
            }, status=status.HTTP_201_CREATED)

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
            return Response({"error": "No se envió ningún archivo Excel"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)

            required_columns = ['Codigo', 'Nombre', 'Estado', 'Universidad']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()}

            records_to_create = []
            failed_rows = []

            for _, row in df.iterrows():
                try:
                    codigo = str(row['Codigo']).strip()
                    nombre = str(row['Nombre']).strip()
                    estado = str(row['Estado']).strip()
                    universidad_nombre = str(row['Universidad']).strip().lower()

                    universidad = universidades.get(universidad_nombre)

                    if not all([codigo, nombre, estado, universidad]):
                        failed_rows.append(f"Datos incompletos o universidad no encontrada en fila: {row.to_dict()}")
                        continue

                    if CategoriaDocente.objects.filter(categoriaCodigo=codigo).exists():
                        failed_rows.append(f"Categoría duplicada (código): {codigo}")
                        continue

                    categoria = CategoriaDocente(
                        categoriaCodigo=codigo,
                        CategoriaNombre=nombre,
                        CategoriaEstado=estado,
                        Categoria_UniversidadFK=universidad,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(categoria)

                except Exception as e:
                    failed_rows.append(f"Error en fila: {row.to_dict()} => {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    CategoriaDocente.objects.bulk_create(records_to_create)

            return Response({
                "message": f"{len(records_to_create)} categorías importadas exitosamente.",
                "errores": failed_rows
            }, status=status.HTTP_201_CREATED)

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

            required_columns = ['Codigo', 'Descripcion', 'Estado', 'Universidad']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan columnas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            universidades = {u.UniversidadNombre.strip().lower(): u for u in Universidad.objects.all()}

            records_to_create = []
            failed_rows = []

            for _, row in df.iterrows():
                try:
                    codigo = str(row['Codigo']).strip()
                    descripcion = str(row['Descripcion']).strip()
                    estado = str(row['Estado']).strip()
                    universidad_nombre = str(row['Universidad']).strip().lower()

                    universidad = universidades.get(universidad_nombre)

                    if not all([codigo, descripcion, estado, universidad]):
                        failed_rows.append(f"Datos incompletos o universidad no encontrada en fila: {row.to_dict()}")
                        continue

                    if TipoDocente.objects.filter(TipoDocenteCodigo=codigo).exists():
                        failed_rows.append(f"TipoDocente duplicado (código): {codigo}")
                        continue

                    tipo_docente = TipoDocente(
                        TipoDocenteCodigo=codigo,
                        TipoDocenteDescripcion=descripcion,
                        TipoDocenteEstado=estado,
                        TipoDocente_UniversidadFK=universidad,
                        UsuarioRegistro=request.user.username if request.user.is_authenticated else "admin"
                    )
                    records_to_create.append(tipo_docente)

                except Exception as e:
                    failed_rows.append(f"Error en fila: {row.to_dict()} => {str(e)}")

            if records_to_create:
                with transaction.atomic():
                    TipoDocente.objects.bulk_create(records_to_create)

            return Response({
                "message": f"{len(records_to_create)} tipos de docente importados exitosamente.",
                "errores": failed_rows
            }, status=status.HTTP_201_CREATED)

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

        nombres_asignaturas = list(asignaciones.values_list('nombre', flat=True))

        return Response({
            "docente": docente.get_nombre_completo,
            "periodo": periodo.PeriodoNombre,
            "total_creditos": resumen['total_creditos'] or 0,
            "total_materias": resumen['total_materias'],
            "asignaturas": nombres_asignaturas
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