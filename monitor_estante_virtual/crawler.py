from . import data_parser, models, utils, query_transformer

# import utils
import re
import bs4
import httpx

# import data_parser
from typing import List
import datetime
from collections import defaultdict

#  TODO: add logging support
#  TODO: better error handling


class EstanteVirtualCrawler:
    def __init__(self, queries):
        self.queries = queries
        self.client = httpx.Client(
            headers=utils.default_headers(),
            base_url="https://www.estantevirtual.com.br",
        )
        self.data = defaultdict(list)

    def run(self):
        current_time = datetime.datetime.now()
        for query in self.queries:
            # print('\n\n' , 'Fetching...',query,'\n' + '-' * 50)
            for item in Fetcher(self.client, query).run():
                yield item
                # self.data[query].append(item)
                # ...
                # print(item)
        # return self


class Fetcher:
    def __init__(self, session: httpx.Client, query: List):
        self.query = query
        self.data = []
        self.website_count = False
        self.page_number = 0
        self.saved_count = 0
        self.limit = 120
        self.session = session

    def run(self):
        for item in self.fetch_all_pages():
            yield item

    def get_count(self) -> None:
        if self._search_initiated() and self._is_valid_page():
            counter = self.soup.find(
                "p",
                class_="product-list-header__sort__text",
                text=re.compile(r".*Exibindo: \d.*"),
            )
            if new_count := re.search(
                r".*?Exibindo\:\D*\d+.*?\D([\d\.]+)\s*resultados[\s\n]*$", counter.text
            ):
                new_count = utils.extract_number(new_count.group(1))
        return new_count

    def check_count(self) -> None:
        new_count = self.get_count()
        if self.website_count:
            if not new_count == self.website_count:
                raise utils.ContentUpdatedError(
                    f"Found different count of books in the same search! \n{new_count=} \n{self.website_count=}"
                )
            else:
                print(f"Found {new_count:_} books.")
            self.website_count = new_count

    @utils.retry()
    def fetch_page(self) -> str:
        self.response = self.session.get(
            url=f"/busca",
            params=query_transformer.QueryTransformer(
                query=self.query, page=self.page_number
            )(),
            follow_redirects=True,
        )
        self.response.raise_for_status()

    @utils.retry()
    def fetch_all_pages(self):
        while True and self.saved_count < self.limit:
            self._get_next_page()
            if not self._is_valid_page():
                break
            for item in data_parser.data_parser(self.response.text).get_parsed_data():
                yield item
                self.saved_count += 1

    def _get_next_page(self):
        self.page_number += 1
        self.fetch_page()

    def _is_valid_page(self) -> bool:
        return bool(
            not self.soup.find(
                text=re.compile(".*(Sua pesquisa não retornou nenhum resultado).*")
            )
            and not self.soup.find() is None
            and self._search_initiated()
        )

    def _search_initiated(self) -> bool:
        return hasattr(self, "response")

    @property
    def soup(self) -> bs4.BeautifulSoup:
        if self._search_initiated():
            return bs4.BeautifulSoup(
                markup=self.response.text,
                features="lxml",
                parse_only=bs4.SoupStrainer("div", class_="search"),
            )
        else:
            raise Exception("Search not initiated")
