from django.shortcuts import render
from datetime import datetime

def about(request):
    current_year = datetime.now().year
    return render(request, 'analyze_platform/about.html', {'current_year': current_year})

def money(request):
    return render(request, 'analyze_platform/money.html')

def splash(request):
    return render(request, 'analyze_platform/splash.html')
