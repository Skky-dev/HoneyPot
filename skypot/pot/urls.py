from django.urls import path
from . import views

urlpatterns = [
    path('', views.pot_map, name="pot_map"),  
]