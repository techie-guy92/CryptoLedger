from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from collections import Counter
from django.utils.timezone import now, localtime
from datetime import timedelta, date
from main.models import *
from main.serializers import *
from coingecko_utils import get_bulk_prices_sync


#====================================== Fetch Prices ==================================================

def fetch_prices(request):
    result = get_bulk_prices_sync()
    return JsonResponse(result["prices"])
        

#====================================== Top Traded Coins APIVie =======================================

@extend_schema(
    responses={200: TopTradedCoinEntrySerializer(many=True)},
    summary="Return most frequently traded coins",
    parameters=[
        OpenApiParameter(name='start_date', type=OpenApiTypes.DATE, required=False, description="Start date (YYYY-MM-DD)"),
        OpenApiParameter(name='end_date', type=OpenApiTypes.DATE, required=False, description="End date (YYYY-MM-DD)"),
        OpenApiParameter(name='limit', type=OpenApiTypes.INT, required=False, description="Number of top coins to return (default: 20)"),
    ],
)
class TopTradedCoinsAPIView(APIView):
    filter_backends = [DjangoFilterBackend]

    def get(self, request: Request):
        try:
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            limit = int(request.query_params.get("limit", 20)) 
            
            queryset = MostBoughtCoin.objects.all()
            
            if start_date and end_date:
                start_date = date.fromisoformat(start_date)
                end_date = date.fromisoformat(end_date)
                queryset = queryset.filter(created_at__range=(start_date, end_date))

            all_coins = []
            for entry in queryset:
                coins = [coin.strip() for coin in entry.coins.split(",") if coin.strip()]
                all_coins.extend(coins)

            coin_counts = Counter(all_coins)
            top_traded = coin_counts.most_common(limit)  
            result = [{"coin": coin, "count": count} for coin, count in top_traded]

            return Response(result, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"detail": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as error:
            return Response(
                {"detail": f"Something went wrong: {str(error)}"},
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