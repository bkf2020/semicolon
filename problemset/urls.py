from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='problemset-home'),
    path('<int:index>/', views.problem, name='problemset-view'),
]
