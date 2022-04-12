from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('blog/<int:index>/', views.view_post, name='blog-view-post'),
    path('about/', views.about, name='blog-about'),
]
