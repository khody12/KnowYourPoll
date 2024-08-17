from django.shortcuts import render
from django.views.generic import ListView
from . models import Poll
from django.db.models import Avg


# Create your views here.


    
def update_daily_aggregates():
    latest_date = Poll.objects.latest('date_published').date_published

    harris_avg_h2h = Poll.objects.all().filter(third_party_support__isnull=True).aggregate(Avg("harris_support"))["harris_support__avg"]
    trump_avg_h2h = Poll.objects.all().filter(third_party_support__isnull=True).aggregate(Avg("trump_support"))["trump_support__avg"]



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
    
