from django.db import models

# Create your models here.

from django.db import models

class Flight(models.Model):
    extracted_at = models.DateTimeField(null=True, blank=True)
    departure_date = models.TextField()  # 날짜 정보가 텍스트 형식
    flight_id = models.IntegerField()  # 항공편 ID
    departure_display_code = models.CharField(max_length=10)  # 공항 코드
    departure_name = models.CharField(max_length=100)  # 출발지 이름
    arrival_display_code = models.CharField(max_length=10)  # 도착 공항 코드
    arrival_name = models.CharField(max_length=100)  # 도착지 이름
    carrier_names = models.TextField()  # 항공사 이름
    departure_time = models.TextField()  # 출발 시간
    arrival_time = models.TextField()  # 도착 시간
    agent_name = models.CharField(max_length=100)  # 에이전트 이름
    amount = models.FloatField()  # 가격
    url = models.TextField()  # URL
    last_updated = models.TextField()  # 마지막 업데이트 시간
    stop_count = models.TextField()  # 중간 기착지 수

    def __str__(self):
        return f"Flight {self.flight_id} from {self.departure_name} to {self.arrival_name}"


