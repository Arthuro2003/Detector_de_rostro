from django.urls import path
from . import views

urlpatterns = [
    # Ruta para la página principal
    path('', views.index, name='index'),

    # Ruta para el feed de video
    path('video_feed/', views.video_feed, name='video_feed'),
    path('capture_snapshot/', views.capture_snapshot, name='capture_snapshot'),
    path('clear_captures/', views.clear_captures, name='clear_captures'),
]