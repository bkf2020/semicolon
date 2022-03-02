from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='contests-home'),
    path('<int:index>/register/', views.register, name='contests-register'),
    path('<int:index>/arena/', views.arena, name='contests-arena'),
]
