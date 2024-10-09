
from django.urls import path
from .views import CollectView, RedirectCollectView, CrawlView
from django.views.generic import TemplateView, View, ListView

urlpatterns = [
    path('', RedirectCollectView.as_view(), name='redirect_collect'),
    path('<slug:username>/', CollectView.as_view(), name='main_monitor_page'),
    path('<slug:username>/crawl/', CrawlView.as_view(), name='crawl'),

]
