from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='contests-home'),
    path('<int:index>/confirm/', views.confirm, name='contests-confirm'),
    path('<int:index>/submit/', views.submit, name='contests-submit'),
    path('<int:index>/semiarena/', views.semiarena, name='contests-semiarena'),
    path('<int:index>/arena/', views.arena, name='contests-arena'),
    path('<int:index>/scoreboard/', views.scoreboard, name='contests-scoreboard'),
    path('<int:index>/preview/', views.preview, name='contests-preview'),
]
