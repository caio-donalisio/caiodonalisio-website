from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, View, ListView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.template.defaultfilters import slugify



from .models import Query, Book, Collection
from . import utils, crawler
import httpx
import logging

from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger(__name__)

class RedirectCollectView(LoginRequiredMixin, RedirectView):
    permanent = True
    
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            return HttpResponseRedirect(slugify(username))
        else:
            return redirect(f'/login/?next=/{slugify(username)}/')
    

class CollectView(LoginRequiredMixin, ListView):
    template_name = "query.html"
    content_type = "text/html"
    model = Query
    context_object_name = 'queries' 
    ordering = ['id']
    
    def get(self, request, username):
        if slugify(request.user.username) != username:
            return redirect('main_monitor_page', username=slugify(request.user.username))
        return render(request, 'query.html')
    
    def get_queryset(self):
        return Query.objects.filter(user=self.request.user)

class CrawlView(LoginRequiredMixin, View):
    
    def post(self, request, **kwargs):
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
            for item in crawler.Fetcher(
                session=httpx.Client(
                    headers=utils.default_headers(),
                    base_url="https://www.estantevirtual.com.br",
                ),
                query=query,
            ).run():
                print(item)
                break
                # yield str(item) + '<br>'

        return redirect('main_monitor_page', username=slugify(request.user.username))