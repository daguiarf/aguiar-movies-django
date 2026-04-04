# Aguiar Movies API

API REST para gerenciamento de filmes, séries e fórum, construída com Django REST Framework e integrada à API do TMDB.

## Stack

- **Python 3 / Django 5** + Django REST Framework
- **MariaDB 11** (via Docker)
- **JWT** para autenticação (SimpleJWT)
- **Docker / Docker Compose**

## Funcionalidades

- Autenticação com JWT (registro, login, refresh)
- Integração com TMDB: filmes populares, séries, busca e detalhes
- Favoritos e Watchlist por usuário
- Reviews com nota (1–5)
- Fórum com posts, comentários e likes
- Paginação por cursor (fórum) e por página (TMDB)
- Documentação interativa via Swagger e ReDoc

## Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- Uma chave de API do [TMDB](https://www.themoviedb.org/settings/api) (Bearer Token — v4)

## Como rodar

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/aguiar-movies-api.git
cd aguiar-movies-api
```

**2. Configure as variáveis de ambiente**

```bash
cp .env.example .env
```

Edite o `.env` e preencha:
- `TMDB_API_KEY` — seu Bearer Token do TMDB
- `SECRET_KEY` — uma chave secreta Django (pode gerar com `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)

**3. Suba os containers**

```bash
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.

As migrations são aplicadas automaticamente na inicialização.

## Documentação

| Endpoint | Descrição |
|----------|-----------|
| `GET /api/docs/` | Swagger UI |
| `GET /api/redoc/` | ReDoc |
| `GET /api/schema/` | Schema OpenAPI (JSON) |

Para a documentação completa dos endpoints, consulte [API_DOCS.md](API_DOCS.md).

## Variáveis de ambiente

| Variável | Descrição |
|----------|-----------|
| `TMDB_API_KEY` | Bearer Token da API do TMDB |
| `TMDB_BASE_URL` | URL base do TMDB (padrão: `https://api.themoviedb.org/3`) |
| `DB_HOST` | Host do banco (padrão Docker: `db`) |
| `DB_NAME` | Nome do banco |
| `DB_USER` | Usuário do banco |
| `DB_PASSWORD` | Senha do banco |
| `DB_PORT` | Porta do banco (padrão: `3306`) |
| `SECRET_KEY` | Chave secreta do Django |

## Estrutura do projeto

```
.
├── app/
│   ├── accounts/       # Autenticação e usuários
│   ├── movies/         # Integração TMDB (filmes, séries, pessoas)
│   ├── user_lists/     # Favoritos e Watchlist
│   ├── reviews/        # Reviews
│   ├── forum/          # Fórum (posts, comentários, likes)
│   ├── core/           # Respostas e paginação compartilhadas
│   └── config/         # Settings, URLs, WSGI/ASGI
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── API_DOCS.md
```
