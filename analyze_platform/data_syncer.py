import time
from django.shortcuts import render

class DataSyncerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Add any logic you need before the view is processed
        try:
            # Simulate some processing logic
            time.sleep(2)  # Example delay, replace with actual logic
            return render(request, 'analyze_platform/splash.html')
        except Exception as e:
            # Handle any exceptions and render the splash screen
            print(f"Exception in process_view: {e}")
            return render(request, 'analyze_platform/splash.html')
