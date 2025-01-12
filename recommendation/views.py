from datetime import datetime, timedelta

from django.shortcuts import render

from flights.models import Flight
from hotels.models import HotelAvailability, HotelSearch


# Create your views here.

def flight_decision(request):
    return render(request, 'recommendation/decision.html')


def decision_all(request):
    #  URL 쿼리 파라미터 가져오기
    cities_str = request.GET.get('cities', '')
    cities_list = cities_str.split(',') if cities_str else []

    departure_start = request.GET.get('departureStart')
    departure_end = request.GET.get('departureEnd')
    arrival_start = request.GET.get('arrivalStart')
    arrival_end = request.GET.get('arrivalEnd')

    budget_str = request.GET.get('budget', '0')
    budget_str = budget_str.replace(',', '')
    try:
        budget = int(budget_str)
    except ValueError:
        budget = 0
    print(budget)

    dep_start_conv = convert_date(departure_start)
    dep_end_conv = convert_date(departure_end)
    arr_start_conv = convert_date(arrival_start)
    arr_end_conv = convert_date(arrival_end)

    print(dep_start_conv, dep_end_conv, arr_start_conv, arr_end_conv)
    print()

    # 출발 날짜 범위와 도착 날짜 범위 생성
    departure_dates = generate_date_range(departure_start, departure_end)
    arrival_dates = generate_date_range(arrival_start, arrival_end)

    print(departure_dates, arrival_dates)

    # ================================================================================================================
    # 날짜 조합 만들기
    all_combinations = make_all_combinations(arrival_dates, departure_dates)
    # print("all_combinations_length", len(all_combinations))
    # print(all_combinations)

    # ================================================================================================================
    # 항공권 시작
    print(cities_list)
    all_flight_combinations = make_all_flight_combinations(all_combinations, cities_list)
    all_flight_combinations = filter_same_airports(all_flight_combinations)
    # print_flight_combinations(all_flight_combinations)

    # ================================================================================================================
    # 호텔 시작
    all_hotel_combinations = make_all_hotel_combinations(all_combinations)
    all_hotel_combinations = extract_city_from_hotel(all_hotel_combinations, cities_list)
    # print_hotel_combinations(all_hotel_combinations)

    # ================================================================================================================
    # 항공권 + 호텔 시작
    combined_combinations = make_combined_combinations(all_flight_combinations, all_hotel_combinations)
    combined_combinations = check_budget(budget, combined_combinations)
    # print_combined_combinations(combined_combinations)

    # ================================================================================================================
    # 가능한 날짜 조합 확인
    # print_common_dates(all_flight_combinations, all_hotel_combinations)

    # ================================================================================================================
    # 템플릿 형식에 맞게 고치기
    formatted_packages = make_formatted_packages(combined_combinations)

    # 결과 렌더링
    return render(request, 'recommendation/decision_all.html', {
        'cities': cities_list,
        'departure_start': departure_start,
        'departure_end': departure_end,
        'arrival_start': arrival_start,
        'arrival_end': arrival_end,
        'budget': budget,
        'packages': formatted_packages
    })


