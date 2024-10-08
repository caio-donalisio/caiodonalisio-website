#from django.http import HttpResponse
# def index(request):
#     return HttpResponse("<h3>Hello World</h3>")


from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'
    content_type = 'text/html'
    name='index'