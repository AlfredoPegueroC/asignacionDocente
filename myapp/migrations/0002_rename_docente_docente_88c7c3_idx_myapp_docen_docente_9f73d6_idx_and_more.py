# Generated by Django 4.2.19 on 2025-05-04 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='docente',
            new_name='myapp_docen_Docente_9f73d6_idx',
            old_name='Docente_Docente_88c7c3_idx',
        ),
        migrations.RenameIndex(
            model_name='docente',
            new_name='myapp_docen_Docente_e8f339_idx',
            old_name='Docente_Docente_19fe7d_idx',
        ),
        migrations.AlterModelTable(
            name='docente',
            table=None,
        ),
    ]
