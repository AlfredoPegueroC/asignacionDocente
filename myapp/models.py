from django.db import models


class Universidad(models.Model):
    UniversidadID = models.AutoField(primary_key=True)  # ID interno autoincremental
    UniversidadCodigo = models.CharField(max_length=25, unique=True)  # Ingresado por el usuario
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
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')]
    )

    class Meta:
        indexes = [
            models.Index(fields=['UniversidadCodigo'], name='idx_universidad_codigo'),
            models.Index(fields=['UniversidadNombre'], name='idx_universidad_nombre'),
        ]

    def __str__(self):
        return f"{self.UniversidadNombre} ({self.UniversidadCodigo})"
   
class Campus(models.Model):
    CampusID = models.AutoField(primary_key=True)  # ID interno autoincremental
    CampusCodigo = models.CharField(max_length=25, unique=True)
    CampusNombre = models.CharField(max_length=100, unique=True)
    CampusDireccion = models.CharField(max_length=255, blank=True, null=True)
    CampusPais = models.CharField(max_length=100, blank=True, null=True)
    CampusProvincia = models.CharField(max_length=100, blank=True, null=True)
    CampusCiudad = models.CharField(max_length=100, blank=True, null=True)
    CampusTelefono = models.CharField(max_length=50, blank=True, null=True)
    CampusCorreoContacto = models.CharField(max_length=100, blank=True, null=True)
    CampusFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    CampusEstado = models.CharField(
        max_length=15,
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')]
    )
    
    Campus_UniversidadFK = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.CampusNombre
    class Meta:
        indexes = [
            models.Index(fields=['CampusEstado'], name='idx_campus_estado'),
            models.Index(fields=['CampusNombre'], name='idx_campus_nombre'),
        ]

class Facultad(models.Model):
    FacultadID = models.AutoField(primary_key=True)  # ID interno autoincremental
    FacultadCodigo = models.CharField(max_length=25, unique=True)  # Ingresado por el usuario)
    FacultadNombre = models.CharField(max_length=100, null=False, unique=True) ## REVISAR MAS TARDE UNIQUE TRUE
    FacultadDecano = models.CharField(max_length=100, null=False)
    FacultadDireccion = models.CharField(max_length=100, null=False)
    FacultadTelefono = models.CharField(max_length=100, null=False)
    FacultadEmail = models.CharField(max_length=100, null=False)
    FacultadFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    FacultadEstado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])
    
    
    Facultad_UniversidadFK = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    Facultad_CampusFK = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        indexes = [
                models.Index(fields=['FacultadCodigo'], name='idx_facultad_codigo'),
                models.Index(fields=['FacultadNombre'], name='idx_facultad_nombre'),
                models.Index(fields=['FacultadEstado'], name='idx_facultad_estado'),
            ]

class Escuela(models.Model):
    EscuelaId = models.AutoField(primary_key=True) 
    EscuelaCodigo = models.CharField(max_length=25,unique=True)  
    EscuelaNombre = models.CharField(max_length=100, null=False, unique=True) ## REVISAR MAS TARDE UNIQUE TRUE
    EscuelaDirectora = models.CharField(max_length=100, null=False)
    EscuelaTelefono = models.CharField(max_length=100, null=False)
    EscuelaCorreo = models.CharField(max_length=100, null=False)
    EscuelaFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
    EscuelaEstado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])

    Escuela_UniversidadFK = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    Escuela_facultadFK = models.ForeignKey(Facultad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    class Meta:
        indexes = [
                models.Index(fields=['EscuelaNombre'], name='idx_escuela_nombre'),
                models.Index(fields=['EscuelaEstado'], name='idx_escuela_estado'),
            ]


class TipoDocente(models.Model):
    # CAMPOS
    TipoDocenteID = models.AutoField(primary_key=True)  # ID interno autoincremental
    TipoDocenteCodigo = models.CharField(max_length=25, unique=True)  # Ingresado por el usuario
    TipoDocenteDescripcion = models.CharField(max_length=255, null=False, unique=True)
    TipoDocenteEstado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])
    TipoFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')

    # FOREIGNKEY
    TipoDocente_UniversidadFK = models.ForeignKey('Universidad', on_delete=models.CASCADE, db_column='UniversidadCodigo')

    def __str__(self):
        return self.TipoDocenteDescripcion

    class Meta:
        indexes = [
            models.Index(fields=['TipoDocenteDescripcion'], name='idx_tipo_descripcion'),
            models.Index(fields=['TipoDocenteEstado'], name='idx_tipo_estado'),
        ]

class CategoriaDocente(models.Model):
  #CAMPOS
  CategoriaID = models.AutoField(primary_key=True)  # ID interno autoincremental
  categoriaCodigo = models.CharField(max_length=25,unique=True)  # Ingresado por el usuario
  CategoriaNombre = models.CharField(max_length=100, null=False, unique=True)
  CategoriaEstado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])
  CategoriaFechaRegistro = models.DateTimeField(auto_now_add=True)
  UsuarioRegistro = models.CharField(max_length=50, blank=True, null=True, default='admin')
 
  #FORIGNKEY
  Categoria_UniversidadFK = models.ForeignKey(Universidad, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre

  class Meta:
      indexes = [
            models.Index(fields=['CategoriaNombre'], name='idx_categiria_nombre'),
            models.Index(fields=['CategoriaEstado'], name='idx_categoria_estado'),
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
    DocenteCorreoElectronico = models.EmailField(max_length=100)
    DocenteDireccion = models.CharField(max_length=200)
    DocenteEstado = models.CharField(
    max_length=15,
    choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')],
    default='Activo')
    DocenteObservaciones = models.TextField(blank=True, null=True)
    DocenteFechaRegistro = models.DateTimeField(auto_now_add=True)
    UsuarioRegistro = models.CharField(max_length=50, default='admin')

    # Foreign Keys
    Docente_UniversidadFK = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    Docente_TipoDocenteFK = models.ForeignKey(TipoDocente, on_delete=models.SET_NULL, null=True)
    Docente_CategoriaDocenteFK = models.ForeignKey(CategoriaDocente, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.DocenteNombre} {self.DocenteApellido}"
    
    @property
    def get_nombre_completo(self):
        return f"{self.DocenteNombre} {self.DocenteApellido}"

    class Meta:
        unique_together = ('DocenteNumeroIdentificacion', 'Docente_UniversidadFK')
        indexes = [
            models.Index(fields=['DocenteCodigo']),
            models.Index(fields=['Docente_UniversidadFK']),
        ]


class PeriodoAcademico(models.Model):
    # CAMPOS
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
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')]
    )

    # FOREIGNKEY
    Periodo_UniversidadFK = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    def __str__(self):
        return self.PeriodoNombre

    class Meta:
        indexes = [
            models.Index(fields=['PeriodoEstado'], name='idx_periodo_estado'),
            models.Index(fields=['PeriodoAnio'], name='idx_periodo_anio'),
        ]
        
class AsignacionDocente(models.Model):
    AsignacionID = models.AutoField(primary_key=True)
    nrc = models.CharField(max_length=10, unique=True)
    clave = models.CharField(max_length=10)
    nombre = models.CharField(max_length=150, blank=True, null=True)
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
    accion = models.CharField(max_length=50, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_registro = models.CharField(max_length=50, blank=True, null=True, default='admin')

    # Foreign keys
    docenteFk = models.ForeignKey(Docente, on_delete=models.CASCADE)
    campusFk = models.ForeignKey(Campus, on_delete=models.CASCADE)
    universidadFk = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    facultadFk = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    escuelaFk = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    periodoFk = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nrc} - {self.nombre}"

