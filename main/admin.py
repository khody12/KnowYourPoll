from django.contrib import admin
from . models import Poll, Pollster
# Register your models here.

from main.models import Pollster

class PollsterAdmin(admin.ModelAdmin):
    list_display = ("name_of_pollster",)
    

class PollAdmin(admin.ModelAdmin):
    
    
    list_display = ("date_published","pollster",)

    


admin.site.register(Pollster,PollsterAdmin)
admin.site.register(Poll, PollAdmin)