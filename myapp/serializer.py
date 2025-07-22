from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Universidad,Campus, Facultad, Escuela, TipoDocente, CategoriaDocente, Docente, PeriodoAcademico, AsignacionDocente, APILog
from django.contrib.auth.models import Group 

from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_active', 'groups', 'password'
        ]

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password(User.objects.make_random_password())
        user.save()

        groups = Group.objects.filter(name__in=groups_data)
        user.groups.set(groups)
        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if groups_data is not None:
            groups = Group.objects.filter(name__in=groups_data)
            instance.groups.set(groups)

        return instance

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_staff']

    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff', False)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        if is_staff:
            user.is_staff = True
            user.is_superuser = True
            grupo_admin, _ = Group.objects.get_or_create(name="admin")
            user.groups.add(grupo_admin)
        else:
            grupo_usuario, _ = Group.objects.get_or_create(name="usuario")
            user.groups.add(grupo_usuario)

        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))

        is_staff = validated_data.pop('is_staff', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Cambiar grupo si se modifica is_staff
        if is_staff is not None:
            instance.is_staff = is_staff
            instance.is_superuser = is_staff
            instance.groups.clear()
            group_name = "admin" if is_staff else "usuario"
            group, _ = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)

        instance.save()
        return instance

class APILogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = APILog
        fields = ['id', 'method', 'path', 'status_code', 'timestamp', 'message', 'user']

    def get_user(self, obj):
        return obj.user.username if obj.user else "Anónimo"
# Universidad Serializer
class CampusSerializer(serializers.ModelSerializer):
    Campus_UniversidadFK = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    universidadNombre = serializers.CharField(source='Campus_UniversidadFK.UniversidadNombre', read_only=True)

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
            'universidadNombre',
            'Campus_UniversidadFK',
        ]

class UniversidadSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(many=True, source='campus_list', read_only=True)

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
            'campus',
        ]

class FacultadSerializer(serializers.ModelSerializer):
    Facultad_UniversidadFK = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    Facultad_CampusFK = serializers.PrimaryKeyRelatedField(queryset=Campus.objects.all())
    universidadNombre = serializers.CharField(source='Facultad_UniversidadFK.UniversidadNombre', read_only=True)
    campusNombre = serializers.CharField(source='Facultad_CampusFK.CampusNombre', read_only=True)

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
            'universidadNombre',  
            'campusNombre',
        ]

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
            'universidadNombre',
        ]

class AsignacionDocenteSerializer(serializers.ModelSerializer):
    docenteFk = serializers.PrimaryKeyRelatedField(queryset=Docente.objects.all())
    campusFk = serializers.PrimaryKeyRelatedField(queryset=Campus.objects.all())
    universidadFk = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    facultadFk = serializers.PrimaryKeyRelatedField(queryset=Facultad.objects.all())
    escuelaFk = serializers.PrimaryKeyRelatedField(queryset=Escuela.objects.all())
    periodoFk = serializers.PrimaryKeyRelatedField(queryset=PeriodoAcademico.objects.all())

    docenteNombre = serializers.CharField(source="docenteFk.get_nombre_completo", read_only=True)
    campusNombre = serializers.CharField(source="campusFk.CampusNombre", read_only=True)
    universidadNombre = serializers.CharField(source="universidadFk.UniversidadNombre", read_only=True)
    facultadNombre = serializers.CharField(source="facultadFk.FacultadNombre", read_only=True)
    escuelaNombre = serializers.CharField(source="escuelaFk.EscuelaNombre", read_only=True)
    periodoNombre = serializers.CharField(source="periodoFk.PeriodoNombre", read_only=True)

    class Meta:
        model = AsignacionDocente
        fields = [
            'AsignacionID', 'nrc', 'clave', 'nombre', 'codigo', 'seccion',
            'modalidad', 'cupo', 'inscripto', 'horario', 'dias', 'aula',
            'creditos', 'tipo', 'accion', 'fecha_registro', 'usuario_registro',
            'docenteFk', 'campusFk', 'universidadFk', 'facultadFk', 'escuelaFk', 'periodoFk',
            'docenteNombre', 'campusNombre', 'universidadNombre',
            'facultadNombre', 'escuelaNombre', 'periodoNombre',
        ]

class AsignacionDocenteSerializer_frontend(serializers.ModelSerializer):
    facultadCodigo = serializers.CharField(source='facultadFk.FacultadNombre', read_only=True)
    escuelaCodigo = serializers.CharField(source='escuelaFk.EscuelaNombre', read_only=True)
    docente_nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = AsignacionDocente
        fields = [
            'AsignacionID', 'nrc', 'clave', 'nombre', 'codigo', 'seccion', 'modalidad', 
            'campusFk', 'tipo', 'cupo', 'inscripto', 'horario', 'dias', 'aula', 'creditos', 
            'facultadCodigo', 'escuelaCodigo', 'docente_nombre_completo', 'periodoFk'
        ]

    def get_docente_nombre_completo(self, obj):
        docente = obj.docenteFk
        if docente:
            return f"{docente.DocenteNombre} {docente.DocenteApellido}"
        return None
    
    
    