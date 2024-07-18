from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import DataStatus

def about(request):
    current_year = datetime.now().year
    return render(request, 'analyze_platform/about.html', {'current_year': current_year})

def money(request):
    return render(request, 'analyze_platform/money.html')

def splash(request):
    return render(request, 'analyze_platform/splash.html')

def get_data():
    # Placeholder function to update data
    pass

def update_data(request):
    # Assume there's only one row in DataStatus
    data_status = get_data(DataStatus, pk=1)
    time_diff = timezone.now() - data_status.update_time

    if time_diff >= timedelta(hours=12):
        get_data()
        data_status.update_time = timezone.now()
        data_status.save()

    return JsonResponse({'status': 'success'}, status=200)