def flight_decision_date(request):
    departure_start = request.GET.get('departureStart')
    departure_end = request.GET.get('departureEnd')
    arrival_start = request.GET.get('arrivalStart')
    arrival_end = request.GET.get('arrivalEnd')
    print(departure_start, departure_end, arrival_start, arrival_end)

    budget_str = request.GET.get('budget', '0')
    budget_str = budget_str.replace(',', '')
    try:
        budget = int(budget_str)
    except ValueError:
        budget = 0
    print(budget)

    dep_start_conv = convert_date(departure_start)
    dep_end_conv = convert_date(departure_end)
    arr_start_conv = convert_date(arrival_start)
    arr_end_conv = convert_date(arrival_end)

    print(dep_start_conv, dep_end_conv, arr_start_conv, arr_end_conv)
    print()

    # 출발 날짜 범위와 도착 날짜 범위 생성
    departure_dates = generate_date_range(departure_start, departure_end)
    arrival_dates = generate_date_range(arrival_start, arrival_end)

    print(departure_dates, arrival_dates)

    # ================================================================================================================
    # 날짜 조합 만들기
    all_combinations = make_all_combinations(arrival_dates, departure_dates)
    # print("all_combinations_length", len(all_combinations))
    # print(all_combinations)

    # ================================================================================================================
    # 항공권 시작
    all_flight_combinations = make_all_flight_combinations(all_combinations, ['NRT', 'KIX', 'FUK', 'CTS'])
    all_flight_combinations = filter_same_airports(all_flight_combinations)
    # print_flight_combinations(all_flight_combinations)

    # ================================================================================================================
    # 호텔 시작
    all_hotel_combinations = make_all_hotel_combinations(all_combinations)
    all_hotel_combinations = extract_city_from_hotel(all_hotel_combinations, ['NRT', 'KIX', 'FUK', 'CTS'])
    # print_hotel_combinations(all_hotel_combinations)

    # ================================================================================================================
    # 항공권 + 호텔 시작
    combined_combinations = make_combined_combinations(all_flight_combinations, all_hotel_combinations)
    combined_combinations = check_budget(budget, combined_combinations)
    # print_combined_combinations(combined_combinations)

    # ================================================================================================================
    # 가능한 날짜 조합 확인
    # print_common_dates(all_flight_combinations, all_hotel_combinations)

    # ================================================================================================================
    # 템플릿 형식에 맞게 고치기
    formatted_packages = make_formatted_packages(combined_combinations)

    return render(request, 'recommendation/decision_date.html', {
        'departure_start': departure_start,
        'departure_end': departure_end,
        'arrival_start': arrival_start,
        'arrival_end': arrival_end,
        'budget': budget,
        'packages': formatted_packages
    })


def flight_decision_date_range(request):
    cities_str = request.GET.get('cities', '')
    print(cities_str)
    cities_list = cities_str.split(',') if cities_str else []
    if len(cities_list) == 0:
        cities_list = ['NRT', 'KIX', 'FUK', 'CTS']
    print(cities_list)

    stay_duration = request.GET.get('stayDuration')
    stay_duration = int(stay_duration)
    print(stay_duration)

    budget_str = request.GET.get('budget', '0')
    budget_str = budget_str.replace(',', '')
    try:
        budget = int(budget_str)
    except ValueError:
        budget = 0
    print(budget)

    first_date, last_date = generate_first_last_date()
    print("First Date (Tomorrow):", first_date)
    print("Last Date:", last_date)

    # ================================================================================================================
    # 날짜 조합 만들기
    all_combinations = generate_departure_arrival_dates(first_date, last_date, stay_duration)
    print("all_combinations_length", len(all_combinations))
    print(all_combinations)

    # ================================================================================================================
    # 항공권 시작
    all_flight_combinations = make_all_flight_combinations(all_combinations, cities_list)
    all_flight_combinations = filter_same_airports(all_flight_combinations)
    # print_flight_combinations(all_flight_combinations)

    # ================================================================================================================
    # 호텔 시작
    all_hotel_combinations = make_all_hotel_combinations(all_combinations)
    all_hotel_combinations = extract_city_from_hotel(all_hotel_combinations, cities_list)
    # print_hotel_combinations(all_hotel_combinations)

    # ================================================================================================================
    # 항공권 + 호텔 시작
    combined_combinations = make_combined_combinations(all_flight_combinations, all_hotel_combinations)
    combined_combinations = check_budget(budget, combined_combinations)
    # print_combined_combinations(combined_combinations)

    # ================================================================================================================
    # 가능한 날짜 조합 확인
    # print_common_dates(all_flight_combinations, all_hotel_combinations)

    # ================================================================================================================
    # 템플릿 형식에 맞게 고치기
    formatted_packages = make_formatted_packages(combined_combinations)

    return render(request, 'recommendation/decision_date_range.html', {
        'cities': cities_str,
        'stay_duration': stay_duration,
        'budget': budget,
        'packages': formatted_packages
    })


def generate_first_last_date():
    # Flight에서 가장 최근 departure_date를 가져오기
    latest_departure_date = Flight.objects.values('departure_date') \
        .distinct() \
        .order_by('-departure_date') \
        .first()
    # departure_date: 문자열 -> datetime 변환
    departure_date_str = latest_departure_date['departure_date']
    departure_date_as_datetime = datetime.strptime(departure_date_str, '%y%m%d').date()  # .date()로 시간 제외
    # HotelAvailability에서 가장 최근 checkin_date를 가져오기
    latest_checkin_date = HotelAvailability.objects.values('checkin_date') \
        .distinct() \
        .order_by('-checkin_date') \
        .first()
    # checkin_date: datetime.date -> datetime 변환
    checkin_date = latest_checkin_date['checkin_date']
    checkin_date_as_datetime = checkin_date  # 이미 datetime.date 객체
    # 더 빠른 날짜 선택
    last_date = min(departure_date_as_datetime, checkin_date_as_datetime)
    # 현재 날짜로부터 내일을 구해서 first_date 설정 (시간 제외)
    today = datetime.now().date()  # .date()로 시간 제외
    first_date = today + timedelta(days=1)
    return first_date, last_date


