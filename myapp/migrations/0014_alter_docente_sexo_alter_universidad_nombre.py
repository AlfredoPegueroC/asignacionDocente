# Generated by Django 4.2.19 on 2025-02-17 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_alter_docente_apellidos_alter_docente_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docente',
            name='sexo',
            field=models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=15),
        ),
        migrations.AlterField(
            model_name='universidad',
            name='nombre',
            field=models.CharField(max_length=110),
        ),
    ]
