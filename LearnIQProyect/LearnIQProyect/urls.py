from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from Auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='HomePage'),
    path('Auth/', include("Auth.urls")),
    path('Users/', include("Users.urls")),
    path('App/', include("App.urls")),
    path('Quiz/', include("Quiz.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)