# Generated by Django 5.1.4 on 2025-01-31 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_remove_asignaciondocente_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodoacademico',
            name='estado',
            field=models.CharField(choices=[('Abierto', 'Abierto'), ('Cerrado', 'Cerrado')], max_length=15),
        ),
    ]
