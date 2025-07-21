from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import (TopTradedCoinsAPIView, AnalystViewSet, )

router = DefaultRouter()
router.register(r"analyst", AnalystViewSet, basename="analyst")


urlpatterns = [
    path("most-traded-coins/", TopTradedCoinsAPIView.as_view(), name="most-traded-coins"),
]

urlpatterns += router.urls