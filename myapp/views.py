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
from rest_framework.response import Response
# Create your views here.
def index(request):
  return render(request, 'client/index.html')







# APIS


# CREATE
@api_view(['POST'])
def create_Universidad(request):
  if request.method == 'POST':
    ser = UniversidadSerializer(data=request.data)
    if ser.is_valid():
      ser.save()
      return Response({"message": "Data saved successfully"})
    else:
      return Response(ser.error)
@api_view(['POST'])
def create_Facultad(request):
  if request.method == 'POST':
    ser = FacultadSerializer(data=request.data)
    if ser.is_valid():
      ser.save()
      return Response({"message": "Data saved Successfully"})
    else:
      return Response(ser.error)

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



# RETRIEVE OR READ
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



