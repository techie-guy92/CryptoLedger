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
    min_target_price = models.DecimalField(max_digits=13, decimal_places=8, blank=True, null=True, verbose_name="Min Price")
    max_target_price = models.DecimalField(max_digits=13, decimal_places=8, blank=True, null=True, verbose_name="Max Price")
    significance = models.CharField(max_length=10, choices=SIGNIFICANCE, verbose_name="Significance")
    signal_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created At")

    def __str__(self):
        return f"{self.coin} at ({self.min_target_price} and {self.max_target_price})"

    class Meta:
        verbose_name = "Target Coin"
        verbose_name_plural = "Target Coins"
        indexes = [
            models.Index(fields=["coin"]),
            models.Index(fields=["significance"]),
        ]


#====================================== BoughtCoin Model ==============================================

class BoughtCoin(models.Model):
    coin = models.CharField(max_length=20, verbose_name="Coin")
    bought_price = models.DecimalField(max_digits=13, decimal_places=8, verbose_name="Min Price")
    sold_price = models.DecimalField(max_digits=13, decimal_places=8, blank=True, null=True, verbose_name="Min Price")
    is_available = models.BooleanField(default=True, verbose_name="Is Available")
    profit = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name="Profit (%)")
    bought_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Bought At")
    sold_at = models.DateTimeField(blank=True, null=True, verbose_name="Sold At")

    def __str__(self):
        return f"{self.coin} bought at {self.bought_price} and sold at {self.sold_price}"
        
    def save(self, *args, **kwargs):
        if self.sold_price:
            self.is_available = False
        if self.sold_price and self.bought_price:
            change = (self.sold_price - self.bought_price) / self.bought_price
            self.profit = change * 100
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Bought Coin"
        verbose_name_plural = "Bought Coins"
        indexes = [
            models.Index(fields=["coin"]),
            models.Index(fields=["is_available"]),
        ]
        
        
#====================================== MostBoughtCoin Model ==========================================
        
class MostBoughtCoin(models.Model):
    SOURCE = [("1", "TradingView"), ("2", "CoinMarketCap"), ("3", "Cryptometer")]
    coin = models.CharField(max_length=20, verbose_name="Coin")
    rank = models.IntegerField(blank=True, null=True, verbose_name="Rank")
    source = models.CharField(max_length=20, choices=SOURCE, verbose_name="Data Source")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created At")
    
    def __str__(self):
        return f"{self.coin} at {self.created_at}"
    
    class Meta:
        verbose_name = "Most Bought Coin"
        verbose_name_plural = "Most Bought Coins"
        indexes = [
            models.Index(fields=["coin"]),
            models.Index(fields=["created_at"]),
        ]
        
        
#======================================================================================================
