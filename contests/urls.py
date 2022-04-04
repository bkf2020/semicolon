from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='contests-home'),
    path('<int:index>/confirm/', views.confirm, name='contests-confirm'),
    path('<int:index>/arena/', views.arena, name='contests-arena'),
    path('<int:index>/scoreboard/', views.scoreboard, name='contests-scoreboard'),
]
