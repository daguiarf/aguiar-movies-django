from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.responses import success_response, error_response
from .models import Review
from .serializers import ReviewSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


@extend_schema_view(
    list=extend_schema(
        summary="Listar reviews",
        description="Lista reviews. Filtre por tmdb_id + media_type ou por usuário autenticado.",
        parameters=[
            OpenApiParameter("tmdb_id", OpenApiTypes.INT, description="ID do conteúdo no TMDB"),
            OpenApiParameter("media_type", OpenApiTypes.STR, description="Tipo: movie | tv | person"),
            OpenApiParameter("mine", OpenApiTypes.BOOL, description="Se true, retorna apenas suas reviews"),
        ],
        tags=["Reviews"],
    ),
    create=extend_schema(summary="Criar review", tags=["Reviews"]),
    retrieve=extend_schema(summary="Detalhe da review", tags=["Reviews"]),
    partial_update=extend_schema(summary="Editar review (somente dono)", tags=["Reviews"]),
    destroy=extend_schema(summary="Deletar review (somente dono)", tags=["Reviews"]),
)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        qs = Review.objects.select_related("user", "content")

        if self.request.query_params.get("mine") == "true":
            qs = qs.filter(user=self.request.user)

        tmdb_id = self.request.query_params.get("tmdb_id")
        media_type = self.request.query_params.get("media_type")
        if tmdb_id and media_type:
            qs = qs.filter(content__tmdb_id=tmdb_id, content__media_type=media_type)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(error="Dados inválidos.", details=serializer.errors)
        try:
            self.perform_create(serializer)
        except Exception:
            return error_response(error="Você já possui uma review para este conteúdo.", status=409)
        return success_response(
            data=self.get_serializer(serializer.instance).data,
            message="Review criada com sucesso.",
            status=201,
        )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(data={"results": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        return success_response(data=self.get_serializer(self.get_object()).data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(error="Dados inválidos.", details=serializer.errors)
        serializer.save()
        return success_response(data=serializer.data, message="Review atualizada.")

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return success_response(message="Review deletada.")
