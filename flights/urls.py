from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_search, name='flight_search'),
    path('details/', views.flight_details, name='flight_details'),
]