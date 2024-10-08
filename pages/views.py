from django.views.generic import TemplateView
from django.views.decorators.http import require_GET


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
    
class BabyGifView(TemplateView):
    template_name = 'gif_display.html'
    content_type = 'text/html'