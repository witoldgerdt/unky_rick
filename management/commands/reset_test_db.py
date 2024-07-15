from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Drop and recreate the test database'

    def handle(self, *args, **options):
        db_name = 'test_analyze_db'
        db_user = settings.DATABASES['default']['USER']

        with connection.cursor() as cursor:
            # Drop the database if it exists
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
            self.stdout.write(self.style.SUCCESS(f'Dropped database {db_name}'))

            # Create a new database
            cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user};")
            self.stdout.write(self.style.SUCCESS(f'Created database {db_name}'))

        # Apply migrations
        self.call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Applied all migrations'))

        # Collect static files
        self.call_command('collectstatic', '--noinput')
        self.stdout.write(self.style.SUCCESS('Collected static files'))
