from django.db import models


# Create your models here.
from django.db import models

class Universidad(models.Model):
    UniversidadCodigo = models.AutoField(primary_key=True,editable=False)
    nombre = models.CharField(max_length=100, null=False)
    estado = models.CharField(
        max_length=15,
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')]
    )

    # def save(self, *args, **kwargs):
    #   if not self.UniversidadCodigo:
    #       # Get the last Universidad object by UniversidadCodigo
    #       last_codigo = Universidad.objects.all().order_by('UniversidadCodigo').last()
    #       if last_codigo and isinstance(last_codigo.UniversidadCodigo, str) and last_codigo.UniversidadCodigo.startswith('U'):
    #           try:
    #               # Extract numeric part and increment
    #               last_id = int(last_codigo.UniversidadCodigo[1:])
    #               new_id = f"U{last_id + 1:03d}"
    #           except ValueError:
    #               # Handle cases where the numeric part is invalid
    #               new_id = "U001"
    #       else:
    #           # Default ID if no entries exist or invalid format
    #           new_id = "U001"
    #       self.UniversidadCodigo = new_id

    #   super().save(*args, **kwargs)
    # def __str__(self):
    #     return self.nombre

  

class Facultad(models.Model):
  facultadCodigo = models.AutoField(primary_key=True, editable=False)
  nombre = models.CharField(max_length=100, null=False)
  estado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])
  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre

class Escuela(models.Model):
  escuelaCodigo = models.AutoField(primary_key=True, editable=False)
  nombre = models.CharField(max_length=100, null=False)
  estado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])

  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)
  facultadCodigo = models.ForeignKey(Facultad, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre
  

class TipoDocente(models.Model):
  #CAMPOS
  tipoDocenteCodigo = models.AutoField(primary_key=True, editable=False)
  nombre = models.CharField(max_length=100, null=False)
  estado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])


  #FORIGNKEY
  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre

class CategoriaDocente(models.Model):
  #CAMPOS
  categoriaCodigo = models.AutoField(primary_key=True, editable=False)
  nombre = models.CharField(max_length=100, null=False)
  estado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])


  #FORIGNKEY
  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre
  
class Docente(models.Model):
    #CAMPOS
    Docentecodigo = models.AutoField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    sexo = models.CharField(max_length=1, choices=[('F', 'Femenino'), ('M', 'Masculino')])
    estado_civil = models.CharField(max_length=1, choices=[('S', 'Soltero'), ('C', 'Casado'), ('U', 'Unión Libre'), ('V', 'Viudo')])
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=250)
    estado = models.CharField(max_length=10, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo'), ('Jubilado', 'Jubilado'), ('Sabático', 'Sabático'), ('Licencia', 'Licencia')])


    # FORIGNKEY
    UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    facultadCodigo = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    escuelaCodigo = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    tipoDocenteCodigo = models.ForeignKey(TipoDocente, on_delete=models.SET_NULL, null=True)
    categoriaCodigo = models.ForeignKey(CategoriaDocente, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class PeriodoAcademico(models.Model):
  periodoAcademicoCodigo = models.AutoField(primary_key=True, editable=False)
  nombre = models.CharField(max_length=50, null=True)
  estado = models.CharField(max_length=15, choices=[('A', 'Abierto'), ('C', 'Cerrado')])

  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)

  def __str__(self):
      return f"{self.nombre} {self.estado}"
  

class asignacionDocente(models.Model):
    nrc = models.CharField(max_length=40)
    clave = models.CharField(max_length=40)
    asignatura = models.CharField(max_length=40)
    codigo = models.CharField(max_length=40)
    seccion = models.CharField(max_length=40)
    modalidad = models.CharField(max_length=40)
    campus = models.CharField(max_length=40)
    tipo = models.CharField(max_length=40)
    cupo = models.CharField(max_length=40)
    inscripto = models.CharField(max_length=40)
    horario = models.CharField(max_length=40)
    dias = models.CharField(max_length=40)
    Aula = models.CharField(max_length=40)
    creditos = models.CharField(max_length=40)
    period = models.CharField(max_length=7, default='2025-20')  # Add the period field (e.g., '2025-20')

    facultadCodigo = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    escuelaCodigo = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    DocenteCodigo = models.ForeignKey(Docente, on_delete=models.CASCADE)
    
    #FOREIGHKEY 
    def __str__(self):
      return f"{self.nrc} {self.clave} {self.asignatura}"