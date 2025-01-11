from django.db import models

# Create your models here.

from django.db import models

class hotels_availability(models.Model):
    hotel_id = models.IntegerField()
    checkin_date = models.DateField()
    is_available = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    currency = models.CharField(max_length=3, null=True)
    updated_at = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'hotels_availability'  # ✅ 기존 테이블 이름과 연결
        managed = False

    def __str__(self):
        return f"Hotel {self.hotel_id} Availability"

class hotels_search(models.Model):
    hotel_id = models.CharField(max_length=100)
    hotel_name = models.CharField(max_length=200)
    airport_code = models.CharField(max_length=3)
    city_name = models.CharField(max_length=50)
    city_name_ko = models.CharField(max_length=50)
    place_id = models.CharField(max_length=100)
    place_name = models.CharField(max_length=200)
    review_score = models.FloatField()
    review_score_word = models.CharField(max_length=50)
    review_nr = models.IntegerField()
    checkin_time = models.CharField(max_length=50)
    checkout_time = models.CharField(max_length=50)
    hotel_class = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    distance = models.FloatField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'hotels_search'  # ✅ 기존 테이블 이름과 연결
        managed = False

    def __str__(self):
        return self.hotel_name