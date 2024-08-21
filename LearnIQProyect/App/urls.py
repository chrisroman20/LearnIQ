from django.urls import path
from .views import graficar_radar_estilos_aprendizaje
from . import views

app_name = "App"

urlpatterns = [
    path('', views.Home.as_view(), name='AppHome'),
    path('Test/', views.AppTest.as_view(), name='AppTest'),
    path('learning_styles/', views.Informacion.as_view(), name='Informacion'),
    path('score/', graficar_radar_estilos_aprendizaje, name='GraficarRadar'),
]