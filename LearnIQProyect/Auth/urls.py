from django.urls import path

from . import views

app_name = "Auth"

urlpatterns = [
    path('signin/', views.LogIn.as_view(), name='signIn'),
    path('signup/', views.Signup.as_view(), name='signUp'),
    path('resetpassword/', views.ResetPassword.as_view(), name='resetPassword'),
    path('signOut/', views.logout_view, name='signOut'),
]