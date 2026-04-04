from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.responses import success_response, error_response
from .models import Favorite, Watchlist
from .serializers import FavoriteSerializer, WatchlistSerializer


@extend_schema_view(
    list=extend_schema(summary="Listar favoritos", tags=["Favoritos"]),
    create=extend_schema(summary="Adicionar favorito", tags=["Favoritos"]),
    retrieve=extend_schema(summary="Detalhe do favorito", tags=["Favoritos"]),
    destroy=extend_schema(summary="Remover favorito", tags=["Favoritos"]),
)
class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("content")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(error="Dados inválidos.", details=serializer.errors)
        try:
            self.perform_create(serializer)
        except Exception:
            return error_response(error="Este item já está nos seus favoritos.", status=409)
        return success_response(
            data=self.get_serializer(serializer.instance).data,
            message="Adicionado aos favoritos.",
            status=201,
        )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(data={"results": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return success_response(data=self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return success_response(message="Removido dos favoritos.", status=200)


@extend_schema_view(
    list=extend_schema(summary="Listar watchlist", tags=["Watchlist"]),
    create=extend_schema(summary="Adicionar à watchlist", tags=["Watchlist"]),
    retrieve=extend_schema(summary="Detalhe do item da watchlist", tags=["Watchlist"]),
    partial_update=extend_schema(summary="Atualizar item da watchlist", tags=["Watchlist"]),
    destroy=extend_schema(summary="Remover da watchlist", tags=["Watchlist"]),
)
class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user).select_related("content")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(error="Dados inválidos.", details=serializer.errors)
        try:
            self.perform_create(serializer)
        except Exception:
            return error_response(error="Este item já está na sua watchlist.", status=409)
        return success_response(
            data=self.get_serializer(serializer.instance).data,
            message="Adicionado à watchlist.",
            status=201,
        )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(data={"results": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return success_response(data=self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(error="Dados inválidos.", details=serializer.errors)
        serializer.save()
        return success_response(data=serializer.data, message="Watchlist atualizada.")

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return success_response(message="Removido da watchlist.", status=200)
