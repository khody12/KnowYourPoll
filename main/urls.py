from django.urls import path
from . import views

urlpatterns = [
    path("", views.Homepage.as_view(),name="home"),
    path("three-way-race", views.Homepage_Three_Way.as_view(),name="threeway")
]