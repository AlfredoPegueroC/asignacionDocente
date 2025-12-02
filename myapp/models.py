from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
User = get_user_model()

class Universidad(models.Model):
    UniversidadID = models.AutoField(primary_key=True)
    UniversidadCodigo = models.CharField(max_length=25, unique=True)
    UniversidadNombre = models.CharField(max_length=55, null=False, unique=True)
    UniversidadDireccion = models.CharField(max_length=200, null=False)
    UniversidadTelefono = models.CharField(max_length=20, null=False)
    UniversidadEmail = models.CharField(max_length=55, null=False)
    UniversidadSitioWeb = models.CharField(max_length=55, null=False)
    UniversidadRector = models.CharField(max_length=55, null=False)
    UniversidadFechaRegistro = models.DateField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=55, null=False, default='admin')
    UniversidadEstado = models.CharField(
        max_length=15,
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')],
        default='Activo'
    )

    class Meta:
        indexes = [
            models.Index(fields=['UniversidadCodigo'], name='idx_universidad_codigo'),
            models.Index(fields=['UniversidadNombre'], name='idx_universidad_nombre'),
        ]

    def __str__(self):
        return f"{self.UniversidadNombre} ({self.UniversidadCodigo})"


class Campus(models.Model):
    CampusID = models.AutoField(primary_key=True)
    CampusCodigo = models.CharField(max_length=25, unique=True)
    CampusNombre = models.CharField(max_length=100, unique=True)
    CampusDireccion = models.CharField(max_length=255, blank=True, null=True)
    CampusDirector = models.CharField(max_length=100, blank=True, null=True)
    CampusPais = models.CharField(max_length=100, blank=True, null=True)
    CampusProvincia = models.CharField(max_length=100, blank=True, null=True)
    CampusCiudad = models.CharField(max_length=100, blank=True, null=True)
    CampusTelefono = models.CharField(max_length=50, blank=True, null=True)
    CampusCorreoContacto = models.CharField(max_length=100, blank=True, null=True)
    CampusFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    CampusEstado = models.CharField(
        max_length=15,
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')],
        default='Activo'
    )
    
    Campus_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="campus_list" 
    )

    def __str__(self):
        return self.CampusNombre

    class Meta:
        indexes = [
            models.Index(fields=['CampusEstado'], name='idx_campus_estado'),
            models.Index(fields=['CampusNombre'], name='idx_campus_nombre'),
        ]


class Facultad(models.Model):
    FacultadID = models.AutoField(primary_key=True)
    FacultadCodigo = models.CharField(max_length=25, unique=True)
    FacultadNombre = models.CharField(max_length=100, null=False, unique=True)
    FacultadDecano = models.CharField(max_length=100, null=False)
    FacultadDireccion = models.CharField(max_length=100, null=False)
    FacultadTelefono = models.CharField(max_length=100, null=False)
    FacultadEmail = models.CharField(max_length=100, null=False)
    FacultadFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    FacultadEstado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo')
    
    Facultad_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="facultades" 
    )
    Facultad_CampusFK = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name="facultades"  
    )

    def __str__(self):
        return self.FacultadNombre

    class Meta:
        indexes = [
            models.Index(fields=['FacultadCodigo'], name='idx_facultad_codigo'),
            models.Index(fields=['FacultadNombre'], name='idx_facultad_nombre'),
            models.Index(fields=['FacultadEstado'], name='idx_facultad_estado'),
        ]


class Escuela(models.Model):
    EscuelaId = models.AutoField(primary_key=True) 
    EscuelaCodigo = models.CharField(max_length=25, unique=True)  
    EscuelaNombre = models.CharField(max_length=100, null=False, unique=True)
    EscuelaDirectora = models.CharField(max_length=100, null=False)
    EscuelaTelefono = models.CharField(max_length=100, null=False)
    EscuelaCorreo = models.CharField(max_length=100, null=False)
    EscuelaFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    EscuelaEstado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo')

    Escuela_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="escuelas" 
    )
    Escuela_facultadFK = models.ForeignKey(
        Facultad,
        on_delete=models.CASCADE,
        related_name="escuelas"  
    )

    def __str__(self):
        return self.EscuelaNombre 

    class Meta:
        indexes = [
            models.Index(fields=['EscuelaNombre'], name='idx_escuela_nombre'),
            models.Index(fields=['EscuelaEstado'], name='idx_escuela_estado'),
        ]


class TipoDocente(models.Model):
    TipoDocenteID = models.AutoField(primary_key=True)
    TipoDocenteCodigo = models.CharField(max_length=25, unique=True)
    TipoDocenteDescripcion = models.CharField(max_length=255, null=False, unique=True)
    TipoDocenteEstado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo')
    TipoFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')

    TipoDocente_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="tipos_docente"
    )

    def __str__(self):
        return self.TipoDocenteDescripcion

    class Meta:
        indexes = [
            models.Index(fields=['TipoDocenteDescripcion'], name='idx_tipo_descripcion'),
            models.Index(fields=['TipoDocenteEstado'], name='idx_tipo_estado'),
        ]  
        
