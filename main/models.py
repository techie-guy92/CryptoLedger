from django.db import models, transaction
from django.conf import settings
from django.utils.timezone import now, localtime
from os import path
from uuid import uuid4


#======================================= Needed Method ================================================

def upload_to(instance, filename):
    file_name, ext = path.splitext(filename)
    new_filename = f"{uuid4()}{ext}"
    coin = instance.logo
    return f"photos/{coin.replace(" ", "_")}/{new_filename}"


#====================================== TargetCoin Model ==============================================

class TargetCoin(models.Model):
    SIGNIFICANCE = [("1", "*"), ("2", "**"), ("3", "***"), ("4", "****"), ("5", "*****"),]
    coin = models.CharField(max_length=20, verbose_name="Coin")
    min_target_price = models.IntegerField(default=0, verbose_name="Min Price")
    max_target_price = models.IntegerField(default=0, verbose_name="Max Price")
    significance = models.CharField(max_length=10, choices=SIGNIFICANCE, verbose_name="Significance")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created At")


#====================================== BoughtCoin Model ==============================================

class BoughtCoin(models.Model):
    coin = models.CharField(max_length=20, verbose_name="Coin")
    bought_price = models.IntegerField(default=0, verbose_name="Min Price")
    sold_price = models.IntegerField(default=0, verbose_name="Min Price")
    is_available = models.BooleanField(default=True, verbose_name="Is Available")
    profit = models.IntegerField(verbose_name="Profit")
    bought_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Bought At")
    sold_at = models.DateTimeField(editable=False, verbose_name="Sold At")


#======================================================================================================
