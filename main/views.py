from django.shortcuts import render
from django.views.generic import ListView
from . models import Poll

# Create your views here.

class Homepage(ListView):
    template_name = "main/home_page.html"
    model = Poll
    
    
