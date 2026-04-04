class CursorIdPagination:
    """
    Paginação cursor-based usando ID para infinite scroll.

    A ordenação do queryset NÃO é sobrescrita — o chamador define a ordenação.
    O cursor filtra `id < last_id` para avançar a página de forma eficiente.

    Atenção: quando a ordenação primária não é por `id`, itens podem se
    reposicionar entre páginas se likes/comentários mudarem. Isso é
    comportamento aceito em feeds sociais.

    Query params:
        limit   — itens por página (default: 10, max: 100)
        last_id — cursor: retorna itens com id < last_id
    """

    default_limit = 10
    max_limit = 100

    def paginate_queryset(self, queryset, request):
        try:
            self.limit = min(
                int(request.query_params.get("limit", self.default_limit)),
                self.max_limit,
            )
        except (ValueError, TypeError):
            self.limit = self.default_limit

        last_id = request.query_params.get("last_id")
        if last_id:
            try:
                queryset = queryset.filter(id__lt=int(last_id))
            except (ValueError, TypeError):
                pass

        # Preserva a ordenação existente — não faz order_by("-id")
        items = list(queryset[: self.limit + 1])
        self.has_more = len(items) > self.limit
        self._results = items[: self.limit]
        return self._results

    def get_paginated_data(self, data):
        next_cursor = self._results[-1].id if self._results and self.has_more else None
        return {
            "results": data,
            "next_cursor": next_cursor,
            "has_more": self.has_more,
        }
