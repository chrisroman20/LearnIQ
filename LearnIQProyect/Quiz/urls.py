from django.urls import path
from . import views

urlpatterns = [
    path('take_quiz/', views.take_quiz, name='take_quiz'),
    path('results/', views.results, name='results'),
]
