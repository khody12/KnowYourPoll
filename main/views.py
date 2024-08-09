from django.shortcuts import render
from django.views.generic import ListView
from . models import Poll

# Create your views here.

class Homepage(ListView):
    template_name = "main/home_page.html"
    model = Poll
    context_object_name = "polls"
    


    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.filter(third_party_support__isnull=True)
        return data

class Homepage_Three_Way(ListView):
    template_name = "main/home_page_threeway.html"
    model = Poll
    context_object_name = "polls"

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.filter(third_party_support__isnull=False)
        return data
    
