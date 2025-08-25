# myapp/management/commands/truncate_all.py
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Truncar todas las tablas (vaciar datos) en la base de datos"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Desactivar triggers (como claves foráneas)
            cursor.execute("ALTER TABLE ALL IN SCHEMA public DISABLE TRIGGER ALL;")

            # Obtener todas las tablas (excepto django_migrations)
            cursor.execute("""
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'
                AND tablename != 'django_migrations';
            """)
            tables = cursor.fetchall()

            for table in tables:
                cursor.execute(f'TRUNCATE TABLE public."{table[0]}" CASCADE;')
                self.stdout.write(f'Truncada tabla: {table[0]}')

            # Reactivar triggers
            cursor.execute("ALTER TABLE ALL IN SCHEMA public ENABLE TRIGGER ALL;")

        self.stdout.write(self.style.SUCCESS('¡Todas las tablas truncadas!'))
