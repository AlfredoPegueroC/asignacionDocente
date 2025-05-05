from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Universidad,Campus, Facultad, Escuela, TipoDocente, CategoriaDocente, Docente, PeriodoAcademico, AsignacionDocente

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name', 'last_name',  'is_staff', 'is_active','groups']

# Universidad Serializer
class UniversidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidad
        fields = [
            'UniversidadID',
            'UniversidadCodigo',
            'UniversidadNombre',
            'UniversidadDireccion',
            'UniversidadTelefono',
            'UniversidadEmail',
            'UniversidadSitioWeb',
            'UniversidadRector',
            'UniversidadFechaRegistro',
            'UsuarioRegistro',
            'UniversidadEstado',
        ]

class CampusSerializer(serializers.ModelSerializer):
    Campus_UniversidadFK= serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    
    class Meta:
        model = Campus
        fields = [
            'CampusID',
            'CampusCodigo',
            'CampusNombre',
            'CampusDireccion',
            'CampusPais',
            'CampusProvincia',
            'CampusCiudad',
            'CampusTelefono',
            'CampusCorreoContacto',
            'CampusFechaRegistro',
            'UsuarioRegistro',
            'CampusEstado',
            'Campus_UniversidadFK',
        ]
# Facultad Serializer
class FacultadSerializer(serializers.ModelSerializer):
    Facultad_UniversidadFK = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    Facultad_CampusFK = serializers.PrimaryKeyRelatedField(queryset=Campus.objects.all())
    universidadNombre = serializers.CharField(
        source='Facultad_UniversidadFK.UniversidadNombre', read_only=True
    )
    campusNombre = serializers.CharField(
        source='Facultad_CampusFK.CampusNombre', read_only=True
    )

    class Meta:
        model = Facultad
        fields = [
            'FacultadID',
            'FacultadCodigo',
            'FacultadNombre',
            'FacultadDecano',
            'FacultadDireccion',
            'FacultadTelefono',
            'FacultadEmail',
            'FacultadFechaRegistro',
            'UsuarioRegistro',
            'FacultadEstado',
            'Facultad_UniversidadFK',
            'Facultad_CampusFK',
            "universidadNombre",  
            "campusNombre",
        ]

# Escuela Serializer
class EscuelaSerializer(serializers.ModelSerializer):
    Escuela_UniversidadFK = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    Escuela_facultadFK = serializers.PrimaryKeyRelatedField(queryset=Facultad.objects.all()) 

    universidadNombre = serializers.CharField(source='Escuela_UniversidadFK.UniversidadNombre', read_only=True)
    facultadNombre = serializers.CharField(source='Escuela_facultadFK.FacultadNombre', read_only=True)

    class Meta:
        model = Escuela
        fields = [
            'EscuelaId',
            'EscuelaCodigo',
            'EscuelaNombre',
            'EscuelaDirectora',
            'EscuelaTelefono',
            'EscuelaCorreo',
            'EscuelaFechaRegistro',
            'UsuarioRegistro',
            'EscuelaEstado',
            'Escuela_UniversidadFK',
            'Escuela_facultadFK',
            'universidadNombre',
            'facultadNombre',
        ]


# TipoDocente Serializer Pediente 
class TipoDocenteSerializer(serializers.ModelSerializer):
    TipoDocente_UniversidadFK = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    universidadNombre = serializers.CharField(source='TipoDocente_UniversidadFK.UniversidadNombre', read_only=True)

    class Meta:
        model = TipoDocente
        fields = [
            'TipoDocenteID',
            'TipoDocenteCodigo',
            'TipoDocenteDescripcion',
            'TipoDocenteEstado',
            'TipoFechaRegistro',
            'UsuarioRegistro',
            'TipoDocente_UniversidadFK',
            'universidadNombre',
        ]

# CategoriaDocente Serializer
class CategoriaDocenteSerializer(serializers.ModelSerializer):
    Categoria_UniversidadFK = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    universidadNombre = serializers.CharField(source='Categoria_UniversidadFK.UniversidadNombre', read_only=True)

    class Meta:
        model = CategoriaDocente
        fields = [
            'CategoriaID',
            'categoriaCodigo',
            'CategoriaNombre',
            'CategoriaEstado',
            'CategoriaFechaRegistro',
            'UsuarioRegistro',
            'Categoria_UniversidadFK',
            'universidadNombre',
        ]