def generate_departure_arrival_dates(first_date, last_date, stay_duration):
    departure_arrival_list = []
    current_departure_date = first_date

    while current_departure_date <= last_date:
        # departure_date는 current_departure_date, arrival_date는 current_departure_date + stay_duration
        arrival_date = current_departure_date + timedelta(days=stay_duration)

        # arrival_date가 last_date를 넘지 않도록 조정
        if arrival_date > last_date:
            break

        # departure_date와 arrival_date를 딕셔너리 형태로 추가
        departure_arrival_list.append({
            'departure_date': current_departure_date.strftime('%Y-%m-%d'),
            'arrival_date': arrival_date.strftime('%Y-%m-%d')
        })

        # 다음 출발 날짜로 하루를 더함
        current_departure_date += timedelta(days=1)

    return departure_arrival_list


def generate_date_range(start_date_str, end_date_str):
    # 문자열을 datetime 객체로 변환
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # 날짜 범위 생성
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return date_list


#  날짜 형식 변환 (예: '2025-01-15' → '250115')
def convert_date(date_str, format='%y%m%d'):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime(format)
    except (ValueError, TypeError):
        return None


def print_common_dates(all_flight_combinations, all_hotel_combinations):
    print("\n=== 항공권의 날짜 조합 ===")
    flight_date_combinations = set()
    for flight in all_flight_combinations:
        departure_date = datetime.strptime(flight['departure_flight'].departure_date, '%y%m%d').strftime('%Y-%m-%d')
        return_date = datetime.strptime(flight['return_flight'].departure_date, '%y%m%d').strftime('%Y-%m-%d')
        flight_date_combinations.add(f"{departure_date} ~ {return_date}")
    for date_combo in sorted(flight_date_combinations):
        print(date_combo)
    print("\n=== 호텔의 날짜 조합 ===")
    hotel_date_combinations = set()
    for hotel in all_hotel_combinations:
        hotel_date_combinations.add(f"{hotel['check_in']} ~ {hotel['check_out']}")
    for date_combo in sorted(hotel_date_combinations):
        print(date_combo)
    # 공통된 날짜 조합 확인
    common_dates = flight_date_combinations.intersection(hotel_date_combinations)
    print("\n=== 공통된 날짜 조합 ===")
    for date_combo in sorted(common_dates):
        print(date_combo)
    print(f"\n총 항공권 날짜 조합 수: {len(flight_date_combinations)}")
    print(f"총 호텔 날짜 조합 수: {len(hotel_date_combinations)}")
    print(f"공통된 날짜 조합 수: {len(common_dates)}")


def print_combined_combinations(combined_combinations):
    # 결과 출력
    print(f"\n=== 항공권 + 호텔 조합 (총 {len(combined_combinations)}개) ===")
    for idx, combo in enumerate(combined_combinations, 1):
        print(f"\n[조합 {idx}] 총 여행 가격: {combo['total_price']:,.0f}원")

        print("\n[항공권 정보]")
        print(f"총 항공권 가격: {combo['flight']['total_price']:,.0f}원")
        print("출발편:")
        print(f"  항공편: {combo['flight']['departure_flight']['flight_id']}")
        print(f"  출발: {combo['flight']['departure_flight']['departure']}")
        print(f"  도착: {combo['flight']['departure_flight']['arrival']}")
        print(f"  날짜: {combo['flight']['departure_flight']['date']}")
        print(f"  가격: {combo['flight']['departure_flight']['amount']:,.0f}원")
        print("귀국편:")
        print(f"  항공편: {combo['flight']['return_flight']['flight_id']}")
        print(f"  출발: {combo['flight']['return_flight']['departure']}")
        print(f"  도착: {combo['flight']['return_flight']['arrival']}")
        print(f"  날짜: {combo['flight']['return_flight']['date']}")
        print(f"  가격: {combo['flight']['return_flight']['amount']:,.0f}원")

        print("\n[호텔 정보]")
        print(f"호텔 ID: {combo['hotel']['hotel_id']}")
        print(f"체크인: {combo['hotel']['check_in']}")
        print(f"체크아웃: {combo['hotel']['check_out']}")
        print(f"총 숙박일수: {combo['hotel']['total_nights']}박")
        print(f"총 호텔 가격: {combo['hotel']['total_price']:,.0f}원")
        print(f"일평균 가격: {combo['hotel']['average_price']:,.0f}원")
        print("일별 가격:", end=" ")
        for price in combo['hotel']['daily_prices']:
            print(f"{price:,.0f}원", end=" ")
        print()
        print("-" * 80)


