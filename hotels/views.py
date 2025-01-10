from django.shortcuts import render
from django.db.models import Q
from django.db.models import Sum
from .models import hotels_availability, hotels_search
from datetime import datetime, timedelta
# Create your views here.

def hotel_search(request):
    # 도쿄 명소 데이터
    places_tokyo = [
        {"name": "도쿄 타워", "image": "tokyo_tower.jpg"},
        {"name": "도쿄 스카이트리", "image": "tokyo_skytree.jpg"},
        {"name": "메이지 신궁", "image": "meiji_shrine.jpg"},
        {"name": "센소지", "image": "sensoji.jpg"},
        {"name": "신주쿠 교엔", "image": "shinjuku_garden.jpg"},
        {"name": "도쿄 디즈니랜드", "image": "tokyo_disneyland.jpg"},
        {"name": "하치코 동상", "image": "hachiko_statue.jpg"},
        {"name": "시부야 스카이", "image": "shibuya_sky.jpg"}
    ]

    # 다른 도시 데이터도 유사하게 구성
    places_osaka = [
        {"name": "도톤보리", "image": "dotonbori.jpg"},
        {"name": "오사카 성", "image": "osaka_castle.jpg"},
        {"name": "츠텐카쿠", "image": "tsutenkaku.jpg"},
        {"name": "유니버설 스튜디오 재팬", "image": "universal_studios_japan.jpg"},
        {"name": "우메다 스카이빌딩", "image": "umeda_sky_building.jpg"},
        {"name": "덴포잔 대관람차", "image": "tempozan_ferris_wheel.jpg"}
    ]
    places_sapporo = [
        {"name": "삿포로시 시계탑", "image": "sapporo_clock_tower.jpg"},
        {"name": "마루야마 공원", "image": "maruyama_park.jpg"},
        {"name": "삿포로 맥주 박물관", "image": "sapporo_beer_museum.jpg"},
        {"name": "오도리 공원", "image": "odori_park.jpg"},
        {"name": "삿포로 TV 타워", "image": "sapporo_tv_tower.jpg"}
    ]
    places_fukuoka = [
        {"name": "오호리 공원", "image": "ohori_park.jpg"},
        {"name": "후쿠오카타워", "image": "fukuoka_tower.jpg"},
        {"name": "마린월드 우미노나카미치", "image": "marine_world.jpg"},
        {"name": "하카타 향토관", "image": "hakata_traditional_crafts.jpg"}
    ]

    # 템플릿으로 데이터 전달
    context = {
        "places_tokyo": places_tokyo,
        "places_osaka": places_osaka,
        "places_sapporo": places_sapporo,
        "places_fukuoka": places_fukuoka,
    }
    return render(request, 'hotels/search.html', context)

def hotel_details(request):
    # URL 파라미터 가져오기
    checkin_date = request.GET.get('checkinDate')
    checkout_date = request.GET.get('checkoutDate')
    place = request.GET.get('place')
    sort_by = request.GET.get('sort', 'price')


    try:
        # 날짜 변환
        checkin_date_obj = datetime.strptime(checkin_date, '%Y-%m-%d').date()
        checkout_date_obj = datetime.strptime(checkout_date, '%Y-%m-%d').date()
        print(1)
        # 조회할 날짜 리스트 생성 (checkin부터 checkout 하루 전까지)
        stay_dates = [checkin_date_obj + timedelta(days=x) for x in range((checkout_date_obj - checkin_date_obj).days)]
        # 호텔 검색 (place_name으로 필터링)
        print(place)
        hotel_search_results = hotels_search.objects.filter(place_name=place)
        print(hotel_search_results)
        hotel_ids = hotel_search_results.values_list('hotel_id', flat=True)
        print(hotel_ids)
        final_results = []

        for hotel_id in hotel_ids:
            # 해당 호텔의 stay_dates 동안의 예약 가능 여부 확인
            availability = hotels_availability.objects.filter(
                hotel_id=hotel_id,
                checkin_date__in=stay_dates,
                is_available=True
            )
            print(availability)
            # 예약 가능 날짜 수 확인
            if availability.count() == len(stay_dates):
                # 모든 날짜가 예약 가능하면 가격 합산
                total_price = availability.aggregate(total=Sum('price'))['total']
                # 결과에 추가
                hotel_info = hotel_search_results.get(hotel_id=hotel_id)
                final_results.append({
                    'hotel_name': hotel_info.hotel_name,
                    'city_name_ko': hotel_info.city_name_ko,
                    'place_name': hotel_info.place_name,
                    'review_score': hotel_info.review_score,
                    'checkin_time': hotel_info.checkin_time,
                    'checkout_time': hotel_info.checkout_time,
                    'distance': hotel_info.distance,
                    'total_price': total_price,
                    'hotel_id': hotel_id
                })


        # 가격 기준으로 정렬
        if sort_by == 'price':
            final_results.sort(key=lambda x: x['total_price'])
        elif sort_by == 'review_score':
            final_results.sort(key=lambda x: x['review_score'], reverse=True)
        elif sort_by == 'distance':
            final_results.sort(key=lambda x: x['distance'])

        # 템플릿으로 전달
        return render(request, 'hotels/details.html', {'hotels': final_results, 'sort_by': sort_by})

    except Exception as e:
        return render(request, 'hotels/details.html', {'error': str(e)})