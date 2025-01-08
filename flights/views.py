from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'flights/home.html')

def flight_search(request):
    return render(request, 'flights/search.html')

def flight_details(request):
    return render(request, 'flights/details.html')

def flight_cancellation(request):
    return render(request, 'flights/cancellation.html')

def flight_decision(request):
    return render(request, 'flights/decision.html')

def flight_decision_all(request):
    return render(request, 'flights/decision_all.html')

def flight_decision_city(request):
    return render(request, 'flights/decision_city.html')

def flight_decision_date(request):
    return render(request, 'flights/decision_date.html')