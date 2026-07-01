from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField, IntegerField
from .models import *


#====================================== MostBoughtCoin serializers ====================================

class TopTradedCoinEntrySerializer(Serializer):
    coin = CharField()
    count = IntegerField()
    
    
#====================================== Analyst serializers ===========================================
    
class AnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyst
        fields = "__all__"

    
#======================================================================================================