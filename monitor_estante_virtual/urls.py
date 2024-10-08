
from django.urls import path
from .views import CollectView, crawl

urlpatterns = [
    path('', CollectView.as_view()),
    path('crawl/', crawl, name='crawl'),

]
