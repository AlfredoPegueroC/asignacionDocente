# Generated by Django 5.0.7 on 2024-12-01 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_asignaciondocente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universidad',
            name='UniversidadCodigo',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]
