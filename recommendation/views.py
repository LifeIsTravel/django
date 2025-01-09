from django.shortcuts import render

from flights.models import Flight
from hotels.models import Hotel


# Create your views here.

def flight_decision(request):
    return render(request, 'recommendation/decision.html')

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
    return render(request, 'recommendation/decision_all.html', context)

def flight_decision_date(request):
    return render(request, 'recommendation/decision_date.html')

# def flight_decision_city(request):
#     return render(request, 'flights/decision_city.html')