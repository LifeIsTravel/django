from django.db import models

# Create your models here.

class Flight(models.Model):
    departure = models.CharField(max_length=100)  # 출발지
    destination = models.CharField(max_length=100)  # 도착지
    departure_date = models.DateField(null=True, blank=True)  # 출발일
    departure_time = models.TimeField(null=True, blank=True) # 출발 시간
    return_date = models.DateField(null=True, blank=True)  # 귀국일 (옵션)
    return_time = models.TimeField(null=True, blank=True) # 도착 시간(옵션)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 항공권 가격
    airline = models.CharField(max_length=100)  # 항공사 이름
    agent_name = models.CharField(max_length=100, null=True, blank=True) # 바우처
    url = models.CharField(max_length=1000, null=True, blank=True) #예약 링크

    def __str__(self):
        return f"{self.airline} {self.departure} -> {self.destination} ({self.departure_date})"


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)  # 호텔 이름
    city = models.CharField(max_length=100)  # 도시명
    address = models.CharField(max_length=300, null=True, blank=True)  # 주소
    rating = models.FloatField(null=True, blank=True)  # 호텔 평점 (1~5 등)

    check_in = models.DateField(null=True, blank=True)  # 체크인 날짜
    check_out = models.DateField(null=True, blank=True)  # 체크아웃 날짜

    star_rating = models.IntegerField(null=True, blank=True)  # 별 개수(성급)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 숙박 가격

    # 호텔 상세 페이지, 예약 URL 등 필요한 필드가 있으면 추가 가능
    url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.hotel_name} - {self.city} ({self.check_in}~{self.check_out})"

