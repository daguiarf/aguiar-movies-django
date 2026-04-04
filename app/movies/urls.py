from django.urls import path
from .views import (
    PopularMoviesView,
    PopularTVView,
    SearchView,
    MovieDetailsView,
    TVDetailsView,
    PersonDetailsView,
    GenresView
)

urlpatterns = [
    path("movies/popular/", PopularMoviesView.as_view(), name="movies-popular"),
    path("tv/popular/", PopularTVView.as_view(), name="tv-popular"),
    path("movies/search/", SearchView.as_view(), name="movies-search"),
    path("movies/<int:tmdb_id>/", MovieDetailsView.as_view(), name="movie-detail"),
    path("tv/<int:tmdb_id>/", TVDetailsView.as_view(), name="tv-detail"),
    path("person/<int:tmdb_id>/", PersonDetailsView.as_view(), name="person-detail"),
    path("genres/", GenresView.as_view(), name="genres"),
]
