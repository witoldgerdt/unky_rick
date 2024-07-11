from django.urls import path
from .views import analyze_platform

urlpatterns = [
    path('', analyze_platform, name='about'),
]