from django.urls import path
from django.http import JsonResponse
from . import views

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('', views.about, name='about'), 
    path('money/', views.money, name='money'),
    path('splash/', views.splash, name='splash'),
    path('health_check/', health_check, name='health_check'),
]