def print_hotel_combinations(all_hotel_combinations):
    # 결과를 보기 좋게 출력
    print("\n=== 검색된 호텔 조합 ===")
    for idx, combo in enumerate(all_hotel_combinations, 1):
        print(f"\n[조합 {idx}]")
        print(f"호텔 ID: {combo['hotel_id']}")
        print(f"체크인: {combo['check_in']}")
        print(f"체크아웃: {combo['check_out']}")
        print(f"총 숙박일수: {combo['total_nights']}박")
        print(f"총 가격: {combo['total_price']:,.2f} {combo['currency']}")
        print(f"일평균 가격: {combo['average_price']:,.2f} {combo['currency']}")
        print("일별 가격:", end=" ")
        for price in combo['daily_prices']:
            print(f"{price:,.2f}", end=" ")
        print()
        print("-" * 50)


def print_flight_combinations(all_flight_combinations):
    # 결과 출력을 위한 all_flight_combinations 출력
    print("\n=== 검색된 항공권 조합 ===")
    for idx, combo in enumerate(all_flight_combinations[:100], 1):  # 상위 100개만 출력
        print(f"\n[조합 {idx}]")
        print(f"총 가격: {combo['total_amount']:,.0f}원")
        print(f"출발편: 항공편 {combo['departure_flight'].flight_id}, "
              f"{combo['departure_flight'].departure_display_code} -> {combo['departure_flight'].arrival_display_code}, "
              f"날짜: {combo['departure_flight'].departure_date}, "
              f"가격: {combo['departure_flight'].amount:,.0f}원")
        print(f"귀국편: 항공편 {combo['return_flight'].flight_id}, "
              f"{combo['return_flight'].departure_display_code} -> {combo['return_flight'].arrival_display_code}, "
              f"날짜: {combo['return_flight'].departure_date}, "
              f"가격: {combo['return_flight'].amount:,.0f}원")
        print("-" * 50)


def make_formatted_packages(combined_combinations):
    # 기존 combined_combinations를 템플릿 형식에 맞게 재구성
    formatted_packages = []
    for combo in combined_combinations:
        formatted_package = {
            'total_price': combo['total_price'],
            'departure': {
                'airline': combo['flight']['departure_flight']['flight_id'],
                'departure_display_code': combo['flight']['departure_flight']['departure'],
                'arrival_display_code': combo['flight']['departure_flight']['arrival'],
                'departure_date': datetime.strptime(combo['flight']['departure_flight']['date'], '%y%m%d').strftime(
                    '%Y-%m-%d'),
                'departure_time': datetime.strptime(combo['flight']['departure_flight']['departure_time'],
                                                    '%y%m%d%H%M').strftime('%I:%M %p'),
                'arrival_time': datetime.strptime(combo['flight']['departure_flight']['arrival_time'],
                                                  '%y%m%d%H%M').strftime('%I:%M %p'),
                'amount': combo['flight']['departure_flight']['amount']
            },
            'return': {
                'airline': combo['flight']['return_flight']['flight_id'],
                'departure_display_code': combo['flight']['return_flight']['departure'],
                'arrival_display_code': combo['flight']['return_flight']['arrival'],
                'departure_date': datetime.strptime(combo['flight']['return_flight']['date'], '%y%m%d').strftime(
                    '%Y-%m-%d'),
                'departure_time': datetime.strptime(combo['flight']['return_flight']['departure_time'],
                                                    '%y%m%d%H%M').strftime('%I:%M %p'),
                'arrival_time': datetime.strptime(combo['flight']['return_flight']['arrival_time'],
                                                  '%y%m%d%H%M').strftime('%I:%M %p'),
                'price': combo['flight']['return_flight']['amount']
            },
            'hotel': {
                'hotel_name': f"Hotel #{combo['hotel']['hotel_id']}",  # 호텔 이름이 없는 경우 ID로 대체
                'city': combo['flight']['departure_flight']['arrival'],  # 도착 도시를 호텔 도시로 사용
                'check_in': combo['hotel']['check_in'],
                'check_out': combo['hotel']['check_out']
            },
            'hotel_price': combo['hotel']['total_price']
        }
        formatted_packages.append(formatted_package)
    return formatted_packages


