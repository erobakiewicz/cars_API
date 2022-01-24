from django.contrib import admin
from cars.models import Car, CarRating


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        'make',
        'model',
        'avg_rating'
    ]


@admin.register(CarRating)
class CarRatingAdmin(admin.ModelAdmin):
    pass
