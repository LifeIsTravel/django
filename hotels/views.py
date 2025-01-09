from django.shortcuts import render

# Create your views here.

def hotel_search(request):
    # 도쿄 명소 데이터
    places_tokyo = [
        {"name": "도쿄 타워", "image": "tokyo_tower.jpg"},
        {"name": "도쿄 스카이트리", "image": "tokyo_skytree.jpg"},
        {"name": "메이지 신궁", "image": "meiji_shrine.jpg"},
        {"name": "센소지", "image": "sensoji.jpg"},
        {"name": "신주쿠 교엔", "image": "shinjuku_garden.jpg"},
    ]

    # 다른 도시 데이터도 유사하게 구성
    places_osaka = [
        {"name": "도톤보리", "image": "dontonbori.jpg"},
        {"name": "오사카 성", "image": "osaka_castle.jpg"},
    ]
    places_sapporo = [
        {"name": "삿포로시 시계탑", "image": "clock_tower.jpg"},
    ]
    places_fukuoka = [
        {"name": "오호리 공원", "image": "ohori_park.jpg"},
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
    return render(request, 'hotels/details.html')