def check_budget(budget, combined_combinations):
    # combined_combinations 필터링
    filtered_combinations = []
    for combo in combined_combinations:
        # 총 비용 계산 항공권왕복 + 호텔총가격
        total_cost = combo['flight']['total_price'] + combo['hotel']['total_price']

        # budget 이하인 조합만 포함
        if budget == 0 or total_cost <= budget:  # budget이 0이면 제한 없음
            filtered_combinations.append(combo)
    # 필터링된 결과로 업데이트
    combined_combinations = filtered_combinations
    # 가격순 정렬 (필요한 경우)
    combined_combinations.sort(key=lambda x: (x['flight']['total_price'] + x['hotel']['total_price']))
    return combined_combinations


def make_combined_combinations(all_flight_combinations, all_hotel_combinations):
    # 항공권과 호텔 조합 매칭
    combined_combinations = []
    date_range_combinations = {}  # 날짜 범위별 조합을 저장할 딕셔너리
    for flight_combo in all_flight_combinations:
        # 항공권 날짜를 'YYYY-MM-DD' 형식으로 변환
        departure_date = datetime.strptime(flight_combo['departure_flight'].departure_date, '%y%m%d').strftime(
            '%Y-%m-%d')
        return_date = datetime.strptime(flight_combo['return_flight'].departure_date, '%y%m%d').strftime('%Y-%m-%d')

        # 날짜 범위 키 생성
        date_key = f"{departure_date}_{return_date}"

        # 날짜 범위별 리스트 초기화
        if date_key not in date_range_combinations:
            date_range_combinations[date_key] = []

        # 해당 날짜 범위의 조합이 이미 20개라면 다음 항공권으로 넘어감
        if len(date_range_combinations[date_key]) >= 20:
            continue

        for hotel_combo in all_hotel_combinations:
            # 날짜가 일치하는 경우에만 조합 생성
            if (hotel_combo['check_in'] == departure_date and hotel_combo['check_out'] == return_date) \
                    and hotel_combo['airport_code'] == flight_combo['departure_flight'].arrival_display_code:

                # 총 가격 계산 항공권 + 호텔
                total_trip_price = flight_combo['total_amount'] + hotel_combo['total_price']

                combined_combo = {
                    'total_price': total_trip_price,
                    'flight': {
                        'total_price': flight_combo['total_amount'],
                        'departure_flight': {
                            'flight_id': flight_combo['departure_flight'].flight_id,
                            'departure': flight_combo['departure_flight'].departure_display_code,
                            'arrival': flight_combo['departure_flight'].arrival_display_code,
                            'departure_time': flight_combo['departure_flight'].departure_time,
                            'arrival_time': flight_combo['departure_flight'].arrival_time,
                            'date': flight_combo['departure_flight'].departure_date,
                            'amount': flight_combo['departure_flight'].amount
                        },
                        'return_flight': {
                            'flight_id': flight_combo['return_flight'].flight_id,
                            'departure': flight_combo['return_flight'].departure_display_code,
                            'arrival': flight_combo['return_flight'].arrival_display_code,
                            'departure_time': flight_combo['return_flight'].departure_time,
                            'arrival_time': flight_combo['return_flight'].arrival_time,
                            'date': flight_combo['return_flight'].departure_date,
                            'amount': flight_combo['return_flight'].amount
                        }
                    },
                    'hotel': hotel_combo
                }

                # 해당 날짜 범위의 조합 리스트에 추가
                date_range_combinations[date_key].append(combined_combo)

                # 20개 도달하면 해당 날짜 범위의 호텔 검색 중단
                if len(date_range_combinations[date_key]) >= 20:
                    break
    # 각 날짜 범위별로 가격 순 정렬하고 최종 리스트에 추가
    for date_combos in date_range_combinations.values():
        date_combos.sort(key=lambda x: x['total_price'])
        combined_combinations.extend(date_combos[:20])  # 각 날짜 범위별 상위 20개만 추가
    # 전체 결과를 다시 한 번 가격순으로 정렬
    combined_combinations.sort(key=lambda x: x['total_price'])
    return combined_combinations


