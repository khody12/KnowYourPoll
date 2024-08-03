from django.contrib import admin
from . models import Poll, Pollster
# Register your models here.

class PollsterAdmin(admin.ModelAdmin):
    list_display = ("name_of_pollster",)


admin.site.register(Pollster,PollsterAdmin)
admin.site.register(Poll)