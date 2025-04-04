from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="hub-home"),
    path("about", views.about, name="hub-about"),
    path("movies", views.movies, name="hub-movies"),
]
