from rest_framework import serializers
from .models import Universidad, Facultad, Escuela, TipoDocente, CategoriaDocente, Docente, PeriodoAcademico

# Universidad Serializer
class UniversidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidad
        fields = ['UniversidadCodigo', 'nombre', 'estado']

# Facultad Serializer
class FacultadSerializer(serializers.ModelSerializer):
    UniversidadCodigo = UniversidadSerializer()

    class Meta:
        model = Facultad
        fields = ['facultadCodigo', 'nombre', 'estado', 'UniversidadCodigo']

# Escuela Serializer
class EscuelaSerializer(serializers.ModelSerializer):
    UniversidadCodigo = UniversidadSerializer()
    facultadCodigo = FacultadSerializer()

    class Meta:
        model = Escuela
        fields = ['escuelaCodigo', 'nombre', 'estado', 'UniversidadCodigo', 'facultadCodigo']

# TipoDocente Serializer
class TipoDocenteSerializer(serializers.ModelSerializer):
    UniversidadCodigo = UniversidadSerializer()

    class Meta:
        model = TipoDocente
        fields = ['tipoDocenteCodigo', 'nombre', 'estado', 'UniversidadCodigo']

# CategoriaDocente Serializer
class CategoriaDocenteSerializer(serializers.ModelSerializer):
    UniversidadCodigo = UniversidadSerializer()

    class Meta:
        model = CategoriaDocente
        fields = ['categoriaCodigo', 'nombre', 'estado', 'UniversidadCodigo']

# Docente Serializer
class DocenteSerializer(serializers.ModelSerializer):
    UniversidadCodigo = UniversidadSerializer()
    facultadCodigo = FacultadSerializer()
    escuelaCodigo = EscuelaSerializer()
    tipoDocenteCodigo = TipoDocenteSerializer()
    categoriaCodigo = CategoriaDocenteSerializer()

    class Meta:
        model = Docente
        fields = [
            'DocenteCodigo', 'nombre', 'apellidos', 'sexo', 'estado_civil', 'fecha_nacimiento', 'telefono', 
            'direccion', 'estado', 'UniversidadCodigo', 'facultadCodigo', 'escuelaCodigo', 'tipoDocenteCodigo', 
            'categoriaCodigo'
        ]

# PeriodoAcademico Serializer
class PeriodoAcademicoSerializer(serializers.ModelSerializer):
    UniversidadCodigo = UniversidadSerializer()

    class Meta:
        model = PeriodoAcademico
        fields = ['periodoAcademicoCodigo', 'nombre', 'anio', 'fechaIni', 'fechaFinal', 'estado', 'UniversidadCodigo']
