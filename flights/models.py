# Create your models here.

from django.db import models


class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True)  # 자동 증가되는 필드
    extracted_at = models.TextField()  # 추출된 날짜
    departure_date = models.TextField()  # 출발 날짜
    departure_display_code = models.CharField(max_length=10)  # 공항 코드
    departure_name = models.CharField(max_length=100)  # 출발지 이름
    arrival_display_code = models.CharField(max_length=10)  # 도착 공항 코드
    arrival_name = models.CharField(max_length=100)  # 도착지 이름
    carrier_names = models.TextField()  # 항공사 이름
    departure_time = models.TextField()  # 출발 시간
    arrival_time = models.TextField()  # 도착 시간
    agent_name = models.CharField(max_length=100, null=True)  # 바우처 이름
    amount = models.FloatField(null=True)  # 가격
    url = models.TextField(null=True)  # URL
    last_updated = models.TextField()  # 마지막 업데이트 시간
    stop_count = models.TextField()  # 중간 기착지 수

    class Meta:
        db_table = 'flight'  # 테이블 이름을 'flight'로 지정

    def __str__(self):
        return f"Flight {self.flight_id} from {self.departure_name} to {self.arrival_name}"
