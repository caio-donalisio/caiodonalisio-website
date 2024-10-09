from .models import Query
from typing import Self


class QueryTransformer:

    def __init__(self, query: Query, page: int = 1) -> None:
        self._raw_query = query
        self.query = self._raw_query.__dict__
        self.page = page

    def run(self) -> Self:
        self.remove_extra_keys()
        self.add_price_key()
        self.add_search_field()
        self.get_api_terms()
        self.add_extra_params()
        return self

    def add_search_field(self) -> Self:
        translations = {
            "titulo": "titulo",
            "titulo_ou_autor": "titulo-autor",
            "autor": "autor",
            "isbn": "isbn",
            "editora": "editora",
        }
        for key in self.query:
            if key in translations:
                self.query = {**self.query, "searchField": translations[key]}
                break
        return self

    def add_price_key(self) -> dict:
        if any(key in self.query for key in ["preco_min", "preco_max"] if key):
            self.query["_preco"] = (
                f"{(self.query.get('preco_min') or 1) * 100}-{(self.query.get('preco_max') or 99_999) * 100}"
            )
            self.query.pop("preco_max", None), self.query.pop("preco_min", None)
        return self

    def get_api_terms(self) -> Self:
        termos = {
            "editora": "q",
            "titulo_ou_autor": "q",
            "titulo": "q",
            "autor": "q",
            "isbn": "q",
            "filtro": "qt",
            "cidade": "cidade",
            "vendedor": "vendedor",
            "idioma": "idioma",
            "ano_de_publicacao": "ano-de-publicacao",
            "assunto": "estante",
        }
        self.query = {
            termos.get(termo, termo): self.query[termo]
            for termo in self.query
            if self.query[termo]
        }
        return self

    def add_extra_params(self) -> Self:
        self.query = {
            **self.query,
            "page": self.page,
            "sort": "new-releases",  # Order by most recent
            "nsCat": "Natural",
        }
        return self

    def remove_extra_keys(self) -> Self:
        for key in ["_state", "id", "user_id", "created_at", "updated_at"]:
            self.query.pop(key, None)
        return self

    def __call__(self) -> dict:
        assert self.query == self._raw_query.__dict__
        return self.run().query
