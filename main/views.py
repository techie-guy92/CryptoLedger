from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from collections import Counter
from datetime import timedelta, date
from main.models import *
from main.serializers import *


#====================================== MostBoughtCoin View ===========================================

@extend_schema(
    responses={200: TopTradedCoinEntrySerializer(many=True)},
    summary="Return most frequently traded coins"
)
class TopTradedCoinsAPIView(APIView):
    def get(self, request: Request):
        try:
            start_date = date(2025, 7, 1)
            end_date = date(2025, 7, 15)
            entries = MostBoughtCoin.objects.filter(created_at__range=(start_date, end_date))
            
            queryset = MostBoughtCoin.objects.all()
            
            all_coins = []
            for entry in queryset:
                raw = entry.coins 
                coins = [coin.strip() for coin in raw.split(",") if coin.strip()]
                all_coins.extend(coins)
            coin_counts = Counter(all_coins)
            sorted_counts = sorted(coin_counts.items(), key=lambda item: item[1], reverse=True)
            top_traded = coin_counts.most_common(20)
            result = [{coin: count} for coin, count in top_traded]
            return Response(result, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(
                {"detail": f"Something went wrong while aggregating coins: {str(error)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#====================================== Analyst View ==================================================

class AnalystViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Analyst.objects.all()
    serializer_class = AnalystSerializer
    http_method_names = ["get"]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["analyst"]


#======================================================================================================