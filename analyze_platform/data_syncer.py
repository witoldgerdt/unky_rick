# unky_rick/data_syncer.py
import time
from datetime import datetime, timedelta
from django.utils.deprecation import MiddlewareMixin
from django.db import connection
from django.shortcuts import render

class DataSyncerMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Ensure data_status table exists
        self.ensure_table_exists()

        # Check the time_update value
        if self.is_data_update_needed():
            # Render splash page
            response = render(request, 'splash.html')
            # Perform data fetch in background
            self.fetch_new_data()
            return response

        # Continue processing the view
        return None

    def ensure_table_exists(self):
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time_update DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def is_data_update_needed(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT time_update FROM data_status ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()
            if row:
                last_update = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                if datetime.now() - last_update > timedelta(hours=12):
                    return True
            else:
                return True  # No data, so update is needed
        return False

    def fetch_new_data(self):
        # Simulate data fetch process
        time.sleep(2)  # Simulating data fetch time, replace with actual data fetch logic

        # Update the time_update value
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO data_status (time_update) VALUES (CURRENT_TIMESTAMP)')
