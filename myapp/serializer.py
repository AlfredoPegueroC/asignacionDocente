from rest_framework import serializers
from .models import Universidad, Facultad, Escuela, TipoDocente, CategoriaDocente, Docente, PeriodoAcademico

# Universidad Serializer
class UniversidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidad
        fields = ['UniversidadCodigo', 'nombre', 'estado']

# Facultad Serializer
class FacultadSerializer(serializers.ModelSerializer):
    UniversidadCodigo = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())

    class Meta:
        model = Facultad
        fields = ['facultadCodigo', 'nombre', 'estado', 'UniversidadCodigo']

# Escuela Serializer
class EscuelaSerializer(serializers.ModelSerializer):
    UniversidadCodigo = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    facultadCodigo = serializers.PrimaryKeyRelatedField(queryset=Facultad.objects.all()) 

    class Meta:
        model = Escuela
        fields = ['escuelaCodigo', 'nombre', 'estado', 'UniversidadCodigo', 'facultadCodigo']

# TipoDocente Serializer
class TipoDocenteSerializer(serializers.ModelSerializer):
    UniversidadCodigo = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())

    class Meta:
        model = TipoDocente
        fields = ['tipoDocenteCodigo', 'nombre', 'estado', 'UniversidadCodigo']

# CategoriaDocente Serializer
class CategoriaDocenteSerializer(serializers.ModelSerializer):
    UniversidadCodigo = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())

    class Meta:
        model = CategoriaDocente
        fields = ['categoriaCodigo', 'nombre', 'estado', 'UniversidadCodigo']

# Docente Serializer
class DocenteSerializer(serializers.ModelSerializer):
    UniversidadCodigo = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    facultadCodigo = serializers.PrimaryKeyRelatedField(queryset=Facultad.objects.all())
    escuelaCodigo = serializers.PrimaryKeyRelatedField(queryset=Escuela.objects.all())
    tipoDocenteCodigo = serializers.PrimaryKeyRelatedField(queryset=TipoDocente.objects.all())
    categoriaCodigo = serializers.PrimaryKeyRelatedField(queryset=CategoriaDocente.objects.all())

    class Meta:
        model = Docente
        fields = [
            'Docentecodigo', 'nombre', 'apellidos', 'sexo', 'estado_civil', 'fecha_nacimiento', 'telefono', 
            'direccion', 'estado', 'UniversidadCodigo', 'facultadCodigo', 'escuelaCodigo', 'tipoDocenteCodigo', 
            'categoriaCodigo'
        ]

# PeriodoAcademico Serializer
class PeriodoAcademicoSerializer(serializers.ModelSerializer):
    UniversidadCodigo = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())

    class Meta:
        model = PeriodoAcademico
        fields = ['periodoAcademicoCodigo', 'nombre', 'anio', 'fechaIni', 'fechaFinal', 'estado', 'UniversidadCodigo']
