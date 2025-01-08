from django.shortcuts import render
from .models import Flight, Hotel
from django.db.models import Q

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
    flights = flights.order_by(order)

    return render(request, 'flights/details.html', {'flights': flights, 'sort_by': sort_by})

def flight_decision(request):
    return render(request, 'flights/decision.html')

def flight_decision_all(request):
    # 1) URL 쿼리 파라미터 가져오기
    cities_str = request.GET.get('cities', '')  # 예: "도쿄,오사카"
    if cities_str:
        cities_list = cities_str.split(',')  # ["도쿄", "오사카"]
    else:
        cities_list = []

    departure_start = request.GET.get('departureStart')  # "2025-01-08"
    departure_end   = request.GET.get('departureEnd')    # "2025-01-10"
    arrival_start   = request.GET.get('arrivalStart')    # "2025-01-08"
    arrival_end     = request.GET.get('arrivalEnd')      # "2025-01-16"
    budget_str      = request.GET.get('budget', '0')     # "500000" 등
    try:
        budget = int(budget_str)
    except ValueError:
        budget = 0

    # 2) Flight 모델 필터링
    flights_qs = Flight.objects.all()

    # flight.departure_date가 [departure_start, departure_end] 안에 있는지
    if departure_start and departure_end:
        flights_qs = flights_qs.filter(
            departure_date__range=(departure_start, departure_end)
        )

    # flight.return_date가 [arrival_start, arrival_end] 안에 있는지
    if arrival_start and arrival_end:
        flights_qs = flights_qs.filter(
            return_date__range=(arrival_start, arrival_end)
        )

    # 3) Hotel 모델 필터링
    hotels_qs = Hotel.objects.all()

    # 호텔의 city는 cities_list 중 하나여야 함
    if cities_list:
        hotels_qs = hotels_qs.filter(city__in=cities_list)

    # 호텔의 check_in이 [departure_start, departure_end] 범위 안에 있는지
    if departure_start and departure_end:
        hotels_qs = hotels_qs.filter(
            check_in__range=(departure_start, departure_end)
        )

    # 호텔의 check_out이 [arrival_start, arrival_end] 범위 안에 있는지
    if arrival_start and arrival_end:
        hotels_qs = hotels_qs.filter(
            check_out__range=(arrival_start, arrival_end)
        )

    # 4) Flight-Hotel 조합 찾기
    #    "flight.departure_date == hotel.check_in" AND "flight.return_date == hotel.check_out"
    results = []
    for flight in flights_qs:
        for hotel in hotels_qs:
            # 여기서 날짜가 정확히 같아야 한다고 했으므로, == 비교
            if (flight.departure_date == hotel.check_in) and (flight.return_date == hotel.check_out):
                total_cost = flight.price + hotel.price
                if total_cost <= budget:
                    results.append({
                        'flight': flight,
                        'hotel': hotel,
                        'total_cost': total_cost
                    })

    # 5) 필요 시 정렬
    # 예: 총액 오름차순
    # results = sorted(results, key=lambda x: x['total_cost'])

    context = {
        'results': results,
        'cities': cities_list,
        'departure_start': departure_start,
        'departure_end': departure_end,
        'arrival_start': arrival_start,
        'arrival_end': arrival_end,
        'budget': budget,
    }
    return render(request, 'flights/decision_all.html', context)

def flight_decision_date(request):
    return render(request, 'flights/decision_date.html')

def flight_cancellation(request):
    return render(request, 'flights/cancellation.html')

# def flight_decision_city(request):
#     return render(request, 'flights/decision_city.html')