# Docente Serializer
class DocenteSerializer(serializers.ModelSerializer):
    Docente_UniversidadFK = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    Docente_TipoDocenteFK = serializers.PrimaryKeyRelatedField(queryset=TipoDocente.objects.all())
    Docente_CategoriaDocenteFK = serializers.PrimaryKeyRelatedField(queryset=CategoriaDocente.objects.all())

    universidadNombre = serializers.CharField(source='Docente_UniversidadFK.UniversidadNombre', read_only=True)
    tipoDocenteNombre = serializers.CharField(source='Docente_TipoDocenteFK.TipoDocenteDescripcion', read_only=True)
    categoriaDocenteNombre = serializers.CharField(source='Docente_CategoriaDocenteFK.CategoriaNombre', read_only=True)

    class Meta:
        model = Docente
        fields = [
            'DocenteID',
            'DocenteCodigo',
            'DocenteNombre',
            'DocenteApellido',
            'DocenteSexo',
            'DocenteEstadoCivil',
            'DocenteFechaNacimiento',
            'DocenteLugarNacimiento',
            'DocenteFechaIngreso',
            'DocenteNacionalidad',
            'DocenteTipoIdentificacion',
            'DocenteNumeroIdentificacion',
            'DocenteTelefono',
            'DocenteCorreoElectronico',
            'DocenteDireccion',
            'DocenteEstado',
            'DocenteObservaciones',
            'DocenteFechaRegistro',
            'UsuarioRegistro',
            'Docente_UniversidadFK',
            'Docente_TipoDocenteFK',
            'Docente_CategoriaDocenteFK',
            'universidadNombre',
            'tipoDocenteNombre',
            'categoriaDocenteNombre',
        ]


# PeriodoAcademico Serializer
class PeriodoAcademicoSerializer(serializers.ModelSerializer):
    Periodo_UniversidadFK = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())


    universidadNombre = serializers.CharField(source='Periodo_UniversidadFK.UniversidadNombre', read_only=True)

    class Meta:
        model = PeriodoAcademico
        fields = [
            'PeriodoID',
            'PeriodoCodigo',
            'PeriodoNombre',
            'PeriodoTipo',
            'PeriodoAnio',
            'PeriodoFechaInicio',
            'PeriodoFechaFin',
            'PeriodoFechaRegistro',
            'UsuarioRegistro',
            'PeriodoEstado',
            'Periodo_UniversidadFK',
            'universidadNombre'
        ]

class AsignacionDocenteSerializer(serializers.ModelSerializer):
    docenteFk = serializers.PrimaryKeyRelatedField(queryset=Docente.objects.all())
    campusFk = serializers.PrimaryKeyRelatedField(queryset=Campus.objects.all())
    universidadFk = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    facultadFk = serializers.PrimaryKeyRelatedField(queryset=Facultad.objects.all())
    escuelaFk = serializers.PrimaryKeyRelatedField(queryset=Escuela.objects.all())
    periodoFk = serializers.PrimaryKeyRelatedField(queryset=PeriodoAcademico.objects.all())

    docenteNombre = serializers.SerializerMethodField()
    campusNombre = serializers.CharField(source="campusFk.CampusNombre", read_only=True)
    universidadNombre = serializers.CharField(source="universidadFk.UniversidadNombre", read_only=True)
    facultadNombre = serializers.CharField(source="facultadFk.FacultadNombre", read_only=True)
    escuelaNombre = serializers.CharField(source="escuelaFk.EscuelaNombre", read_only=True)
    periodoNombre = serializers.CharField(source="periodoFk.PeriodoNombre", read_only=True)

    def get_docenteNombre(self, obj):
        return f"{obj.docenteFk.nombre} {obj.docenteFk.apellidos}"

    class Meta:
        model = AsignacionDocente
        fields = [
            'AsignacionID', 'nrc', 'clave', 'nombre', 'codigo', 'seccion',
            'modalidad', 'cupo', 'inscripto', 'horario', 'dias', 'aula',
            'creditos', 'tipo', 'accion', 'fecha_registro', 'usuario_registro',

            'docenteFk', 'campusFk', 'universidadFk', 'facultadFk', 'escuelaFk', 'periodoFk',

            'docenteNombre', 'campusNombre', 'universidadNombre',
            'facultadNombre', 'escuelaNombre', 'periodoNombre'
        ]

class AsignacionDocenteSerializer_frontend(serializers.ModelSerializer):
    facultadCodigo = serializers.CharField(source='facultadCodigo.nombre')
    escuelaCodigo = serializers.CharField(source='escuelaCodigo.nombre')
    docente_nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = AsignacionDocente
        fields = ['ADIDcodigo', 'nrc', 'clave', 'asignatura', 'codigo', 'seccion', 'modalidad', 
                  'campus', 'tipo', 'cupo', 'inscripto', 'horario', 'dias', 'Aula', 'creditos', 
                  'facultadCodigo', 'escuelaCodigo', 'docente_nombre_completo', 'period']

    def get_docente_nombre_completo(self, obj):
        # Assuming 'DocenteCodigo' is a ForeignKey to Docente model
        docente = obj.DocenteCodigo  # Get the related Docente instance
        if docente:
            return f"{docente.nombre} {docente.apellidos}"  # Combine nombre and apellidos
        return None  