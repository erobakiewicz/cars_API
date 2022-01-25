from rest_framework.routers import DefaultRouter

from cars.views import CarsViewSet

router = DefaultRouter()
router.register(r'cars', CarsViewSet, basename="cars")

urlpatterns = router.urls