def extract_city_from_hotel(all_hotel_combinations, cities_list):
    # 해당 도시들의 호텔 ID와 airport_code 함께 가져오기
    hotel_airport_mapping = {
        str(hotel_id): airport_code
        for hotel_id, airport_code in HotelSearch.objects.filter(
            airport_code__in=cities_list
        ).values_list('hotel_id', 'airport_code')
    }

    # valid_hotel_ids에 포함된 호텔만 필터링하고 airport_code 추가
    filtered_combinations = []
    for combo in all_hotel_combinations:
        hotel_id = str(combo['hotel_id'])
        if hotel_id in hotel_airport_mapping:
            combo_with_airport = combo.copy()  # 원본 데이터 보존을 위해 복사
            combo_with_airport['airport_code'] = hotel_airport_mapping[hotel_id]
            filtered_combinations.append(combo_with_airport)

    # 필터링 후 다시 가격순 정렬
    filtered_combinations.sort(key=lambda x: x['total_price'])
    return filtered_combinations


def make_all_hotel_combinations(all_combinations):
    # 결과를 저장할 리스트
    all_hotel_combinations = []
    combinations_per_date = {}  # 날짜 조합별 결과를 저장할 딕셔너리
    for combination in all_combinations:
        dep_date = combination['departure_date']
        arr_date = combination['arrival_date']

        # 날짜 조합 키 생성
        date_key = f"{dep_date}-{arr_date}"

        # 해당 날짜 조합의 호텔이 아직 20개 미만인 경우에만 처리
        if date_key not in combinations_per_date:
            combinations_per_date[date_key] = []

        if len(combinations_per_date[date_key]) >= 20:
            continue

        # 체크인 날짜부터 체크아웃 전날까지의 모든 날짜 생성
        current_date = datetime.strptime(dep_date, '%Y-%m-%d')
        end_date = datetime.strptime(arr_date, '%Y-%m-%d')
        stay_dates = []
        while current_date < end_date:  # < 연산자를 사용하여 체크아웃 날짜 제외
            stay_dates.append(current_date.date())
            current_date += timedelta(days=1)

        # 기본 쿼리 설정
        base_query = HotelAvailability.objects.filter(
            is_available=True,
            price__isnull=False
        )

        # 해당 기간 동안 이용 가능한 호텔 찾기
        available_hotels = {}
        for date in stay_dates:  # 이미 체크아웃 날짜는 제외된 상태
            available_on_date = base_query.filter(
                checkin_date=date
            ).values('hotel_id', 'price', 'currency')

            # 각 호텔별 총 가격 계산
            for hotel in available_on_date:
                hotel_id = hotel['hotel_id']
                if hotel_id not in available_hotels:
                    available_hotels[hotel_id] = {
                        'total_price': 0,
                        'currency': hotel['currency'],
                        'available_all_dates': True,
                        'daily_prices': []
                    }
                available_hotels[hotel_id]['total_price'] += float(hotel['price'])
                available_hotels[hotel_id]['daily_prices'].append(float(hotel['price']))

        # 모든 날짜에 이용 가능한 호텔만 필터링하고 가격순 정렬
        valid_hotels = [
            {
                'hotel_id': k,
                'total_price': v['total_price'],
                'currency': v['currency'],
                'daily_prices': v['daily_prices'],
                'average_price': v['total_price'] / len(stay_dates)  # 실제 숙박 일수로 나눔
            }
            for k, v in available_hotels.items()
            if len(v['daily_prices']) == len(stay_dates)  # 체크아웃 날짜 제외된 상태로 비교
        ]
        valid_hotels.sort(key=lambda x: x['total_price'])

        # 상위 20개만 선택하여 저장
        for hotel in valid_hotels[:20]:
            if len(combinations_per_date[date_key]) >= 20:
                break

            combinations_per_date[date_key].append({
                'hotel_id': hotel['hotel_id'],
                'check_in': dep_date,
                'check_out': arr_date,
                'total_nights': len(stay_dates),  # 실제 숙박 일수 (체크아웃 날짜 제외)
                'total_price': hotel['total_price'],
                'average_price': hotel['average_price'],
                'currency': hotel['currency'],
                'daily_prices': hotel['daily_prices']  # 체크아웃 날짜 제외된 가격 리스트
            })

        # 전체 결과가 100개를 넘어가면 중단
        total_combinations = sum(len(combos) for combos in combinations_per_date.values())
        if total_combinations >= len(all_combinations) * 20:
            break
    # 모든 조합을 하나의 리스트로 합치기
    for date_combos in combinations_per_date.values():
        date_combos.sort(key=lambda x: x['total_price'])
        all_hotel_combinations.extend(date_combos)
    # 전체 결과를 가격 순으로 정렬하고 상위 100개만 반환
    all_hotel_combinations.sort(key=lambda x: x['total_price'])
    all_hotel_combinations = all_hotel_combinations[:len(all_combinations) * 20]
    return all_hotel_combinations


