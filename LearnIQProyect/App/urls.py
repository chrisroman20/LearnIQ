from django.urls import path

from . import views

app_name = "App"

urlpatterns = [
    path('', views.Home.as_view(), name='AppHome'),
    path('Test/', views.AppTest.as_view(), name='AppTest'),
]