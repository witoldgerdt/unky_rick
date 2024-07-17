import time
from django.shortcuts import render
from django.urls import resolve

class DataSyncerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip splash screen for specific views
        if resolve(request.path_info).url_name in ['about', 'money']:
            return None
        
        try:
            # Simulate some processing logic
            time.sleep(2)  # Example delay, replace with actual logic
            return render(request, 'analyze_platform/splash.html')
        except Exception as e:
            print(f"Exception in process_view: {e}")
            raise
