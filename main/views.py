from django.shortcuts import render
from django.views.generic import ListView
from . models import Poll, Poll_Aggregate
from django.db.models import Avg
from django.http import JsonResponse
from datetime import date


# Create your views here.

def data_to_graph(request):

    data = Poll_Aggregate.objects.all().order_by("date")
    

    response_data = list(data.values("date", "trump_support", "harris_support", "kennedy_support", "includes_third_party" )) #this is going to be a list of dictionaries with these <-- keys
    #we arent sending the actual objects because they need to be JSON serializable for d3.js to understand what we need to do here.
    
    

    return JsonResponse(response_data, safe=False) # this safe = False is necessary because we are sending a list back, usually its just a dictionary. 



    
def update_daily_aggregates(): #this code is a bit error prone right now, might want to add some catch statements eventually because if there are no polls in the database, this code will fail
    # because Poll_aggregate will give a null value for harris_support and trump_support, and those cant be null.
    latest_date = date.today()

    harris_avg_h2h = round(Poll.objects.all().filter(third_party_support__isnull=True).aggregate(Avg("harris_support"))["harris_support__avg"],1)
    trump_avg_h2h = round(Poll.objects.all().filter(third_party_support__isnull=True).aggregate(Avg("trump_support"))["trump_support__avg"],1)

    harris_avg_3way = round(Poll.objects.all().filter(third_party_support__isnull=False).aggregate(Avg("harris_support"))["harris_support__avg"],1)
    trump_avg_3way = round(Poll.objects.all().filter(third_party_support__isnull=False).aggregate(Avg("trump_support"))["trump_support__avg"], 1)

    kennedy_3way = round(Poll.objects.all().filter(third_party_support__isnull=False).aggregate(Avg("third_party_support"))["third_party_support__avg"], 1)

    Poll_Aggregate.objects.update_or_create(
        date=latest_date,
        includes_third_party=False,
        defaults={ #this defaults bit is necessary, this is what updates our values. Here we need to update the support numbers based on some new poll. 
            "harris_support":harris_avg_h2h,
            "trump_support":trump_avg_h2h 
        }
        
    )
    Poll_Aggregate.objects.update_or_create(
        date=latest_date,
        includes_third_party=True,
        defaults={
            "harris_support":harris_avg_3way,
            "trump_support": trump_avg_3way,
            "kennedy_support": kennedy_3way
        } 
    )


class Homepage(ListView):
    template_name = "main/home_page.html"
    model = Poll
    context_object_name = "polls"
    


    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.filter(third_party_support__isnull=True).order_by("-date_published")
        return data

class Homepage_Three_Way(ListView):
    template_name = "main/home_page_threeway.html"
    model = Poll
    context_object_name = "polls"

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.filter(third_party_support__isnull=False).order_by("date_published")
        return data
    
