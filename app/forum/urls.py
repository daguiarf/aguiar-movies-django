from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="forum-posts")
router.register("comments", CommentViewSet, basename="forum-comments")

urlpatterns = router.urls
