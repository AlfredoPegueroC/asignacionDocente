# Generated by Django 5.0.7 on 2024-12-01 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universidad',
            name='UniversidadCodigo',
            field=models.CharField(editable=False, max_length=10, primary_key=True, serialize=False),
        ),
    ]
