from django.shortcuts import render

# Create your views here.

def flight_cancellation(request):
    return render(request, 'prediction/cancellation.html')