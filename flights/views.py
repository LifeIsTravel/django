from django.shortcuts import render
from .models import Flight

# Create your views here.

def home(request):
    return render(request, 'flights/home.html')

def flight_search(request):
    return render(request, 'flights/search.html')

def flight_details(request):
    # URL 파라미터 가져오기
    departure = request.GET.get('departure')
    destination = request.GET.get('destination')
    departure_date = request.GET.get('departureDate')
    return_date = request.GET.get('returnDate')
    sort_by = request.GET.get('sort', 'price')  # 기본 정렬: 가격 오름차순

    # 정렬 키 설정
    if sort_by == 'airline':
        order = 'airline'
    elif sort_by == 'price':
        order = 'price'
    else:
        order = 'price'

    # 필터링 조건
    flights = Flight.objects.all()  # 기본적으로 모든 데이터
    if departure and destination and departure_date:
        if return_date:  # 왕복
            flights = flights.filter(
                departure=departure,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date
            )
        else:  # 편도
            flights = flights.filter(
                departure=departure,
                destination=destination,
                departure_date=departure_date,
                return_date__isnull=True
            )

    # 정렬 적용
    #flights = flights.order_by(order)

    return render(request, 'flights/details.html', {'flights': flights, 'sort_by': sort_by})


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