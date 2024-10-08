from django.shortcuts import render
from django.views.generic import FormView

# Create your views here.
class SignUpView(FormView):
    template_name = 'signup.html'
    
    