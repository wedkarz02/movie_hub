from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="hub-home"),
    path("", views.MovieListView.as_view(), name="hub-home"),
    path("about", views.about, name="hub-about"),
    path("movies", views.MovieListView.as_view(), name="hub-movies"),
    path("movies/<int:pk>/", views.MovieDetailView.as_view(),
         name="hub-movie-details"),
    path("movies/new", views.MovieCreateView.as_view(), name="hub-movies-create"),
    path("movies/<int:pk>/update/", views.MovieUpdateView.as_view(),
         name="hub-movie-update"),
    path("movies/<int:pk>/delete/", views.MovieDeleteView.as_view(),
         name="hub-movie-delete"),
    path("movies/<int:pk>/delete-rating/", views.delete_rating,
         name="hub-movie-delete-rating"),
    path("movies/<int:pk>/summarize-movie-description/", views.summarize_movie_description,
         name="hub-summarize-description"),
]
