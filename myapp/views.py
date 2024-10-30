from django.shortcuts import render
from .serializer import (
  UniversidadSerializer, 
  FacultadSerializer, 
  EscuelaSerializer,
  TipoDocenteSerializer,
  CategoriaDocenteSerializer,
  DocenteSerializer,
  PeriodoAcademicoSerializer)
from .models import (
    Universidad, 
    Facultad, 
    Escuela,  
    TipoDocente,
    CategoriaDocente, 
    Docente, 
    PeriodoAcademico)
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
def index(request):
  return render(request, 'client/index.html')

# HERE IS ALL THE APIS

#region CREATE
@api_view(['POST'])
def create_Universidad(request):
  if request.method == 'POST':
    serializer = UniversidadSerializer(data=request.data)   
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_Facultad(request):
  if request.method == 'POST':
    serializer = FacultadSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_Escuela(request):
  if request.method == 'POST':
    ser = EscuelaSerializer(data=request.data)
    if ser.is_valid():
      ser.save()
      return Response({"message": "Data saved successfully"})
    else:
      return Response(ser.error)
@api_view(['POST'])
def create_TipoDocente(request):
  if request.method == 'POST':
    ser = TipoDocenteSerializer(data=request.data)
    if ser.is_valid():
      ser.save()
      return Response({"message": "Data saved Successfully"})
    else:
      return Response(ser.error)

@api_view(['POST'])
def create_CategoriaDocente(request):
  if request.methond == 'POST':
    ser = CategoriaDocenteSerializer(data=request.data)
    if ser.is_valid():
      ser.save()
      return Response({'message': 'Data saved Successfully'})
    else:
      return Response(ser.error)

@api_view(['POST'])
def create_Docente(request):
  if request.methond == 'POST':
    ser = DocenteSerializer(data=request.data)
    if ser.is_valid():
      ser.save()
      return Response({'message': 'Data saved Successfully'})
    else:
      return Response(ser.error)

@api_view(['POST'])
def create_PeriodoAcademico(request):
  if request.methond == 'POST':
    ser = PeriodoAcademicoSerializer(data=request.data)
    if ser.is_valid():
      ser.save()
      return Response({'message': 'Data saved Successfully'})
    else:
      return Response(ser.error)
#endregion


#region RETRIEVE OR READ
@api_view(['GET'])
def getAllUniversidad(request):
  lista = Universidad.objects.all()
  ser = UniversidadSerializer(lista, many=True)
  return Response(ser.data)

@api_view(['GET'])
def getAllFacultad(request):
  lista = Facultad.objects.all()
  ser = FacultadSerializer(lista, many=True)
  return Response(ser.data)

@api_view(['GET'])
def getAllEscuela(request):
  lista = Escuela.objects.all()
  ser = EscuelaSerializer(lista, many=True)
  return Response(ser.data)

@api_view(['GET'])
def getAllTipoDocente(request):
  lista = TipoDocente.objets.all()
  ser = TipoDocenteSerializer(lista, many=True)
  return Response(ser.data)

@api_view(['GET'])
def getAllCategoriaDocente(request):
  lista = CategoriaDocente.objects.all()
  ser = CategoriaDocenteSerializer(lista, many=True)
  return Response(ser.data)

@api_view(['GET'])
def getAllDocente(request):
  lista = Docente.objetcts.all()
  ser = DocenteSerializer(lista, many=True)
  return Response(ser.data)

@api_view(['GET'])
def getAllPeriodoAcademico(request):
  lista = PeriodoAcademico.objects.all()
  ser = PeriodoAcademicoSerializer(lista, many=True)
  return Response(ser.data)
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
      ser = EscuelaSerializer(Escuela, data=request.data, partial=(request.method == 'PATCH'))
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
      ser = DocenteSerializer(categoriaDocente, data=request.data, partial=(request.method == 'PATCH'))
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
        universidad.delete()
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

#region Auth
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

#endregion