def filter_same_airports(all_flight_combinations):
    # 출발 공항과 도착 공항이 같은 항공편만 추출하는 함수
    same_airports_combinations = []
    for combination in all_flight_combinations:
        dep_flight = combination['departure_flight']
        ret_flight = combination['return_flight']

        # 출발 공항과 도착 공항이 같은 경우만 추가
        if dep_flight.arrival_display_code == ret_flight.departure_display_code:
            same_airports_combinations.append(combination)

    # 필터링 후 가격순으로 정렬
    same_airports_combinations.sort(key=lambda x: x['total_amount'])
    return same_airports_combinations


def make_all_flight_combinations(all_combinations, cities_list):
    # 결과를 저장할 리스트
    combinations_per_date = {}  # 날짜 조합별 결과를 저장할 딕셔너리
    for combination in all_combinations:
        dep_date_conv = convert_date(combination['departure_date'])
        arr_date_conv = convert_date(combination['arrival_date'])

        # 날짜 조합 키 생성
        date_key = f"{dep_date_conv}-{arr_date_conv}"

        if date_key not in combinations_per_date:
            combinations_per_date[date_key] = []

        if len(combinations_per_date[date_key]) >= 20:
            continue

        # 출발편 검색 (amount로 정렬하고 NULL 제외)
        departure_flights = Flight.objects.filter(
            departure_date=dep_date_conv,
            arrival_display_code__in=cities_list,
            amount__isnull=False
        ).order_by('amount')

        # 귀국편 검색 (amount로 정렬하고 NULL 제외)
        return_flights = Flight.objects.filter(
            departure_date=arr_date_conv,
            departure_display_code__in=cities_list,
            amount__isnull=False
        ).order_by('amount')

        # 각 출발편과 귀국편의 조합 생성
        for dep_flight in departure_flights:
            for ret_flight in return_flights:
                if len(combinations_per_date[date_key]) >= 20:
                    break

                total_amount = dep_flight.amount + ret_flight.amount
                flight_combo = {
                    'departure_flight': dep_flight,
                    'return_flight': ret_flight,
                    'total_amount': total_amount
                }
                combinations_per_date[date_key].append(flight_combo)

        # 전체 결과가 100개를 넘어가면 중단
        total_combinations = sum(len(combos) for combos in combinations_per_date.values())
        if total_combinations >= len(all_combinations) * 20:
            break

    # 모든 조합을 하나의 리스트로 합치기
    all_flight_combinations = []
    for date_combos in combinations_per_date.values():
        date_combos.sort(key=lambda x: x['total_amount'])  # 각 날짜 조합 내에서 가격순 정렬
        all_flight_combinations.extend(date_combos)

    # 전체 결과를 가격 순으로 정렬하고 상위 100개만 반환
    all_flight_combinations.sort(key=lambda x: x['total_amount'])
    all_flight_combinations = all_flight_combinations[:len(all_combinations) * 20]

    return all_flight_combinations


def make_all_combinations(arrival_dates, departure_dates):
    # 모든 가능한 날짜 조합 생성
    all_combinations = []
    for dep_date in departure_dates:
        for arr_date in arrival_dates:
            if dep_date < arr_date:
                all_combinations.append({
                    'departure_date': dep_date,
                    'arrival_date': arr_date
                })
    return all_combinations
