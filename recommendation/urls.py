from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_decision, name='flight_decision'),
    path('decision_all/', views.flight_decision_all, name='flight_decision_all'),
    # path('decision_city', views.flight_decision_city, name='flight_decision_city'),
    path('decision_date/', views.flight_decision_date, name='flight_decision_date'),
]