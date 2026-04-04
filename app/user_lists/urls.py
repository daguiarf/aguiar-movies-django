from rest_framework.routers import DefaultRouter
from .views import FavoriteViewSet, WatchlistViewSet

router = DefaultRouter()
router.register('favorites', FavoriteViewSet, basename='favorites')
router.register('watchlist', WatchlistViewSet, basename='watchlist')

urlpatterns = router.urls