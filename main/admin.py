from django.contrib import admin
from . models import Poll, Pollster, Poll_Aggregate
# Register your models here.

from main.models import Pollster
from main.views import update_daily_aggregates

class PollsterAdmin(admin.ModelAdmin):
    list_display = ("name_of_pollster",)
class Poll_AggregateAdmin(admin.ModelAdmin):
    list_display =("date",)

class PollAdmin(admin.ModelAdmin):
    
    
    list_display = ("date_published","pollster",)

    def save_model(self,request,obj, form, change):
        super().save_model(request,obj,form,change)

        update_daily_aggregates()

    

admin.site.register(Poll_Aggregate, Poll_AggregateAdmin)
admin.site.register(Pollster,PollsterAdmin)
admin.site.register(Poll, PollAdmin)