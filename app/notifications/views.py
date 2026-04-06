from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.pagination import CursorIdPagination
from core.responses import success_response, error_response
from .models import Notification
from .serializers import NotificationSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Listar notificações do usuário",
        description=(
            "Lista todas as notificações do usuário autenticado com paginação cursor-based.\n\n"
            "Ordenadas da mais recente para a mais antiga."
        ),
        parameters=[
            OpenApiParameter("limit", OpenApiTypes.INT, description="Itens por página (default 10)"),
            OpenApiParameter("last_id", OpenApiTypes.INT, description="Cursor: ID da última notificação recebida"),
        ],
        tags=["Notificações"],
    ),
)
class NotificationViewSet(GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related("sender", "post")

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset().order_by("-created_at")
        paginator = CursorIdPagination()
        results = paginator.paginate_queryset(qs, request)
        data = self.get_serializer(results, many=True).data
        return success_response(data=paginator.get_paginated_data(data))

    def retrieve(self, request, *args, **kwargs):
        try:
            notification = self.get_queryset().get(pk=kwargs["pk"])
        except Notification.DoesNotExist:
            return error_response(error="Notificação não encontrada.", status=404)

        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])

        return success_response(data=self.get_serializer(notification).data)

    @extend_schema(
        summary="Total de notificações do usuário",
        description="Retorna o total geral e o total de notificações não lidas do usuário autenticado.",
        tags=["Notificações"],
    )
    @action(detail=False, methods=["get"], url_path="count")
    def count(self, request):
        qs = self.get_queryset()
        total = qs.count()
        unread = qs.filter(is_read=False).count()
        return success_response(data={"total": total, "unread": unread})

    @extend_schema(
        summary="Marcar notificação como lida",
        description="Marca uma notificação específica como lida.",
        tags=["Notificações"],
    )
    @action(detail=True, methods=["patch"], url_path="read")
    def mark_as_read(self, request, pk=None):
        try:
            notification = self.get_queryset().get(pk=pk)
        except Notification.DoesNotExist:
            return error_response(error="Notificação não encontrada.", status=404)

        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])

        return success_response(
            data=self.get_serializer(notification).data,
            message="Notificação marcada como lida.",
        )

    @extend_schema(
        summary="Marcar todas as notificações como lidas",
        description="Marca todas as notificações não lidas do usuário autenticado como lidas.",
        tags=["Notificações"],
    )
    @action(detail=False, methods=["patch"], url_path="read-all")
    def mark_all_as_read(self, request):
        updated = self.get_queryset().filter(is_read=False).update(is_read=True)
        return success_response(
            data={"updated": updated},
            message="Todas as notificações foram marcadas como lidas.",
        )
