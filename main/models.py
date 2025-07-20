from django.db import models, transaction
from django.conf import settings
from django.utils.timezone import now, localtime
from os import path
from uuid import uuid4


#======================================= Needed Method ================================================

def upload_to(instance, filename):
    file_name, ext = path.splitext(filename)
    new_filename = f"{uuid4()}{ext}"
    return f"photos/{new_filename}"


#====================================== EntryPoint Model ==============================================

class EntryPoint(models.Model):
    SIGNIFICANCE = [("1", "*"), ("2", "**"), ("3", "***"), ("4", "****"), ("5", "*****"),]
    coin = models.CharField(max_length=20, verbose_name="Coin")
    entry_1 = models.CharField(max_length=50, help_text="Enter range like: '2.13 - 1.78'", verbose_name="Entry Point 1")
    entry_2 = models.CharField(max_length=50, blank=True, null=True, help_text="Enter range like: '2.13 - 1.78'", verbose_name="Entry Point 2")
    entry_3 = models.CharField(max_length=50, blank=True, null=True, help_text="Enter range like: '2.13 - 1.78'", verbose_name="Entry Point 3")
    significance = models.CharField(max_length=10, choices=SIGNIFICANCE, verbose_name="Significance")
    signal_notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created At")

    def __str__(self):
        return f"{self.coin} at {self.entry_1}"

    def get_entry_range(self, field_name="entry_1"):
        value = getattr(self, field_name, "")
        if value and " - " in value:
            parts = value.replace(" ", "").split("-")
            try:
                return float(parts[0]), float(parts[1])
            except (ValueError, TypeError):
                return None
        return None

    class Meta:
        verbose_name = "Entry Point"
        verbose_name_plural = "Entry Points"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["coin"]),
            models.Index(fields=["significance"]),
        ]


#====================================== ExitPoint Model ================================================

class ExitPoint(models.Model):
    coin = models.CharField(max_length=20, verbose_name="Coin")
    exit_1 = models.CharField(max_length=50, verbose_name="Exit Point 1")
    exit_2 = models.CharField(max_length=50, blank=True, null=True, verbose_name="Exit Point 2")
    exit_3 = models.CharField(max_length=50, blank=True, null=True, verbose_name="Exit Point 3")
    signal_notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created At")

    def __str__(self):
        return f"{self.coin} at {self.exit_1}"

    class Meta:
        verbose_name = "Exit Point"
        verbose_name_plural = "Exit Points"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["coin"]),
        ]
        
        
#====================================== BoughtCoin Model ==============================================

class BoughtCoin(models.Model):
    coin = models.CharField(max_length=20, verbose_name="Coin")
    bought_price_usdt = models.DecimalField(max_digits=13, decimal_places=8, verbose_name="Bought Price USDT")
    bought_price_irt = models.IntegerField(verbose_name="Bought Price IRT")
    sold_price_usdt = models.DecimalField(max_digits=13, decimal_places=8, blank=True, null=True, verbose_name="Sold Price USDT")
    sold_price_irt = models.IntegerField(blank=True, null=True, verbose_name="Sold Price IRT")
    usdt_rate_buy = models.IntegerField(verbose_name="USDT Rate (buy)")
    usdt_rate_sell = models.IntegerField(verbose_name="USDT Rate (sell)")
    is_available = models.BooleanField(default=True, verbose_name="Being Available")
    profit_usdt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name="Profit USDT")
    profit_irt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name="Profit IRT")
    bought_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Bought At")
    sold_at = models.DateTimeField(blank=True, null=True, verbose_name="Sold At")

    def __str__(self):
        return f"{self.coin} bought at {self.bought_price_usdt} and sold at {self.sold_price_usdt}"
        
    def clean(self):
        self.change_availibility()
        self.add_profits()
    
    def change_availibility(self):
        if self.sold_price_usdt:
            self.is_available = False
            
    def add_profits(self):
        if self.sold_price_usdt and self.bought_price_usdt:
            change_usdt = (self.sold_price_usdt - self.bought_price_usdt) / self.bought_price_usdt
            self.profit_usdt = change_usdt * 100
        if self.sold_price_irt and self.bought_price_irt:
            change_irt = (self.sold_price_irt - self.bought_price_irt) / self.bought_price_irt
            self.profit_irt = change_irt * 100
    
    @property
    def total_irt_profit_from_usdt(self):
        if self.profit_usdt and self.usdt_rate_sell:
            return round((self.profit_usdt / 100) * self.usdt_rate_sell, 2)

    def fx_adjusted_profit(self):
        if self.usdt_rate_buy and self.usdt_rate_sell:
            # FX profit means IRT value of USDT changed over time
            rate_change = (self.usdt_rate_sell - self.usdt_rate_buy) / self.usdt_rate_buy
            return round(rate_change * 100, 2)
        return None

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Bought Coin"
        verbose_name_plural = "Bought Coins"
        ordering = ["-bought_at"]
        indexes = [
            models.Index(fields=["coin"]),
            models.Index(fields=["is_available"]),
        ]
        
        
#====================================== Analyst Model =================================================

class Analyst(models.Model):
    SENTIMENT = [("bullish", "Bullish"), ("bearish", "Bearish")]
    topic = models.CharField(max_length=30, verbose_name="Topic")
    analyst = models.CharField(max_length=20, verbose_name="Analyst")
    sentiment = models.CharField(max_length=10, choices=SENTIMENT, blank=True, null=True, verbose_name="Sentiment")
    text = models.TextField(verbose_name="Text")
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Chart")
    created_at = models.DateField(auto_now_add=True, editable=False, verbose_name="Created At")
    
    def __str__(self):
        return f"{self.analyst} posted at {self.created_at}"
    
    class Meta:
        verbose_name = "Analyst"
        verbose_name_plural = "Analysts"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["analyst"])]


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
