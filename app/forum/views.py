from django.db.models import Count
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.pagination import CursorIdPagination
from core.responses import success_response, error_response
from .models import Post, PostLike, Comment
from .serializers import PostSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


@extend_schema_view(
    list=extend_schema(
        summary="Listar posts do fórum",
        description=(
            "Lista posts com paginação cursor-based (infinite scroll).\n\n"
            "Ordenação por relevância: likes (+1) + comentários (+2) + recência.\n\n"
            "Filtre por `tmdb_id` + `media_type` para posts de um conteúdo específico."
        ),
        parameters=[
            OpenApiParameter("tmdb_id", OpenApiTypes.INT, description="ID TMDB do conteúdo"),
            OpenApiParameter("media_type", OpenApiTypes.STR, description="movie | tv | person"),
            OpenApiParameter("limit", OpenApiTypes.INT, description="Itens por página (default 10)"),
            OpenApiParameter("last_id", OpenApiTypes.INT, description="Cursor: ID do último item recebido"),
        ],
        tags=["Fórum"],
    ),
    create=extend_schema(summary="Criar post no fórum", tags=["Fórum"]),
    retrieve=extend_schema(summary="Detalhe do post", tags=["Fórum"]),
    partial_update=extend_schema(summary="Editar post (somente dono)", tags=["Fórum"]),
    destroy=extend_schema(summary="Deletar post (somente dono)", tags=["Fórum"]),
)
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def _base_queryset(self):
        return Post.objects.annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
        ).select_related("user", "content_reference")

    def get_queryset(self):
        qs = self._base_queryset()

        tmdb_id = self.request.query_params.get("tmdb_id")
        media_type = self.request.query_params.get("media_type")
        if tmdb_id:
            qs = qs.filter(content_reference__tmdb_id=tmdb_id)
        if media_type:
            qs = qs.filter(content_reference__media_type=media_type)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Ordenação por relevância: likes + 2*comentários, desempate por recência
        qs = self.get_queryset().order_by(
            "-likes_count", "-comments_count", "-created_at"
        )
        paginator = CursorIdPagination()
        results = paginator.paginate_queryset(qs, request)
        data = self.get_serializer(results, many=True).data
        return success_response(data=paginator.get_paginated_data(data))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(error="Dados inválidos.", details=serializer.errors)
        self.perform_create(serializer)
        return success_response(
            data=self.get_serializer(serializer.instance).data,
            message="Post criado com sucesso.",
            status=201,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self._base_queryset().get(pk=kwargs["pk"])
        return success_response(data=self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(error="Dados inválidos.", details=serializer.errors)
        serializer.save()
        return success_response(data=serializer.data, message="Post atualizado.")

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return success_response(message="Post deletado.")

    @extend_schema(
        summary="Curtir / descurtir post",
        description="Toggle: cria o like se não existe, remove se já existe.",
        tags=["Fórum"],
    )
    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            msg = "Like removido."
        else:
            msg = "Post curtido."
        likes_count = PostLike.objects.filter(post=post).count()
        return success_response(data={"likes_count": likes_count}, message=msg)

    @extend_schema(
        summary="Listar comentários do post",
        description="Comentários com paginação cursor-based.",
        parameters=[
            OpenApiParameter("limit", OpenApiTypes.INT, description="Itens por página (default 10)"),
            OpenApiParameter("last_id", OpenApiTypes.INT, description="Cursor"),
        ],
        tags=["Fórum"],
    )
    @action(detail=True, methods=["get"], url_path="comments")
    def comments(self, request, pk=None):
        post = self.get_object()
        qs = Comment.objects.filter(post=post).select_related("user").order_by("id")
        paginator = CursorIdPagination()
        # Para comentários a ordem é cronológica (do mais antigo para o mais novo)
        # Invertemos a lógica do cursor: filtramos id > last_id
        last_id = request.query_params.get("last_id")
        if last_id:
            try:
                qs = qs.filter(id__gt=int(last_id))
            except (ValueError, TypeError):
                pass
        try:
            limit = min(int(request.query_params.get("limit", 10)), 100)
        except (ValueError, TypeError):
            limit = 10
        items = list(qs[:limit + 1])
        has_more = len(items) > limit
        results = items[:limit]
        next_cursor = results[-1].id if results and has_more else None
        data = CommentSerializer(results, many=True).data
        return success_response(data={"results": data, "next_cursor": next_cursor, "has_more": has_more})

    @extend_schema(
        summary="Criar comentário no post",
        tags=["Fórum"],
    )
    @action(detail=True, methods=["post"], url_path="comments/create")
    def create_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(error="Dados inválidos.", details=serializer.errors)
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            content=serializer.validated_data["content"],
        )
        return success_response(
            data=CommentSerializer(comment).data,
            message="Comentário adicionado.",
            status=201,
        )


@extend_schema_view(
    partial_update=extend_schema(summary="Editar comentário (somente dono)", tags=["Fórum"]),
    destroy=extend_schema(summary="Deletar comentário (somente dono)", tags=["Fórum"]),
)
class CommentViewSet(viewsets.ModelViewSet):
    """
    Permite apenas editar e deletar comentários próprios.
    Para listar/criar use os endpoints aninhados em /forum/posts/{id}/comments/.
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ["patch", "delete", "head", "options"]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(error="Dados inválidos.", details=serializer.errors)
        serializer.save()
        return success_response(data=serializer.data, message="Comentário atualizado.")

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return success_response(message="Comentário deletado.")
