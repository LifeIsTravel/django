from datetime import datetime
from itertools import product
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Flight


def flight_search(request):
    return render(request, 'flights/search.html')


def flight_details(request):
    # URL 파라미터 가져오기
    departure = request.GET.get('departure')
    destination = request.GET.get('destination')
    departure_date = request.GET.get('departureDate')
    return_date = request.GET.get('returnDate')
    sort_by = request.GET.get('sort', 'amount')  # 기본 정렬: 가격 오름차순
    page = request.GET.get('page', 1)  # 페이지 번호 가져오기

    # 정렬 키 설정
    if sort_by == 'carrier_names':
        order = 'carrier_names'
    else:
        order = 'amount'

    # 공항 코드와 이름 매핑
    airport_mapping = {
        'ICN': ['인천', 'ICN', '인천 국제 공항', '인천 공항', '서울'],
        "FUK": ['후쿠오카', 'FUK', '후쿠오카 공항'],
        "KIX": ['오사카/간사이', 'KIX', '간사이 국제 공항', '간사이 공항', '오사카', '간사이'],
        "NRT": ['도쿄/나리타', 'NRT', '나리타 국제 공항', '나리타 공항', '도쿄', '나리타'],
        "CTS": ['삿포로', 'CTS', '신치토세 공항', '삿포로 공항'],
    }

    # 공항 이름을 코드로 변환하는 함수
    def get_airport_code(airport_name):
        for code, names in airport_mapping.items():
            if airport_name in names:
                return code
        return airport_name  # 매핑되지 않으면 그대로 반환

    # 공항 이름을 코드로 변환
    departure_code = get_airport_code(departure)
    destination_code = get_airport_code(destination)

    # 날짜 포맷 변환 (촐출용)
    def format_display_date(date_str):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%B %d, %Y")  # 예: October 12, 2023
        except (ValueError, TypeError):
            return "N/A"

    # 날짜 포맷 변환 (검색용)
    def format_search_date(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%y%m%d")
        except (ValueError, TypeError):
            return None

    departure_date_formatted = format_search_date(departure_date)
    return_date_formatted = format_search_date(return_date) if return_date else None

    departure_date_display = format_display_date(departure_date)
    return_date_display = format_display_date(return_date) if return_date else None

    print(departure_code, destination_code, departure_date_formatted, return_date_formatted, sort_by)

    # 필터링 조건: stop_count가 0인 직항 항공편만
    outbound_flights = Flight.objects.filter(stop_count='0').order_by(order)
    inbound_flights = None

    # 출발편 필터링
    if departure_code and destination_code and departure_date_formatted:
        outbound_flights = outbound_flights.filter(
            departure_display_code=departure_code,
            arrival_display_code=destination_code,
            departure_date=departure_date_formatted
        )

    # 복귀편 필터링 (왕복인 경우)
    if return_date_formatted:
        if departure_code and destination_code and return_date_formatted:
            inbound_flights = Flight.objects.filter(stop_count='0').order_by(order).filter(
                departure_display_code=destination_code,
                arrival_display_code=departure_code,
                departure_date=return_date_formatted
            )

    # 가격, 바우처, 예약 링크가 null인 항공권을 제외
    outbound_flights = outbound_flights.exclude(amount__isnull=True, agent_name__isnull=True, url__isnull=True)
    if inbound_flights:
        inbound_flights = inbound_flights.exclude(amount__isnull=True, agent_name__isnull=True, url__isnull=True)

    # 왕복일 경우 모든 조합 생성 후 총 가격 기준 정렬
    if inbound_flights:
        # 최대 선택할 항공권 수 제한 (예: 상위 100개)
        MAX_FLIGHTS = 100
        outbound_sorted = outbound_flights.order_by('amount')[:MAX_FLIGHTS]
        inbound_sorted = inbound_flights.order_by('amount')[:MAX_FLIGHTS]

        # 모든 조합 생성
        all_combinations = product(outbound_sorted, inbound_sorted)

        # 조합 리스트 초기화
        flight_combinations = []

        # 조합마다 총 가격 계산
        for outbound, inbound in all_combinations:
            total_price = outbound.amount + inbound.amount
            flight_combinations.append({
                'outbound': outbound,
                'inbound': inbound,
                'total_price': total_price
            })

        # 총 가격 오름차순으로 정렬
        flight_combinations_sorted = sorted(flight_combinations, key=lambda x: x['total_price'])

        # 필요에 따라 상위 N개만 표시 (예: 상위 1000개)
        MAX_COMBINATIONS = 1000  # 성능 문제를 피하기 위해 최대 제한
        flight_combinations_sorted = flight_combinations_sorted[:MAX_COMBINATIONS]

        # 시간 포맷 변환 함수 (조합 생성 후에 적용)
        def format_time(time_str):
            try:
                time_obj = datetime.strptime(time_str, "%y%m%d%H%M")
                return time_obj.strftime("%I:%M %p")
            except (ValueError, TypeError):
                return time_str

        # 시간 포맷 변환을 포함하여 최종 조합 리스트 생성
        formatted_combinations = []
        for combination in flight_combinations_sorted:
            formatted_outbound = {
                'carrier_names': combination['outbound'].carrier_names,
                'departure_display_code': combination['outbound'].departure_display_code,
                'arrival_display_code': combination['outbound'].arrival_display_code,
                'departure_time': format_time(combination['outbound'].departure_time),
                'arrival_time': format_time(combination['outbound'].arrival_time),
                'url': combination['outbound'].url,
                'amount': combination['outbound'].amount,
                'agent_name': combination['outbound'].agent_name,
            }
            formatted_inbound = {
                'carrier_names': combination['inbound'].carrier_names,
                'departure_display_code': combination['inbound'].departure_display_code,
                'arrival_display_code': combination['inbound'].arrival_display_code,
                'departure_time': format_time(combination['inbound'].departure_time),
                'arrival_time': format_time(combination['inbound'].arrival_time),
                'url': combination['inbound'].url,
                'amount': combination['inbound'].amount,
                'agent_name': combination['inbound'].agent_name,
            }
            formatted_combinations.append({
                'outbound': formatted_outbound,
                'inbound': formatted_inbound,
                'total_price': combination['total_price']
            })

        # 페이지네이터 설정
        paginator = Paginator(formatted_combinations, 10)  # 한 페이지당 10개
        try:
            flight_combinations_page = paginator.page(page)
        except PageNotAnInteger:
            # 페이지 번호가 정수가 아니면 첫 페이지를 보여줌
            flight_combinations_page = paginator.page(1)
        except EmptyPage:
            # 페이지가 범위를 벗어나면 마지막 페이지를 보여줌
            flight_combinations_page = paginator.page(paginator.num_pages)

        context = {
            'flight_combinations': flight_combinations_page,
            'paginator': paginator,
            'page_obj': flight_combinations_page,
            'is_paginated': flight_combinations_page.has_other_pages(),
            'sort_by': sort_by,
            'departure_date_display': departure_date_display,
            'return_date_display': return_date_display,
        }
    else:
        # 편도 항공권을 위한 페이지네이션
        # 시간 포맷 변환 함수
        def format_time(time_str):
            try:
                time_obj = datetime.strptime(time_str, "%y%m%d%H%M")
                return time_obj.strftime("%I:%M %p")
            except (ValueError, TypeError):
                return time_str

        # 시간 포맷 변환
        formatted_flights = []
        for flight in outbound_flights:
            formatted_flight = {
                'carrier_names': flight.carrier_names,
                'departure_display_code': flight.departure_display_code,
                'arrival_display_code': flight.arrival_display_code,
                'departure_time': format_time(flight.departure_time),
                'arrival_time': format_time(flight.arrival_time),
                'amount': flight.amount,
                'agent_name': flight.agent_name,
                'url': flight.url,
            }
            formatted_flights.append(formatted_flight)

        # 페이지네이터 설정
        paginator = Paginator(formatted_flights, 10)  # 한 페이지당 10개
        try:
            flights_page = paginator.page(page)
        except PageNotAnInteger:
            # 페이지 번호가 정수가 아니면 첫 페이지를 보여줌
            flights_page = paginator.page(1)
        except EmptyPage:
            # 페이지가 범위를 벗어나면 마지막 페이지를 보여줌
            flights_page = paginator.page(paginator.num_pages)

        context = {
            'flights': flights_page,
            'paginator': paginator,
            'page_obj': flights_page,
            'is_paginated': flights_page.has_other_pages(),
            'sort_by': sort_by,
            'departure_date_display': departure_date_display,
        }

    return render(request, 'flights/details.html', context)
