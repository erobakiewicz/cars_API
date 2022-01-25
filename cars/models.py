from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.contrib import admin


class Car(models.Model):
    make = models.CharField("make", max_length=100)
    model = models.CharField("model", max_length=100, unique=True)

    def __str__(self):
        return f'{self.make}: {self.model}'

    @property
    @admin.display(description="average rating")
    def avg_rating(self):
        if car_rating := CarRating.objects.filter(car_id=self).aggregate(Avg('rating'))['rating__avg']:
            return car_rating
        return 0

    @property
    def rates_number(self):
        return CarRating.objects.filter(car_id=self).count()

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"


class CarRating(models.Model):
    car_id = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name="rated car id", related_name="ratings")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.car_id.model}: {self.rating}'

    class Meta:
        verbose_name = "Car rating"
        verbose_name_plural = "Cars ratings"
