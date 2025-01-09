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


