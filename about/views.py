from django.shortcuts import render
from datetime import datetime

def home(request):
    current_year = datetime.now().year
    return render(request, 'about/home.html', {'current_year': current_year})
