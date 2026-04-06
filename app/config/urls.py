from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Documentação Swagger / ReDoc
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Autenticação JWT
    path("api/auth/", include("accounts.urls")),

    # Integração TMDB (movies, tv, person, search)
    path("api/", include("movies.urls")),

    # Favoritos e Watchlist  →  router gera /favorites/ e /watchlist/
    path("api/", include("user_lists.urls")),

    # Reviews
    path("api/reviews/", include("reviews.urls")),

    # Fórum
    path("api/forum/", include("forum.urls")),

    # Notificações
    path("api/", include("notifications.urls")),
]
