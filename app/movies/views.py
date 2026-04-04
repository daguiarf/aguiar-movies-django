from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .services.tmdb_service import TMDBService
from core.responses import success_response, error_response


class PopularMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Filmes populares / filtrados por gênero",
        description="Retorna filmes populares ou filtra por gênero usando discover.",
        parameters=[
            OpenApiParameter(
                "page",
                OpenApiTypes.INT,
                description="Número da página (default: 1)",
            ),
            OpenApiParameter(
                "genres",
                OpenApiTypes.STR,
                description="IDs de gêneros separados por vírgula (ex: 28,12)",
                required=False,
            ),
        ],
        tags=["TMDB"],
    )
    def get(self, request):
        page = request.query_params.get("page", 1)
        genres = request.query_params.get("genres")

        try:
            service = TMDBService()

            if genres:
                data = service.discover_movies(page=page, genres=genres)
            else:
                data = service.get_popular_movies(page)

            return success_response(data=data)

        except Exception as e:
            return error_response(error=str(e), status=502)


class PopularTVView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Séries populares / filtradas por gênero",
        description="Retorna séries populares ou filtra por gênero usando discover.",
        parameters=[
            OpenApiParameter(
                "page",
                OpenApiTypes.INT,
                description="Número da página (default: 1)",
            ),
            OpenApiParameter(
                "genres",
                OpenApiTypes.STR,
                description="IDs de gêneros separados por vírgula (ex: 18,10765)",
                required=False,
            ),
        ],
        tags=["TMDB"],
    )
    def get(self, request):
        page = request.query_params.get("page", 1)
        genres = request.query_params.get("genres")

        try:
            service = TMDBService()

            if genres:
                data = service.discover_tv(page=page, genres=genres)
            else:
                data = service.get_popular_tv(page)

            return success_response(data=data)

        except Exception as e:
            return error_response(error=str(e), status=502)


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Busca multi (filme, série, ator)",
        description="Busca em filmes, séries e atores via TMDB /search/multi.",
        parameters=[
            OpenApiParameter("query", OpenApiTypes.STR, required=True, description="Termo de busca"),
            OpenApiParameter("page", OpenApiTypes.INT, description="Número da página (default: 1)"),
        ],
        tags=["TMDB"],
    )
    def get(self, request):
        query = request.query_params.get("query")
        if not query:
            return error_response(error="O parâmetro 'query' é obrigatório.")

        page = request.query_params.get("page", 1)
        try:
            data = TMDBService().search(query, page)
            return success_response(data=data)
        except Exception as e:
            return error_response(error=str(e), status=502)


class MovieDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Detalhes de um filme",
        description="Retorna detalhes completos de um filme via TMDB (inclui créditos e vídeos).",
        tags=["TMDB"],
    )
    def get(self, request, tmdb_id):
        try:
            data = TMDBService().get_movie_details(tmdb_id)
            return success_response(data=data)
        except Exception as e:
            return error_response(error=str(e), status=502)


class TVDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Detalhes de uma série",
        description="Retorna detalhes completos de uma série via TMDB (inclui créditos e vídeos).",
        tags=["TMDB"],
    )
    def get(self, request, tmdb_id):
        try:
            data = TMDBService().get_tv_details(tmdb_id)
            return success_response(data=data)
        except Exception as e:
            return error_response(error=str(e), status=502)


class PersonDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Detalhes de uma pessoa",
        description="Retorna detalhes de um ator/diretor via TMDB (inclui filmografia).",
        tags=["TMDB"],
    )
    def get(self, request, tmdb_id):
        try:
            data = TMDBService().get_person_details(tmdb_id)
            return success_response(data=data)
        except Exception as e:
            return error_response(error=str(e), status=502)

class GenresView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Lista de gêneros",
        description="Retorna gêneros de filmes ou séries do TMDB",
        parameters=[
            OpenApiParameter(
                "type",
                OpenApiTypes.STR,
                description="movie ou tv (default: movie)",
            ),
        ],
        tags=["TMDB"],
    )
    def get(self, request):
        media_type = request.query_params.get("type", "movie")

        try:
            service = TMDBService()

            if media_type == "tv":
                data = service.get_tv_genres()
            else:
                data = service.get_movie_genres()

            return success_response(data=data)

        except Exception as e:
            return error_response(error=str(e), status=502)