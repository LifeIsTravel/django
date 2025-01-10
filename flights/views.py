from datetime import datetime
from django.shortcuts import render
from .models import Flight  # Flight 모델을 임포트하는 부분

def flight_search(request):
    return render(request, 'flights/search.html')

def flight_details(request):
    # URL 파라미터 가져오기
    departure = request.GET.get('departure')
    destination = request.GET.get('destination')
    departure_date = request.GET.get('departureDate')
    return_date = request.GET.get('returnDate')
    sort_by = request.GET.get('sort', 'amount')  # 기본 정렬: 가격 오름차순

    # 정렬 키 설정
    if sort_by == 'carrier_names':
        order = 'carrier_names'
    elif sort_by == 'amount':
        order = 'amount'
    else:
        order = 'amount'

    # 필터링 조건
    flights = Flight.objects.all()  # 기본적으로 모든 데이터
    if departure and destination and departure_date:
        departure_date_str = datetime.strptime(departure_date, "%Y-%m-%d").strftime("%y%m%d")
        if return_date:  # 왕복
            return_date_str = datetime.strptime(return_date, "%Y-%m-%d").strftime("%y%m%d")
            flights = flights.filter(
                departure_display_code=departure,
                arrival_display_code=destination,
                departure_date=departure_date_str,
                arrival_time__startswith=return_date_str[:6]  # arrival_time의 앞 6자만 비교
            )
        else:  # 편도
            flights = flights.filter(
                departure_display_code=departure,
                arrival_display_code=destination,
                departure_date=departure_date_str,
                arrival_time__isnull=True  # 왕복이 아닌 경우 arrival_time이 Null이어야 함
            )

    # 정렬 적용
    flights = flights.order_by(order)

    return render(request, 'flights/details.html', {'flights': flights, 'sort_by': sort_by})
