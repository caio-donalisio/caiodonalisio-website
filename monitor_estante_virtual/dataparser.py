import re
import bs4
from . import models
from typing import List, Dict, Generator
from functools import cached_property

class DataParser:
    def __init__(self, raw_data: str):
        self.raw_data = raw_data

    @cached_property
    def soup(self) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(self.raw_data, 'lxml')

    def _split_books(self) -> List[bs4.Tag]:
        return self.soup.find_all("div", class_="product-item product-list__item")

    def _parse_book(self, book: bs4.Tag) -> Dict:
        return dict(
            title=book.find("h2", 
                attrs={"class": "product-item__title product-item__title--mt product-item__name"}).text,
            author=book.find("p", 
                attrs={"class": "product-item__text product-item__text--mt product-item__author"}).text,
            book_type=self.get_book_type(book),
            price=book.find("span", attrs={"data-auto": "price"}).text,
            url= "https://www.estantevirtual.com.br/" + \
                book.find('a')['href'].replace('undefined',''),
        )
        
    def get_book_type(self, book):
        book_type = re.findall(r'(novo|usado)', book.find("p", class_="product-item__variations__text product-item__variations__item").text)
        if 'usado' in book_type and 'novo' in book_type:
            book_type='ambos'
        elif 'usado' in book_type:
            book_type='usado'
        elif 'novo' in book_type:
            book_type='novo'
        return book_type

    def _clean_book(self, book: bs4.Tag) -> Dict:
        return {key: self._clean_text(value) for key, value in book.items()}

    def _clean_text(self, text: str) -> str:
        return re.sub(r'\s{2,}', '', text).strip()

    def get_parsed_data(self) -> Generator:
        return [
            models.Book(**self._clean_book(self._parse_book(book))) for book in self._split_books()
        ]
