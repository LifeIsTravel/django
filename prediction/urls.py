from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_cancellation, name='flight_cancellation'),
]