class Status(models.Model):
    StatusID = models.AutoField(primary_key=True)
    StatusCodigo = models.CharField(max_length=25, unique=True)
    StatusNombre = models.CharField(max_length=50, unique=True)
    StatusFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    
    Status_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="status_lista"
    )
    def __str__(self):
        return self.StatusNombre

    class Meta:
        indexes = [
            models.Index(fields=['StatusNombre'], name='idx_status_nombre'),
        ]
class Accion(models.Model):
    AccionID = models.AutoField(primary_key=True)
    AccionCodigo = models.CharField(max_length=25, unique=True)
    AccionNombre = models.CharField(max_length=50, unique=True)
    AccionFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    
    Accion_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="acciones_lista"
    )
    def __str__(self):
        return self.AccionNombre

    class Meta:
        indexes = [
            models.Index(fields=['AccionNombre'], name='idx_accion_nombre'),
        ]

class CategoriaDocente(models.Model):
    CategoriaID = models.AutoField(primary_key=True)
    categoriaCodigo = models.CharField(max_length=25, unique=True)
    CategoriaNombre = models.CharField(max_length=100, null=False, unique=True)
    CategoriaEstado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo')
    CategoriaFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
 
    Categoria_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="categorias_docente"
    )

    def __str__(self):
        return self.CategoriaNombre  # Corregí de "return self.nombre"

    class Meta:
        indexes = [
            models.Index(fields=['CategoriaNombre'], name='idx_categoria_nombre'),
            models.Index(fields=['CategoriaEstado'], name='idx_categoria_estado'),
        ]

class Asignatura(models.Model):
    AsignaturaCodigo = models.CharField(max_length=25, primary_key=True)
    AsignaturaNombre = models.CharField(max_length=100)
    AsignaturaCreditos = models.IntegerField(default=0)
    AsignaturaHorasTeoricas = models.IntegerField(default=0)
    AsignaturaHorasPracticas = models.IntegerField(default=0)
    AsignaturaEstado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo')
    
    AsignaturaFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    
    Asignatura_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="asignaturas"
    )
    Asignatura_FacultadFK = models.ForeignKey(
        Facultad,
        on_delete=models.CASCADE,
        related_name="asignaturas"
    )
    Asignatura_EscuelaFK = models.ForeignKey(
        Escuela,
        on_delete=models.CASCADE,
        related_name="asignaturas"
    )

    def __str__(self):
        return self.AsignaturaNombre

    class Meta:
        indexes = [
            models.Index(fields=['AsignaturaNombre'], name='idx_asignatura_nombre'),
            models.Index(fields=['AsignaturaEstado'], name='idx_asignatura_estado'),
        ]


class Docente(models.Model):
    DocenteID = models.AutoField(primary_key=True)
    DocenteCodigo = models.CharField(max_length=10, unique=True)
    DocenteNombre = models.CharField(max_length=100)
    DocenteApellido = models.CharField(max_length=100)
    DocenteSexo = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Femenino')]
    )
    DocenteEstadoCivil = models.CharField(
        max_length=20,
        choices=[
            ('Soltero', 'Soltero'),
            ('Casado', 'Casado'),
            ('Union Libre', 'Unión Libre'),
            ('Viudo', 'Viudo')
        ]
    )
    DocenteFechaNacimiento = models.DateField(null=True, blank=True)
    DocenteLugarNacimiento = models.CharField(max_length=100)
    DocenteFechaIngreso = models.DateField(null=True, blank=True)
    DocenteNacionalidad = models.CharField(max_length=50)
    DocenteTipoIdentificacion = models.CharField(max_length=20)
    DocenteNumeroIdentificacion = models.CharField(max_length=20)
    DocenteTelefono = models.CharField(max_length=20)
    DocenteCelular = models.CharField(max_length=20, default='88888888')
    DocenteCorreoElectronico = models.EmailField(max_length=100)
    DocenteDireccion = models.CharField(max_length=200)
    DocenteEstado = models.CharField(
        max_length=50,
        default='Activo')
    DocenteObservaciones = models.TextField(blank=True, null=True)
    DocenteFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, default='admin')

    Docente_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="docentes"
    )
    Docente_TipoDocenteFK = models.ForeignKey(
        TipoDocente,
        on_delete=models.SET_NULL,
        null=True,
        related_name="docentes"
    )
    Docente_CategoriaDocenteFK = models.ForeignKey(
        CategoriaDocente,
        on_delete=models.SET_NULL,
        null=True,
        related_name="docentes"
    )

    def __str__(self):
        return f"{self.DocenteNombre} {self.DocenteApellido}"
    
    @property
    def get_nombre_completo(self):
        return f"{self.DocenteNombre} {self.DocenteApellido}"

    class Meta:
        # unique_together = ('DocenteNumeroIdentificacion', 'Docente_UniversidadFK')
        indexes = [
            models.Index(fields=['DocenteCodigo']),
            models.Index(fields=['Docente_UniversidadFK']),
        ]


