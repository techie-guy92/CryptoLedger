from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    AnalystViewSet,
    TopTradedCoinsAPIView,
    fetch_prices,
)

router = DefaultRouter()
router.register(r"perspectives", AnalystViewSet, basename="analyst")


urlpatterns = [
    path("fetch-prices/", fetch_prices, name="fetch_prices"),
    path(
        "most-traded-coins/", TopTradedCoinsAPIView.as_view(), name="most_traded_coins"
    ),
]

urlpatterns += router.urls
