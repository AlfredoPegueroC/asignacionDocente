
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
  asignacionDocenteSerializer)
from .models import (
    Universidad, 
    Facultad, 
    Escuela,  
    TipoDocente,
    CategoriaDocente, 
    Docente, 
    PeriodoAcademico,
    asignacionDocente)
from .handles import createHandle, getAllHandle
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth import authenticate
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
  return getAllHandle(request,asignacionDocente,asignacionDocenteSerializer)
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
        Escuela.delete()
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

        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    
    except TokenError as e:  # Handles case if the token is invalid or already blacklisted
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
      'nombre': universidad.nombre,
      'estado': universidad.estado
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
      'categoria docente': docente.categoriaCodigo.nombre,
    })

  response = HttpResponse(content_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename="Docente_data.xlsx"'

  with panda.ExcelWriter(response, engine='openpyxl') as writer:
    panda.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)

  return response

def asignacionDocenteExport(request):
    queryset = asignacionDocente.objects.select_related('facultadCodigo', 'escuelaCodigo', 'DocenteCodigo').all()
    data = []

    for asignacion in queryset:
      data.append({
        'NRC': asignacion.nrc,
        'Clave': asignacion.clave,
        'Asignatura': asignacion.asignatura,
        'Código': asignacion.codigo,
        'Sección': asignacion.seccion,
        'Modalidad': asignacion.modalidad,
        'Campus': asignacion.campus,
        'Tipo': asignacion.tipo,
        'Cupo': asignacion.cupo,
        'Inscripto': asignacion.inscripto,
        'Horario': asignacion.horario,
        'Aula': asignacion.Aula,
        'Créditos': asignacion.creditos,
        'Facultad': asignacion.facultadCodigo.nombre if asignacion.facultadCodigo else None,
        'Escuela': asignacion.escuelaCodigo.nombre if asignacion.escuelaCodigo else None,
        'Docente': asignacion.DocenteCodigo.nombre if asignacion.DocenteCodigo else None,
      })

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Asignacion_data.xlsx"'

    with panda.ExcelWriter(response, engine='openpyxl') as writer:
        panda.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)

    return response


#endregion

#region Import
class ImportAsignacion(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        period = request.data.get('period')  # Retrieve the period
        if not period:
            return Response({"error": "Period is required"}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file
            df = panda.read_excel(excel_file)

            required_columns = [
                'nrc', 'clave', 'asignatura', 'codigo', 'seccion', 'modalidad',
                'campus', 'tipo', 'cupo', 'inscripto', 'horario', 'dias',
                'Aula', 'creditos', 'facultadNombre', 'escuelaNombre', 'docenteNombre'
            ]

            # Check if all required columns are present
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {"error": f"Missing required columns: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            records_created = 0
            for _, row in df.iterrows():
                try:
                    # Fetch Facultad, Escuela, and Docente using their 'nombre'
                    facultad = Facultad.objects.get(nombre=row['facultadNombre'])
                    escuela = Escuela.objects.get(nombre=row['escuelaNombre'])
                    docente = Docente.objects.get(nombre=row['docenteNombre'])

                    # Create or get the asignacionDocente record
                    obj, created = asignacionDocente.objects.get_or_create(
                        nrc=row['nrc'],
                        clave=row['clave'],
                        asignatura=row['asignatura'],
                        codigo=row['codigo'],
                        seccion=row['seccion'],
                        modalidad=row['modalidad'],
                        campus=row['campus'],
                        tipo=row['tipo'],
                        cupo=row['cupo'],
                        inscripto=row['inscripto'],
                        horario=row['horario'],
                        dias=row['dias'],
                        Aula=row['Aula'],
                        creditos=row['creditos'],
                        facultadCodigo=facultad,  # Associate the fetched Facultad
                        escuelaCodigo=escuela,  # Associate the fetched Escuela
                        DocenteCodigo=docente,  # Associate the fetched Docente
                        period=period  # Store the period
                    )
                    if created:
                        records_created += 1
                except Facultad.DoesNotExist:
                    return Response(
                        {"error": f"Facultad with nombre {row['facultadNombre']} does not exist."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Escuela.DoesNotExist:
                    return Response(
                        {"error": f"Escuela with nombre {row['escuelaNombre']} does not exist."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Docente.DoesNotExist:
                    return Response(
                        {"error": f"Docente with nombre {row['docenteNombre']} does not exist."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except KeyError as e:
                    return Response(
                        {"error": f"Missing data for column: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Exception as e:
                    return Response(
                        {"error": f"Error processing row: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(
                {"message": f"Successfully imported {records_created} records."},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#endregion