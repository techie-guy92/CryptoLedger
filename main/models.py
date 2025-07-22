from django.db import models, transaction
from django.conf import settings
from django.utils.timezone import now, localtime
from os import path
from django.utils.text import slugify


#======================================= Needed Method ================================================

def upload_to(instance, filename):
    file_name, ext =path.splitext(filename)
    new_filename = f"{instance}{ext}"
    if isinstance(instance, EntryPoint):
        return f"images/EntryPoint/{slugify(instance.coin.lower(), allow_unicode=True)}/{new_filename}"
    elif isinstance(instance, ExitPoint):
        return f"images/ExitPoint/{slugify(instance.coin.lower(), allow_unicode=True)}/{new_filename}"
    elif isinstance(instance, BoughtCoin):
        return f"images/BoughtCoin/{slugify(instance.coin.lower(), allow_unicode=True)}/{new_filename}"
    elif isinstance(instance, Analyst):
        return f"images/Analyst/{slugify(instance.analyst.lower(), allow_unicode=True)}/{new_filename}"
    else:
        return f"images/others/{new_filename}"
    
    
#====================================== EntryPoint Model ==============================================

class EntryPoint(models.Model):
    SIGNIFICANCE = [("1", "*"), ("2", "**"), ("3", "***"), ("4", "****"), ("5", "*****"),]
    coin = models.CharField(max_length=20, verbose_name="Coin")
    entry_1 = models.CharField(max_length=50, help_text="Enter range like: '2.13 - 1.78'", verbose_name="Entry Point 1")
    entry_2 = models.CharField(max_length=50, blank=True, null=True, help_text="Enter range like: '2.13 - 1.78'", verbose_name="Entry Point 2")
    entry_3 = models.CharField(max_length=50, blank=True, null=True, help_text="Enter range like: '2.13 - 1.78'", verbose_name="Entry Point 3")
    significance = models.CharField(max_length=10, choices=SIGNIFICANCE, verbose_name="Significance")
    signal_notes = models.TextField(blank=True, null=True, verbose_name="Signal Notes")
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Image")
    created_at = models.DateField(auto_now_add=True, editable=False, verbose_name="Created At")

    def __str__(self):
        current_time = localtime(now())
        formatted_date = current_time.strftime("%Y-%m-%d")
        return f"{self.coin} {self.entry_1} {formatted_date}"

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
    signal_notes = models.TextField(blank=True, null=True, verbose_name="Signal Notes")
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Image")
    created_at = models.DateField(auto_now_add=True, editable=False, verbose_name="Created At")

    def __str__(self):
        current_time = localtime(now())
        formatted_date = current_time.strftime("%Y-%m-%d")
        return f"{self.coin} {self.exit_1} {formatted_date}"

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
    holding_value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Holding Value")
    total_cost_usdt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Cost (USDT)")
    total_cost_irt = models.IntegerField(verbose_name="Total Cost (IRT)")
    avg_net_cost_usdt = models.DecimalField(max_digits=14, decimal_places=8, verbose_name="AVG Net Cost (USDT)")
    avg_net_cost_irt = models.IntegerField(verbose_name="AVG Net Cost (IRT)")
    usdt_rate_buy = models.IntegerField(verbose_name="USDT Rate (Buy)")
    usdt_rate_sell = models.IntegerField(blank=True, null=True, verbose_name="USDT Rate (Sell)")
    total_earn_usdt = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Total Earn (USDT)")
    total_earn_irt = models.IntegerField(blank=True, null=True, verbose_name="Total Earn (IRT)")
    is_available = models.BooleanField(default=True, verbose_name="Being Available")
    profit_usdt = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Profit (USDT)")
    profit_irt = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Profit (IRT)")
    bought_at = models.DateField(auto_now_add=True, editable=False, verbose_name="Bought At")
    sold_at = models.DateField(blank=True, null=True, verbose_name="Sold At")

    def __str__(self):
        return f"{self.coin} bought at {self.avg_net_cost_usdt} and holding value is  {self.holding_value}"
        
    def clean(self):
        self.change_availibility()
        self.add_profits()
    
    def change_availibility(self):
        if self.total_earn_usdt:
            self.is_available = False
            self.sold_at = localtime(now())
            
    def add_profits(self):
        if self.total_cost_usdt and self.total_earn_usdt:
            self.profit_usdt = self.total_earn_usdt - self.total_cost_usdt
        if self.total_cost_irt and self.total_earn_usdt:
            self.profit_irt = self.total_earn_irt - self.total_cost_irt

    def fx_adjusted_profit(self):
        if self.usdt_rate_buy and self.usdt_rate_sell:
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
    ANALYST = [
        ("Il Capo", "CryptoCapo"), ("Hayes", "Arthur Hayes"), ("Kiyosaki", "Robert Kiyosaki"), ("Clay", "Alex Clay"), 
        ("Jonathan", "Jonathan Carter"), ("Butterfly", "Butterfly"), ("Noah", "Noah Lutz"), ("Ananda", "Master Ananda"),
        ("", ""),
        ]
    SENTIMENT = [("bullish", "Bullish"), ("bearish", "Bearish")]
    topic = models.CharField(max_length=30, verbose_name="Topic")
    analyst = models.CharField(max_length=30, choices=ANALYST, verbose_name="Analyst")
    sentiment = models.CharField(max_length=10, choices=SENTIMENT, blank=True, null=True, verbose_name="Sentiment")
    text = models.TextField(verbose_name="Text")
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Chart")
    created_at = models.DateField(auto_now_add=True, editable=False, verbose_name="Created At")

    def __str__(self):
        current_time = localtime(now())
        formatted_date = current_time.strftime("%Y-%m-%d")
        return f"{self.analyst} {self.topic} {formatted_date}"

    
    class Meta:
        verbose_name = "Analyst"
        verbose_name_plural = "Analysts"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["analyst"])]


#====================================== MostBoughtCoin Model ==========================================
        
class MostBoughtCoin(models.Model):
    SOURCE = [("1", "TradingView"), ("2", "CoinMarketCap"), ("3", "Cryptometer")]
    coins = models.TextField(verbose_name="Coins")
    source = models.CharField(max_length=20, choices=SOURCE, blank=True, null=True, verbose_name="Data Source")
    created_at = models.DateField(verbose_name="Created At")
    
    def __str__(self):
        return f"{self.coins} at {self.created_at}"
    
    class Meta:
        verbose_name = "Most Bought Coin"
        verbose_name_plural = "Most Bought Coins"
        indexes = [
            models.Index(fields=["coins"]),
            models.Index(fields=["source"]),
            models.Index(fields=["created_at"]),
        ]
        
        
#======================================================================================================
