
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
    # Get the period from request
    period = request.GET.get("period")

    # Filter by period if provided
    queryset = AsignacionDocente.objects.select_related("facultadCodigo", "escuelaCodigo", "DocenteCodigo")
    if period:
        queryset = queryset.filter(period=period)

    data = []

    for asignacion in queryset:
        data.append({
            "NRC": asignacion.nrc,
            "Clave": asignacion.clave,
            "Asignatura": asignacion.asignatura,
            "Codigo": asignacion.codigo,
            "Profesor": f"{asignacion.DocenteCodigo.nombre} {asignacion.DocenteCodigo.apellidos}" if asignacion.DocenteCodigo else None,
            "Seccion": asignacion.seccion,
            "Modalidad": asignacion.modalidad,
            "Campus": asignacion.campus,
            "Facultad": asignacion.facultadCodigo.nombre if asignacion.facultadCodigo else None,
            "Escuela": asignacion.escuelaCodigo.nombre if asignacion.escuelaCodigo else None,
            "Tipo": asignacion.tipo,
            "Cupo": asignacion.cupo,
            "Inscripto": asignacion.inscripto,
            "Horario": asignacion.horario,
            "Dias": asignacion.dias,
            "Aula": asignacion.Aula,
            "Creditos": asignacion.creditos,
        })

    # Create Excel response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="Asignacion_{period if period else "all"}.xlsx"'

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
            return Response({"error": "No excel enviado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)

            required_columns = ['Nombre', 'Estado', 'Universidad', 'Facultad']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Falta una columna: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            records_to_create = []
            records_created = 0
            
            with transaction.atomic():
                for _, row in df.iterrows():
                    try:
                        universidad = Universidad.objects.get(nombre=row['Universidad'].strip())

                        # Handle Facultad retrieval
                        facultades = Facultad.objects.filter(nombre=row['Facultad'].strip(), UniversidadCodigo=universidad)
                        if facultades.exists():
                            facultad = facultades.first()  # Use the first matching Facultad
                        else:
                            return Response(
                                {"error": f"Facultad con nombre '{row['Facultad']}' no existe."},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                        # Check for existing Escuela instance
                        existing_escuela = Escuela.objects.filter(
                            nombre=row['Nombre'].strip(),
                            estado=row['Estado'].strip(),
                            UniversidadCodigo=universidad,
                            facultadCodigo=facultad
                        ).first()

                        if existing_escuela:
                            continue  # Skip if a duplicate exists

                        # Create Escuela instance
                        escuela_instance = Escuela(
                            nombre=row['Nombre'].strip(),
                            estado=row['Estado'].strip(),
                            UniversidadCodigo=universidad,
                            facultadCodigo=facultad
                        )
                        records_to_create.append(escuela_instance)

                    except Universidad.DoesNotExist:
                        return Response(
                            {"error": f"Universidad con nombre '{row['Universidad']}' no existe."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    except KeyError as e:
                        return Response(
                            {"error": f"Falta los datos columna: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    except Exception as e:
                        return Response(
                            {"error": f"Error processing row: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                # Bulk create the records in the database
                if records_to_create:
                    Escuela.objects.bulk_create(records_to_create)
                    records_created = len(records_to_create)

            return Response(
                {"message": f"Se han importado {records_created} registros."},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ImportDocente(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No se envió un archivo Excel"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)  # Fixed: 'pd' → 'pd'

            required_columns = [
                'Nombre', 'Apellidos', 'Sexo', 'Estado Civil', 'Fecha de nacimiento',
                'Telefono', 'Direccion', 'Estado', 'Universidad', 'Facultad', 'Escuela',
                'Tipo de docente', 'Categoria docente'
            ]
            # Check if all required columns are present
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Faltan las columnas: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():  # Atomic transaction for batch operations
                # Get all related objects in a single query to avoid repetitive queries
                universidades = {u.nombre.strip(): u for u in Universidad.objects.all()}
                facultades = {f.nombre.strip(): f for f in Facultad.objects.all()}
                escuelas = {e.nombre.strip(): e for e in Escuela.objects.all()}
                tipos_docente = {t.nombre.strip(): t for t in TipoDocente.objects.all()}
                categorias_docente = {c.nombre.strip(): c for c in CategoriaDocente.objects.all()}

                records_to_create = []
                records_created = 0

                for _, row in df.iterrows():
                    try:
                        universidad = universidades.get(str(row['Universidad']).strip())
                        facultad = facultades.get(str(row['Facultad']).strip())
                        escuela = escuelas.get(str(row['Escuela']).strip())
                        tipo_docente = tipos_docente.get(str(row['Tipo de docente']).strip())
                        categoria_docente = categorias_docente.get(str(row['Categoria docente']).strip())

                        # Validate existence of foreign keys
                        if not universidad:
                            return Response({"error": f"Universidad '{row['Universidad']}' no existe."}, status=status.HTTP_400_BAD_REQUEST)
                        if not facultad:
                            return Response({"error": f"Facultad '{row['Facultad']}' no existe."}, status=status.HTTP_400_BAD_REQUEST)
                        if not escuela:
                            return Response({"error": f"Escuela '{row['Escuela']}' no existe."}, status=status.HTTP_400_BAD_REQUEST)
                        if not tipo_docente:
                            return Response({"error": f"Tipo de docente '{row['Tipo de docente']}' no existe."}, status=status.HTTP_400_BAD_REQUEST)
                        if not categoria_docente:
                            return Response({"error": f"Categoría docente '{row['Categoria docente']}' no existe."}, status=status.HTTP_400_BAD_REQUEST)

                        # Check for duplicates before inserting
                        if Docente.objects.filter(
                            nombre=str(row['Nombre']).strip(),
                            apellidos=str(row['Apellidos']).strip(),
                            sexo=str(row['Sexo']).strip(),
                            estado_civil=str(row['Estado Civil']).strip(),
                            fecha_nacimiento=row['Fecha de nacimiento'],
                            telefono=str(row['Telefono']).strip(),
                            direccion=str(row['Direccion']).strip(),
                            estado=str(row['Estado']).strip(),
                            UniversidadCodigo=universidad
                        ).exists():
                            continue  # Skip duplicate entry

                        # Create new Docente instance
                        docente_instance = Docente(
                            nombre=str(row['Nombre']).strip(),
                            apellidos=str(row['Apellidos']).strip(),
                            sexo=str(row['Sexo']).strip(),
                            estado_civil=str(row['Estado Civil']).strip(),
                            fecha_nacimiento=row['Fecha de nacimiento'],
                            telefono=str(row['Telefono']).strip(),
                            direccion=str(row['Direccion']).strip(),
                            estado=str(row['Estado']).strip(),
                            UniversidadCodigo=universidad,
                            facultadCodigo=facultad,
                            escuelaCodigo=escuela,
                            tipoDocenteCodigo=tipo_docente,
                            categoriaCodigo=categoria_docente
                        )
                        records_to_create.append(docente_instance)

                    except KeyError as e:
                        return Response({"error": f"Faltan datos en la columna: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return Response({"error": f"Error en la fila {row['Nombre']}: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

                # Bulk insert for better performance
                if records_to_create:
                    Docente.objects.bulk_create(records_to_create)
                    records_created = len(records_to_create)

            return Response({"message": f"Se han importado {records_created} registros"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Ocurrió un error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImportAsignacion(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        period = request.data.get("period")
        if not period:
            return Response({"error": "Periodo es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            return Response({"error": "No excel enviado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)

            required_columns = [
                "NRC", "Clave", "Asignatura", "Codigo", "Profesor", "Seccion", "Modalidad",
                "Campus", "Facultad", "Escuela", "Tipo", "Cupo", "Inscripto", "Horario", "Dias",
                "Aula", "Creditos",
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Missing required columns: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch all Facultad, Escuela, and Docente objects beforehand
            facultades = {f.nombre.strip().lower(): f for f in Facultad.objects.all()}
            escuelas = {e.nombre.strip().lower(): e for e in Escuela.objects.all()}
            docentes = {f"{d.nombre.strip()} {d.apellidos.strip()}".lower(): d for d in Docente.objects.all()}

            records_to_create = []
            failed_rows = []
            duplicates = []

            # First pass: Validate all rows
            for _, row in df.iterrows():
                try:
                    # Retrieve Facultad & Escuela
                    facultad_nombre = row["Facultad"].strip().lower()
                    escuela_nombre = row["Escuela"].strip().lower()

                    facultad = facultades.get(facultad_nombre)
                    escuela = escuelas.get(escuela_nombre)

                    # Process docente name
                    full_name = row["Profesor"].strip().split()
                    if len(full_name) < 2:
                        failed_rows.append(f"Docente name '{row['Profesor']}' is invalid.")
                        continue

                    nombre = " ".join(full_name[:-1]).strip()  # Everything except last word
                    apellidos = full_name[-1].strip()  # Last word
                    docente_nombre = f"{nombre} {apellidos}".lower()
                    docente = docentes.get(docente_nombre)

                    if not facultad:
                        failed_rows.append(f"Facultad '{facultad_nombre}' no existe.")
                    if not escuela:
                        failed_rows.append(f"Escuela '{escuela_nombre}' no existe.")
                    if not docente:
                        failed_rows.append(f"El docente '{nombre} {apellidos}' no existe.")

                    # If any required entity is missing, skip this row
                    if not facultad or not escuela or not docente:
                        continue

                    # Check for duplicate record
                    existing_record = AsignacionDocente.objects.filter(
                        nrc=row["NRC"],
                        clave=row["Clave"],
                        codigo=row["Codigo"],
                        period=period
                    ).exists()

                    if existing_record:
                        duplicates.append(f"Registro duplicado encontrado: NRC {row['NRC']}, Clave {row['Clave']}, Codigo {row['Codigo']}")
                        continue

                    # Prepare the record for bulk creation
                    records_to_create.append(
                        AsignacionDocente(
                            nrc=row["NRC"],
                            clave=row["Clave"],
                            asignatura=row["Asignatura"],
                            codigo=row["Codigo"],
                            DocenteCodigo=docente,
                            seccion=row["Seccion"],
                            modalidad=row["Modalidad"],
                            campus=row["Campus"],
                            facultadCodigo=facultad,
                            escuelaCodigo=escuela,
                            tipo=row["Tipo"],
                            cupo=row["Cupo"],
                            inscripto=row["Inscripto"],
                            horario=row["Horario"],
                            dias=row["Dias"],
                            Aula=row["Aula"],
                            creditos=row["Creditos"],
                            period=period,
                        )
                    )

                except KeyError as e:
                    failed_rows.append(f"Falta el dato: {str(e)}")
                except Exception as e:
                    failed_rows.append(f"Error processing row {row.to_dict()}: {str(e)}")

            # If there are any failed rows, return the error response without creating any records
            if failed_rows:
                return Response(
                    {"error": "No se han importado registros. Errores encontrados:", "failed_records": failed_rows},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Perform a bulk create of all records if there are any valid records to create
            if records_to_create:
                with transaction.atomic():
                    AsignacionDocente.objects.bulk_create(records_to_create)

            response_data = {
                "message": f"Se han importado {len(records_to_create)} registros.",
                "duplicate_records": duplicates,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class ImportUniversidad(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No excel enviado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)

            required_columns = ['Nombre', 'Estado']
            # Check if all required columns are present
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Falta la columna: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            records_to_create = []
            failed_rows = []

            for _, row in df.iterrows():
                try:
                    nombre = str(row.get('Nombre', '')).strip()
                    estado = str(row.get('Estado', '')).strip()

                    # Validate the data
                    if not nombre or not estado:
                        failed_rows.append(f"Invalid data in row: {row.to_dict()}")
                        continue

                    # Check if the record already exists
                    if Universidad.objects.filter(nombre=nombre, estado=estado).exists():
                        failed_rows.append(f"Record already exists: {nombre}, {estado}")
                        continue

                    # Create a new Universidad object
                    records_to_create.append(Universidad(nombre=nombre, estado=estado))

                except Exception as e:
                    failed_rows.append(f"Error processing row {row.to_dict()}: {str(e)}")

            # Use transaction.atomic() to ensure all or nothing
            with transaction.atomic():
                Universidad.objects.bulk_create(records_to_create)

            response_data = {
                "message": f"Se han importado {len(records_to_create)} registros.",
                "failed_records": failed_rows
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
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

class ImportFacultad(ImportData):
    model_class = Facultad

class ImportCategoriaDocente(ImportData):
    model_class = CategoriaDocente

class ImportTipoDocente(ImportData):
    model_class = TipoDocente
#endregion

@api_view(['POST'])
def copiar_asignaciones(request):
    from_period = request.data.get('from_period')
    to_period = request.data.get('to_period')

    if not from_period or not to_period:
        return Response({"error": "Parámetros inválidos"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        asignaciones_origen = AsignacionDocente.objects.filter(period=from_period)
        cantidad_origen = asignaciones_origen.count()

        if cantidad_origen == 0:
            return Response({
                "message": f"No hay asignaciones en el periodo {from_period}"
            }, status=200)

        nuevas_asignaciones = []

        for a in asignaciones_origen:
            nuevas_asignaciones.append(AsignacionDocente(
                nrc=a.nrc,
                clave=a.clave,
                asignatura=a.asignatura,
                codigo=a.codigo,
                DocenteCodigo=a.DocenteCodigo,
                seccion=a.seccion,
                modalidad=a.modalidad,
                campus=a.campus,
                facultadCodigo=a.facultadCodigo,
                escuelaCodigo=a.escuelaCodigo,
                tipo=a.tipo,
                cupo=a.cupo,
                inscripto=a.inscripto,
                horario=a.horario,
                dias=a.dias,
                Aula=a.Aula,
                creditos=a.creditos,
                period=to_period  # ✅ corregido aquí
            ))

        AsignacionDocente.objects.bulk_create(nuevas_asignaciones)

        return Response({
            "message": f"{len(nuevas_asignaciones)} asignaciones copiadas de {from_period} a {to_period}"
        }, status=201)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)