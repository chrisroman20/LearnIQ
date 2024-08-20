from django.urls import path

from . import views

app_name = "Users"

urlpatterns = [
    path('', views.Home.as_view(), name="UsersHome"),
    path('edit/<int:id>', views.EditUser.as_view(), name="EditUser"),

]