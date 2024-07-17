from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from django.utils import timezone
import sqlite3
import os

class DataSyncerMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        self.ensure_table_exists()
        
        if self.is_data_outdated():
            self.update_data()
            return render(request, 'analyze_platform/splash.html')
        else:
            response = view_func(request, *view_args, **view_kwargs)
            return response

    def ensure_table_exists(self):
        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_status (
                    id INTEGER PRIMARY KEY,
                    time_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def is_data_outdated(self):
        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT time_update FROM data_status ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()
            if row:
                last_update = timezone.make_aware(datetime.fromisoformat(row[0]))
                return (timezone.now() - last_update).total_seconds() > 12 * 3600
            return True

    def update_data(self):
        # Implement the data update logic
        pass
