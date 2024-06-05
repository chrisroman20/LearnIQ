from django.contrib import admin
from django.urls import path,include

from Auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='HomePage'),
    path('Auth/', include("Auth.urls")),
    path('Users/', include("Users.urls")),
    path('App/', include("App.urls")),
]
