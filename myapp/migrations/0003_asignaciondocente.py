# Generated by Django 5.0.7 on 2024-12-01 22:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_universidad_universidadcodigo'),
    ]

    operations = [
        migrations.CreateModel(
            name='asignacionDocente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nrc', models.CharField(max_length=10)),
                ('clave', models.CharField(max_length=15)),
                ('asignatura', models.CharField(max_length=25)),
                ('codigo', models.CharField(max_length=15)),
                ('seccion', models.CharField(max_length=10)),
                ('modalidad', models.CharField(max_length=15)),
                ('campus', models.CharField(max_length=20)),
                ('tipo', models.CharField(max_length=20)),
                ('cupo', models.CharField(max_length=20)),
                ('inscripto', models.CharField(max_length=20)),
                ('horario', models.CharField(max_length=20)),
                ('dias', models.CharField(max_length=20)),
                ('Aula', models.CharField(max_length=20)),
                ('creditos', models.CharField(max_length=20)),
                ('DocenteCodigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.docente')),
                ('escuelaCodigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.escuela')),
                ('facultadCodigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.facultad')),
            ],
        ),
    ]
