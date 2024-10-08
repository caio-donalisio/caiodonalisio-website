# pages/urls.py
from django.urls import path
from .views import RobotsTxtView, BabyGifView

urlpatterns = [
    path('robots.txt', RobotsTxtView.as_view()),
    path('baby.gif', BabyGifView.as_view()),
]