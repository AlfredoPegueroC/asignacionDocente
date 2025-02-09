from rest_framework import serializers
from .models import Universidad, Facultad, Escuela, TipoDocente, CategoriaDocente, Docente, PeriodoAcademico, asignacionDocente

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
        fields = ['periodoAcademicoCodigo', 'nombre', 'estado', 'UniversidadCodigo']

class asignacionDocenteSerializer(serializers.ModelSerializer):
    facultadCodigo = serializers.PrimaryKeyRelatedField(queryset=Facultad.objects.all())
    escuelaCodigo = serializers.PrimaryKeyRelatedField(queryset=Escuela.objects.all())
    DocenteCodigo = serializers.PrimaryKeyRelatedField(queryset=Docente.objects.all())

    class Meta:
        model = asignacionDocente
        fields = ['ADIDcodigo','nrc', 'clave', 'asignatura', 'codigo', 'seccion', 'modalidad', 'campus', 'tipo', 'cupo', 'inscripto', 'horario','dias', 'Aula', 'creditos', 'facultadCodigo', 'escuelaCodigo', 'DocenteCodigo', 'period']


class asignacionDocenteSerializer_frontend(serializers.ModelSerializer):
    facultadCodigo = serializers.CharField(source='facultadCodigo.nombre')
    escuelaCodigo = serializers.CharField(source='escuelaCodigo.nombre')
    docente_nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = asignacionDocente
        fields = ['ADIDcodigo', 'nrc', 'clave', 'asignatura', 'codigo', 'seccion', 'modalidad', 
                  'campus', 'tipo', 'cupo', 'inscripto', 'horario', 'dias', 'Aula', 'creditos', 
                  'facultadCodigo', 'escuelaCodigo', 'docente_nombre_completo', 'period']

    def get_docente_nombre_completo(self, obj):
        # Assuming 'DocenteCodigo' is a ForeignKey to Docente model
        docente = obj.DocenteCodigo  # Get the related Docente instance
        if docente:
            return f"{docente.nombre} {docente.apellidos}"  # Combine nombre and apellidos
        return None  