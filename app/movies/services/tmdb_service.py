import requests
from django.conf import settings


class TMDBService:

    def __init__(self):
        self.base_url = settings.TMDB_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.TMDB_API_KEY}",
            "Content-Type": "application/json;charset=utf-8",
        }

    def _get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        merged_params = {"language": "pt-BR", **(params or {})}
        response = requests.get(url, headers=self.headers, params=merged_params, timeout=10)

        if response.status_code != 200:
            raise Exception(f"TMDB Error {response.status_code}: {response.text}")

        return response.json()

    def get_popular_movies(self, page=1):
        return self._get("/movie/popular", {"page": page})

    def get_popular_tv(self, page=1):
        return self._get("/tv/popular", {"page": page})

    def search(self, query, page=1):
        return self._get("/search/multi", {"query": query, "page": page})

    def get_movie_details(self, movie_id):
        return self._get(f"/movie/{movie_id}", {"append_to_response": "credits,videos"})

    def get_tv_details(self, tv_id):
        return self._get(f"/tv/{tv_id}", {"append_to_response": "credits,videos"})

    def get_person_details(self, person_id):
        return self._get(f"/person/{person_id}", {"append_to_response": "movie_credits,tv_credits"})
    def discover_movies(self, page=1, genres=None, sort_by="popularity.desc"):
        params = {
            "page": page,
            "sort_by": sort_by,
        }

        if genres:
            params["with_genres"] = genres

        return self._get("/discover/movie", params)


    def discover_tv(self, page=1, genres=None, sort_by="popularity.desc"):
        params = {
            "page": page,
            "sort_by": sort_by,
        }

        if genres:
            params["with_genres"] = genres

        return self._get("/discover/tv", params)


    def get_movie_genres(self):
        return self._get("/genre/movie/list")


    def get_tv_genres(self):
        return self._get("/genre/tv/list")
