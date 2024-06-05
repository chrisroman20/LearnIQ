from django.urls import path

from . import views

app_name = "App"

urlpatterns = [
    path('App/', views.Home.as_view(), name='AppHome'),

]