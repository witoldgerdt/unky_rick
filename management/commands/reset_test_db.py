from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Drops and recreates the test database.'

    def handle(self, *args, **options):
        test_db_name = settings.DATABASES['default']['TEST']['NAME']
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name};")
            cursor.execute(f"CREATE DATABASE {test_db_name};")
        self.stdout.write(self.style.SUCCESS(f'Successfully reset the test database: {test_db_name}'))
