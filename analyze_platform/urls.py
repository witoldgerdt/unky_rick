from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'), 
    path('money/', views.money, name='money'),
    path('health/', views.about, name='health_check'),
     path('splash/', views.splash, name='splash'),
]