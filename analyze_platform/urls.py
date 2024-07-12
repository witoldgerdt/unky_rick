from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'), 
    path('money/', views.money, name='money'),
    path('about/', views.about, name='health_check'),
    path('splash/', views.splash, name='splash'),
]