from itertools import product

from django.shortcuts import render
from datetime import datetime, timedelta
from flights.models import Flight
from hotels.models import hotels_availability,hotels_search

# Create your views here.

def flight_decision(request):
    return render(request, 'recommendation/decision.html')

def flight_decision_all(request):
    # 1) URL 쿼리 파라미터 가져오기
    cities_str = request.GET.get('cities', '')
    cities_list = cities_str.split(',') if cities_str else []

    departure_start = request.GET.get('departureStart')
    departure_end   = request.GET.get('departureEnd')
    arrival_start   = request.GET.get('arrivalStart')
    arrival_end     = request.GET.get('arrivalEnd')

    budget_str = request.GET.get('budget', '0')
    try:
        budget = int(budget_str)
    except ValueError:
        budget = 0

    # 2) 날짜 형식 변환 (예: '2025-01-15' → '250115')
    def convert_date(date_str, format='%y%m%d'):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime(format)
        except (ValueError, TypeError):
            return None

    dep_start_conv = convert_date(departure_start)
    dep_end_conv   = convert_date(departure_end)
    arr_start_conv = convert_date(arrival_start)
    arr_end_conv   = convert_date(arrival_end)

    # 3) 출발편 필터링 (출발 → 목적지)
    departure_flights = Flight.objects.filter(
        departure_date__gte=dep_start_conv,
        departure_date__lte=dep_end_conv,
        arrival_display_code__in=cities_list
    )

    # 4) 복귀편 필터링 (목적지 → 출발지)
    return_flights = Flight.objects.filter(
        departure_date__gte=arr_start_conv,
        departure_date__lte=arr_end_conv,
        departure_display_code__in=cities_list
    )

    # 5) 호텔 정보 추출
    hotel_ids = hotels_search.objects.filter(
        airport_code__in=cities_list
    ).values_list('hotel_id', flat=True)

    hotels = hotels_availability.objects.filter(
        hotel_id__in=hotel_ids
    ).distinct('hotel_id')

    # 6) 출발일~복귀일 숙박 가능 여부 확인
    valid_combinations = []
    for dep_flight, ret_flight in product(departure_flights, return_flights):
        total_flight_price = dep_flight.price + ret_flight.price

        # 숙박 기간 계산
        checkin_date = datetime.strptime(dep_flight.departure_date, '%y%m%d')
        checkout_date = datetime.strptime(ret_flight.departure_date, '%y%m%d')
        stay_dates = [(checkin_date + timedelta(days=i)).strftime('%Y-%m-%d')
                      for i in range((checkout_date - checkin_date).days + 1)]

        for hotel in hotels:
            # 숙박 가능 여부 확인
            availability = hotels_availability.objects.filter(
                hotel_id=hotel.hotel_id,
                checkin_date__in=stay_dates,
                is_available=True
            ).count()

            if availability == len(stay_dates):
                # 호텔 가격 합산
                hotel_price = sum(
                    hotels_availability.objects.filter(
                        hotel_id=hotel.hotel_id,
                        checkin_date__in=stay_dates
                    ).values_list('price', flat=True)
                )

                total_price = total_flight_price + hotel_price

                # 예산 체크
                if total_price <= budget:
                    valid_combinations.append({
                        'departure': dep_flight,
                        'return': ret_flight,
                        'hotel': hotel,
                        'total_price': total_price
                    })

    # 7) 결과 렌더링
    return render(request, 'recommendation/decision_all.html', {'packages': valid_combinations})

def flight_decision_date(request):
    return render(request, 'recommendation/decision_date.html')

# def flight_decision_city(request):
#     return render(request, 'flights/decision_city.html')