class PeriodoAcademico(models.Model):
    PeriodoID = models.AutoField(primary_key=True)
    PeriodoCodigo = models.CharField(max_length=25, unique=True)
    PeriodoNombre = models.CharField(max_length=100, unique=True)
    PeriodoTipo = models.CharField(max_length=20)
    PeriodoAnio = models.IntegerField()
    PeriodoFechaInicio = models.DateField()
    PeriodoFechaFin = models.DateField()
    PeriodoFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    PeriodoEstado = models.CharField(
        max_length=15,
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')],
        default='Activo'
    )

    Periodo_UniversidadFK = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name="periodos"
    )

    def __str__(self):
        return self.PeriodoNombre

    class Meta:
        indexes = [
            models.Index(fields=['PeriodoEstado'], name='idx_periodo_estado'),
            models.Index(fields=['PeriodoAnio'], name='idx_periodo_anio'),
        ]
        
class AsignacionDocente(models.Model):
    AsignacionID = models.AutoField(primary_key=True)

    nrc = models.CharField(max_length=10, null=True, blank=True)  # sin default 'N/A'
    clave = models.CharField(max_length=10)
    nombre = models.CharField(max_length=150, blank=True, null=True) # asignatura nombre

    # Puede faltar el código → mejor null; “N/A” lo mostrarás en serializer/UI
    codigo = models.CharField(max_length=10, blank=True, null=True)

    seccion = models.CharField(max_length=10, blank=True, null=True)
    modalidad = models.CharField(max_length=30, blank=True, null=True)
    cupo = models.IntegerField(blank=True, null=True)
    inscripto = models.IntegerField(blank=True, null=True)
    horario = models.CharField(max_length=100, blank=True, null=True)
    dias = models.CharField(max_length=50, blank=True, null=True)
    aula = models.CharField(max_length=50, blank=True, null=True)
    creditos = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)

    comentario = models.CharField(max_length=255, blank=True, null=True, default='observaciones')
    accion = models.CharField(max_length=50, blank=True, null=True, default='Pendiente Asignar') # status
    modificacion = models.CharField(max_length=100, blank=True, null=True, default='--------') # acciones

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_registro = models.CharField(max_length=50, blank=True, null=True, default='admin')

    # Foreign keys (permitir que falte el docente)
    docenteFk = models.ForeignKey(
        Docente,
        on_delete=models.SET_NULL,      # antes: CASCADE
        null=True, blank=True,
        related_name='asignaciones'
    )
    campusFk = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    universidadFk = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    facultadFk = models.ForeignKey(
        Facultad,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    escuelaFk = models.ForeignKey(
        Escuela,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    periodoFk = models.ForeignKey(
        PeriodoAcademico,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )

    class Meta:
        constraints = [
            # Unicidad solo si NRC no es nulo
            # models.UniqueConstraint(
            #     fields=['nrc', 'periodoFk'],
            #     name='unique_nrc_periodo',
            #     condition=Q(nrc__isnull=False)
            # ),
            # Opcional: exigir que exista al menos docente o código
            # models.CheckConstraint(
            #     check=Q(docenteFk__isnull=False) | Q(codigo__isnull=False),
            #     name="asignacion_docente_o_codigo_presente"
            # )
        ]
        indexes = [
            models.Index(fields=['nrc'], name='idx_asignacion_nrc'),
            models.Index(fields=['periodoFk'], name='idx_asignacion_periodo'),
            models.Index(fields=['docenteFk'], name='idx_asignacion_docente'),
            models.Index(fields=['campusFk'], name='idx_asignacion_campus'),
            models.Index(fields=['facultadFk'], name='idx_asignacion_facultad'),
        ]

    def __str__(self):
        return f"{self.nrc or 'N/A'} - {self.nombre or 'N/A'}"


class APILog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    method = models.CharField(max_length=10)
    path = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField()
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} {self.method} {self.path} [{self.status_code}]"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    universidad = models.ForeignKey(
        Universidad, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='profiles_universidad'
    )
    
    facultad = models.ForeignKey(
        Facultad, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='profiles_facultad' 
    )
    
    escuela = models.ForeignKey(
        Escuela, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='profiles_escuela' 
    )

    def __str__(self):
        return self.user.username