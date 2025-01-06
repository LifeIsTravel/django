from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.flight_search, name='flight_search'),
    path('details/', views.flight_details, name='flight_details'),
    path('cancellation/', views.flight_cancellation, name='flight_cancellation'),
]