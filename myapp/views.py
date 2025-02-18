
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .serializer import (
  UniversidadSerializer, 
  FacultadSerializer, 
  EscuelaSerializer,
  TipoDocenteSerializer,
  CategoriaDocenteSerializer,
  DocenteSerializer,
  PeriodoAcademicoSerializer,
  asignacionDocenteSerializer,
  asignacionDocenteSerializer_frontend)
from .models import (
    Universidad, 
    Facultad, 
    Escuela,  
    TipoDocente,
    CategoriaDocente, 
    Docente, 
    PeriodoAcademico,
    asignacionDocente)
from .handles import createHandle, getAllHandle, deleteHandler,getAllHandle_asignacion
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
import pandas as panda


# Create your views here.
def index(request):
  return render(request, 'client/index.html')

# HERE IS ALL THE ENDPOINTS OF THE API

#region CREATE

@api_view(['POST'])
def create_Universidad(request):
  return  createHandle(request, UniversidadSerializer)

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
  return getAllHandle_asignacion(request,asignacionDocente,asignacionDocenteSerializer)

@api_view(['GET'])
def getAllAsignacion_frontend(request):
  return getAllHandle_asignacion(request,asignacionDocente,asignacionDocenteSerializer_frontend)
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
        asignacion = asignacionDocente.objects.get(pk=pk)
    except asignacionDocente.DoesNotExist:
        return JsonResponse({'error': "Asignacion Docente No encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH']:
        # Exclude 'docente_nombre_completo' from the request data (since it's read-only)
        request_data = request.data.copy()
        request_data.pop('docente_nombre_completo', None)  # Remove 'docente_nombre_completo' if it exists

        ser = asignacionDocenteSerializer(asignacion, data=request_data, partial=(request.method == 'PATCH'))

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
        asignacion = asignacionDocente.objects.get(pk=pk)
        asignacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except asignacionDocente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_asignacion_by_period(request):
    period = request.GET.get('period')
    if not period:
        return Response({"error": "Missing period"}, status=status.HTTP_400_BAD_REQUEST)
    deleted_count, _ = asignacionDocente.objects.filter(period=period).delete()
    
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
    asignacion = asignacionDocente.objects.filter(pk=pk).first()
    if asignacion is None:
        return Response({'error': 'Periodo academico not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = asignacionDocenteSerializer(asignacion)

    return Response(serializer.data, status=status.HTTP_200_OK)
#endregion

#region Auth
@api_view(['POST'])
def login_view(request):
    # Retrieve username and password from request data
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    user = authenticate(username=username, password=password)
    if user is not None:
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
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
def UniversidadExport(request):
  queryset = Universidad.objects.all()
  data = []

  for universidad in queryset:
    data.append({
      'Nombre': universidad.nombre,
      'Estado': universidad.estado
    })

  response = HttpResponse(content_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename="universidad_data.xlsx"'

  # pandas is a data analysis library for python
  with panda.ExcelWriter(response, engine='openpyxl') as writer:
        panda.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)

  return response

def FacultadExport(request):
  queryset = Facultad.objects.all()
  data = []

  for facultad in queryset:
    data.append({
      'Nombre': facultad.nombre,
      'Estado': facultad.estado,
      'Universidad': facultad.UniversidadCodigo.nombre

    })

  response = HttpResponse(content_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename="facultad_data.xlsx"'

  with panda.ExcelWriter(response, engine='openpyxl') as writer:
    panda.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)

  return response

def EscuelaExport(request):
  queryset = Escuela.objects.all()
  data = []

  for escuela in queryset:
    data.append({
      'Nombre': escuela.nombre,
      'Estado': escuela.estado,
      'Universidad': escuela.UniversidadCodigo.nombre,
      'Facultad': escuela.facultadCodigo.nombre
    })

  response = HttpResponse(content_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename="escuela_data.xlsx"'

  with panda.ExcelWriter(response, engine='openpyxl') as writer:
    panda.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)

  return response

def DocenteExport(request):
  queryset = Docente.objects.all()
  data = []

  for docente in queryset:
    data.append({
      'Nombre': docente.nombre,
      'Apellidos': docente.apellidos,
      'Sexo': docente.sexo,
      'Estado Civil': docente.estado_civil,
      'Fecha de nacimiento': docente.fecha_nacimiento,
      'Telefono': docente.telefono,
      'Direccion': docente.direccion,
      'Estado': docente.estado,
      'Universidad': docente.UniversidadCodigo.nombre,
      'Facultad': docente.facultadCodigo.nombre,
      'Escuela': docente.escuelaCodigo.nombre,
      'Tipo de docente': docente.tipoDocenteCodigo.nombre,
      'Categoria docente': docente.categoriaCodigo.nombre,
    })

  response = HttpResponse(content_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename="Docente_data.xlsx"'

  with panda.ExcelWriter(response, engine='openpyxl') as writer:
    panda.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)

  return response

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

  with panda.ExcelWriter(response, engine='openpyxl') as writer:
    panda.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)

  return response

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
    
    with panda.ExcelWriter(response, engine='openpyxl') as writer:
        panda.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)
    
    return response

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
    
    with panda.ExcelWriter(response, engine='openpyxl') as writer:
        panda.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)
    return response




@api_view(["GET"])
def asignacionDocenteExport(request):
    # Get the period from request
    period = request.GET.get("period")

    # Filter by period if provided
    queryset = asignacionDocente.objects.select_related("facultadCodigo", "escuelaCodigo", "DocenteCodigo")
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

    with panda.ExcelWriter(response, engine="openpyxl") as writer:
        panda.DataFrame(data).to_excel(writer, sheet_name="Sheet1", index=False)

    return response
#endregion

#region Import
class ImportFacultad(APIView):
  parser_classes = [MultiPartParser, FormParser]

  def post(self, request, *args, **kwargs):
    excel_file = request.FILES.get('excel_file')
    if not excel_file:
        return Response({"error": "No excel enviado"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Read the Excel file
        df = panda.read_excel(excel_file)

        required_columns = ['Nombre', 'Estado', 'Universidad']
        # Check if all required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response(
                {"error": f"Falta la columna {', '.join(missing_columns)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        records_created = 0
        for _, row in df.iterrows():
            try:
              universidad = Universidad.objects.get(nombre=row['Universidad'])

              obj, created = Facultad.objects.get_or_create(
                  nombre=row['Nombre'],
                  estado=row['Estado'],
                  UniversidadCodigo=universidad
              )
              if created:
                records_created += 1
            except Universidad.DoesNotExist:
              return Response(
                  {"error": f"Universidad con nombre {row['Universidad']} no existe."},
                  status=status.HTTP_400_BAD_REQUEST
              )
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
        return Response(
            {"message": f"se han Importados {records_created} registros."},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class ImportEscuela(APIView):
  parser_classes = [MultiPartParser, FormParser]

  def post(self, request, *args, **kwargs):
    excel_file = request.FILES.get('excel_file')
    if not excel_file:
        return Response({"error": "No excel enviado."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Read the Excel file
        df = panda.read_excel(excel_file)

        required_columns = ['Nombre', 'Estado', 'Universidad', 'Facultad']
        # Check if all required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response(
                {"error": f"Falta una columna: {', '.join(missing_columns)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        records_created = 0
        for _, row in df.iterrows():
            try:
              universidad = Universidad.objects.get(nombre=row['Universidad'])
              facultad = Facultad.objects.get(nombre=row['Facultad'])

              obj, created = Escuela.objects.get_or_create(
                  nombre=row['Nombre'],
                  estado=row['Estado'],
                  UniversidadCodigo=universidad,
                  facultadCodigo=facultad
              )
              if created:
                records_created += 1
            except Universidad.DoesNotExist:
              return Response(
                  {"error": f"Universidad con nombre {row['UniversidadCodigo']} no existe."},
                  status=status.HTTP_400_BAD_REQUEST
              )
            except Facultad.DoesNotExist:
              return Response(
                  {"error": f"Facultad con nombre {row['Facultad']} no existe."},
                  status=status.HTTP_400_BAD_REQUEST
              )
            except KeyError as e:
              return Response(
                  {"error": f"falta los datos columna: {str(e)}"},
                  status=status.HTTP_400_BAD_REQUEST
              )
            except Exception as e:
              return Response(
                  {"error": f"Error processing row: {str(e)}"},
                  status=status.HTTP_400_BAD_REQUEST
              )
        return Response(
            {"message": f"se han Importado {records_created} registros."},
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
            return Response({"error": "No excel enviado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file
            df = panda.read_excel(excel_file)

            required_columns = [
                'Nombre', 'Apellidos', 'Sexo', 'Estado Civil', 'Fecha de nacimiento',
                'Telefono', 'Direccion', 'Estado', 'Universidad', 'Facultad', 'Escuela',
                'Tipo de docente', 'Categoria docente'
            ]
            # Check if all required columns are present
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Falta la columna : {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            records_created = 0
            for _, row in df.iterrows():
                try:
                    
                    universidad = Universidad.objects.get(nombre=row['Universidad'])
                    facultad = Facultad.objects.get(nombre=row['Facultad'])
                    escuela = Escuela.objects.get(nombre=row['Escuela'])
                    tipoDocente = TipoDocente.objects.get(nombre=row['Tipo de docente'])
                    categoriaDocente = CategoriaDocente.objects.get(nombre=row['Categoria docente'])

                    obj, created = Docente.objects.get_or_create(
                        nombre=row['Nombre'],
                        apellidos=row['Apellidos'],
                        sexo=row['Sexo'],
                        estado_civil=row['Estado Civil'],
                        fecha_nacimiento=row['Fecha de nacimiento'],
                        telefono=row['Telefono'],
                        direccion=row['Direccion'],
                        estado=row['Estado'],
                        UniversidadCodigo=universidad,
                        facultadCodigo=facultad,
                        escuelaCodigo=escuela,
                        tipoDocenteCodigo=tipoDocente,
                        categoriaCodigo=categoriaDocente
                    )
                    if created:
                        records_created += 1
                except Universidad.DoesNotExist:
                    return Response(
                        {"error": f"Universidad con nombre {row['Universidad']} no existe."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Facultad.DoesNotExist:
                    return Response(
                        {"error": f"Facultad con nombre {row['Facultad']} no existe."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Escuela.DoesNotExist:
                    return Response(
                        {"error": f"Escuela con nombre {row['Escuela']} no existe."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except TipoDocente.DoesNotExist:
                    return Response(
                        {"error": f"Tipo de docente con nombre {row['Tipo de docente']} no existe."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except CategoriaDocente.DoesNotExist:
                    return Response(
                        {"error": f"Categoria docente con nombre {row['Categoria docente']} no existe."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except KeyError as e:
                    return Response(
                        {"error": f"falta los datos de la columna: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            return Response(
                {"error": f"Error processing row: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": f"se han importados {records_created} registros"},
            status=status.HTTP_201_CREATED
        )

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
            df = panda.read_excel(excel_file)

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
            facultades = {f.nombre: f for f in Facultad.objects.all()}
            escuelas = {e.nombre: e for e in Escuela.objects.all()}
            docentes = {f"{d.nombre} {d.apellidos}": d for d in Docente.objects.all()}

            records_to_create = []
            for _, row in df.iterrows():
                try:
                    # Retrieve Facultad & Escuela
                    facultad = facultades.get(row["Facultad"].strip())
                    escuela = escuelas.get(row["Escuela"].strip())

                    # Process docente name
                    full_name = row["Profesor"].strip().split()
                    if len(full_name) < 2:
                        return Response(
                            {"error": f"Docente name '{row['Profesor']}' is invalid."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    nombre = " ".join(full_name[:-1])  # Everything except last word
                    apellidos = full_name[-1]  # Last word

                    docente = docentes.get(f"{nombre} {apellidos}")
                    if not docente:
                        return Response(
                            {"error": f"El docente '{nombre} {apellidos}' No existe."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # Prepare the record for bulk creation
                    records_to_create.append(
                        asignacionDocente(
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
                    return Response(
                        {"error": f"Falta el dato: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Perform a bulk create of all records
            with transaction.atomic():
                asignacionDocente.objects.bulk_create(records_to_create)

            return Response(
                {"message": f"Se han importado {len(records_to_create)} registros"},
                status=status.HTTP_201_CREATED,
            )

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
            df = panda.read_excel(excel_file)

            required_columns = ['Nombre', 'Estado']
            # Check if all required columns are present
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Falta la columna: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            records_created = 0
            for _, row in df.iterrows():

                nombre = str(row.get('Nombre', '')).strip()
                estado = str(row.get('Estado', '')).strip()
                try:
                    obj, created = Universidad.objects.get_or_create(
                        nombre=nombre,
                        estado=estado
                    )
                    if created:
                        records_created += 1
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

            return Response(
                {"message": f"se han importados {records_created} registros"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImportTipoDocente(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No excel enviado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file
            df = panda.read_excel(excel_file)

            required_columns = ['Nombre', 'Estado', 'Universidad']
            # Check if all required columns are present
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Falta la columna: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            records_created = 0
            for _, row in df.iterrows():
                try:
                    universidad = Universidad.objects.get(nombre=row['Universidad'])

                    obj, created = TipoDocente.objects.get_or_create(
                        nombre=row['Nombre'],
                        estado=row['Estado'],
                        UniversidadCodigo=universidad
                    )
                    if created:
                        records_created += 1
                except Universidad.DoesNotExist:
                    return Response(
                        {"error": f"Universidad con nombre {row['Universidad']} no existe."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
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

            return Response(
                {"message": f"se han importados {records_created} registros"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImportCategoriaDocente(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No excel enviado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file
            df = panda.read_excel(excel_file)

            required_columns = ['Nombre', 'Estado', 'Universidad']
            # Check if all required columns are present
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Falta la columna: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            records_created = 0
            for _, row in df.iterrows():
                try:
                    universidad = Universidad.objects.get(nombre=row['Universidad'])

                    obj, created = CategoriaDocente.objects.get_or_create(
                        nombre=row['Nombre'],
                        estado=row['Estado'],
                        UniversidadCodigo=universidad
                    )
                    if created:
                        records_created += 1
                except Universidad.DoesNotExist:
                    return Response(
                        {"error": f"Universidad con nombre {row['Universidad']} no existe."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
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

            return Response(
                {"message": f"se han importados {records_created} registros"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#endregion