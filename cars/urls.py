from django.urls import path
from rest_framework.routers import DefaultRouter

from cars.views import CarsViewSet, CarRatingCreateAPIView, PopularCarListAPIView, AllCarsByMakeAPIView

router = DefaultRouter()
router.register(r'cars', CarsViewSet, basename="cars")

app_name = 'cars'

urlpatterns = [
    path(r'rate/', CarRatingCreateAPIView.as_view(), name='rate'),
    path(r'popular/', PopularCarListAPIView.as_view(), name='popular'),
    path(r'cars_by_make/', AllCarsByMakeAPIView.as_view(), name="cars_by_make")
]

urlpatterns += router.urls
