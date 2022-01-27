from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.contrib import admin
from django.utils.functional import cached_property


class Car(models.Model):
    make = models.CharField("make", max_length=100)
    model = models.CharField("model", max_length=100, unique=True)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return f'{self.make}: {self.model}'

    @cached_property
    @admin.display(description="average rating")
    def avg_rating(self):
        if car_rating := self.ratings.aggregate(Avg('rating'))['rating__avg']:
            return round(car_rating, 1)
        return 0

    @cached_property
    def rates_number(self):
        return self.ratings.count()


class CarRating(models.Model):
    car_id = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name="rated car id", related_name="ratings")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = "Car rating"
        verbose_name_plural = "Cars ratings"

    def __str__(self):
        return f'{self.car_id.model}: {self.rating}'
