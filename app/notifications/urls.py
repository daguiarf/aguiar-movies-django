from django.urls import path

from .views import NotificationViewSet

notification_list = NotificationViewSet.as_view({"get": "list"})
notification_detail = NotificationViewSet.as_view({"get": "retrieve"})
notification_count = NotificationViewSet.as_view({"get": "count"})
notification_read = NotificationViewSet.as_view({"patch": "mark_as_read"})
notification_read_all = NotificationViewSet.as_view({"patch": "mark_all_as_read"})

urlpatterns = [
    path("notifications/", notification_list, name="notification-list"),
    path("notifications/count/", notification_count, name="notification-count"),
    path("notifications/read-all/", notification_read_all, name="notification-read-all"),
    path("notifications/<int:pk>/", notification_detail, name="notification-detail"),
    path("notifications/<int:pk>/read/", notification_read, name="notification-read"),
]
