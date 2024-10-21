from django.db import models

# Create your models here.
class Universidad(models.Model):
  UniversidadCodigo = models.IntegerField(primary_key=True)
  nombre = models.CharField(max_length=100, null=False)
  estado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])

  def __str__(self):
      return self.nombre
  

class Facultad(models.Model):
  facultadCodigo = models.IntegerField(primary_key=True)
  nombre = models.CharField(max_length=100, null=False)
  estado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])
  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre

class Escuela(models.Model):
  escuelaCodigo = models.IntegerField(primary_key=True)
  nombre = models.CharField(max_length=100, null=False)
  estado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])

  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)
  facultadCodigo = models.ForeignKey(Facultad, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre
  

class TipoDocente(models.Model):
  #CAMPOS
  tipoDocenteCodigo = models.IntegerField(primary_key=True)
  nombre = models.CharField(max_length=100, null=False)
  estado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])


  #FORIGNKEY
  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre

class CategoriaDocente(models.Model):
  #CAMPOS
  categoriaCodigo = models.IntegerField(primary_key=True)
  nombre = models.CharField(max_length=100, null=False)
  estado = models.CharField(max_length=15, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])


  #FORIGNKEY
  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre
  
class Docente(models.Model):
    #CAMPOS
    Docentecodigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    sexo = models.CharField(max_length=1, choices=[('F', 'Femenino'), ('M', 'Masculino')])
    estado_civil = models.CharField(max_length=1, choices=[('S', 'Soltero'), ('C', 'Casado'), ('U', 'Unión Libre'), ('V', 'Viudo')])
    fecha_nacimiento = models.DateField()
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
  periodoAcademicoCodigo = models.IntegerField(primary_key=True)
  nombre = models.CharField(max_length=50, null=True)
  anio = models.SmallIntegerField()
  fechaIni = models.DateField(auto_now=False,auto_now_add=False)
  fechaFinal = models.DateField(auto_now=False, auto_now_add=False)
  estado = models.CharField(max_length=15, choices=[('A', 'Abierto'), ('C', 'Cerrado')])

  UniversidadCodigo = models.ForeignKey(Universidad, on_delete=models.CASCADE)

  def __str__(self):
      return f"{self.nombre} {self.anio} {self.fechaIni} {self.fechaFinal}"
  