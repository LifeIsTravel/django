from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.flight_search, name='flight_search'),
    path('hotels/', views.hotel_search, name='hotel_search'),
    path('details/', views.flight_details, name='flight_details'),
    path('hotel_details/', views.hotel_details, name='hotel_details'),
    path('cancellation/', views.flight_cancellation, name='flight_cancellation'),
    path('decision/', views.flight_decision, name='flight_decision'),
    path('decision_all/', views.flight_decision_all, name='flight_decision_all'),
    #path('decision_city', views.flight_decision_city, name='flight_decision_city'),
    path('decision_date', views.flight_decision_date, name='flight_decision_date'),
]