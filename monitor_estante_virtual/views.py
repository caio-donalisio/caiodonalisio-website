from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.contrib.auth.views import LoginView

from .models import Query, Book
from . import utils, crawler
import httpx
import logging

logger = logging.getLogger(__name__)


class CollectView(TemplateView):
    template_name = "query.html"
    content_type = "text/html"
    name = "query"

class MonitorEstanteVirtualLoginView(LoginView):
    template_name = 'login.html'  # Specify the template for the login page
    redirect_authenticated_user = True    # Redirect if already logged in

class CrawlView(View):
    def get(self, request):
        
        ...
def crawl(request):
    queries = [
        Query(titulo="japan", preco_max=200),
        #         Query(titulo='japanese', preco_max=200),
        #         Query(titulo='japao', preco_max=200),
        #         Query(titulo='japones', preco_max=200),
        #         Query(titulo='japonesa', preco_max=200),
        #         Query(titulo='china', idioma='portugues', preco_max=200),
        #         Query(titulo='china', idioma='ingles', preco_max=200),
        #         Query(titulo='chinese', preco_max=200),
        #         Query(titulo='chines', preco_max=200),
        #         Query(titulo='chinesa', preco_max=200),
        #         Query(titulo='korea', preco_max=200),
        #         Query(titulo='korean', preco_max=200),
        #         Query(titulo='coreia', preco_max=200),
        #         Query(titulo='coreano', preco_max=200),
        #         Query(titulo='coreana', preco_max=200),
        #         Query(titulo='taiwan', preco_max=200),
        #         Query(titulo='taiwanese', preco_max=200),
        #         Query(autor='geny wakisaka'),
        #         Query(titulo_ou_autor='deng xiaoping'),
        #         Query(titulo_ou_autor='xi jinping'),
        #         Query(titulo_ou_autor='sun yat'),
        #         Query(autor='ronald dore'),
        #         Query(titulo_ou_autor='park chung hee'),
        #         Query(titulo_ou_autor='ryutaro komiya'),
        #         Query(autor='penelope francks'),
        #         Query(idioma='japones'),
    ]

    for query in queries:
        logger.info("")
        print(f"Fetching {str(query.__repr__())}")
        # yield str('<h3>\n\n' + 'Fetching...' + str(query) + '\n' + '-' * 50 + '</h3>')
        for item in crawler.Fetcher(
            session=httpx.Client(
                headers=utils.default_headers(),
                base_url="https://www.estantevirtual.com.br",
            ),
            query=query,
        ).run():
            (item)
            # yield str(item) + '<br>'

    return HttpResponse(str(query.__repr__()))
