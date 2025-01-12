from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_decision, name='flight_decision'),
    path('decision_all/', views.decision_all, name='flight_decision_all'),
    path('decision_date_range', views.flight_decision_date_range, name='flight_decision_date_range'),
    path('decision_date/', views.flight_decision_date, name='flight_decision_date'),
]