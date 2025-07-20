from django.contrib import admin
from django.utils.html import format_html
from .models import *


#====================================== EntryPoint Model ==============================================

@admin.register(EntryPoint)
class EntryPointAdmin(admin.ModelAdmin):
    list_display = ["coin", "entry_1", "entry_2", "entry_3", "significance", "created_at"]
    list_filter = ["significance", "created_at"]
    search_fields = ["coin", "significance"]
    ordering = ["id"]
    

#====================================== ExitPoint Model ================================================

@admin.register(ExitPoint)
class ExitPointAdmin(admin.ModelAdmin):
    list_display = ["coin", "exit_1", "exit_2", "exit_3", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["coin"]
    ordering = ["id"]
    
    
#====================================== BoughtCoin Model ==============================================

@admin.register(BoughtCoin)
class BoughtCoinAdmin(admin.ModelAdmin):
    list_display = ["coin", "usdt_rate_buy", "usdt_rate_sell", "bought_price_usdt", "sold_price_usdt", "bought_price_irt", "sold_price_irt", "is_available", "profit_display_usdt", "profit_display_irt", "bought_at", "sold_at"]
    list_filter = ["is_available"]
    search_fields = ["coin", "bought_at", "sold_at"]
    ordering = ["id"]
    list_editable = ["is_available"]
    readonly_fields = ["profit_display_usdt", "profit_display_irt"]

    def profit_display_usdt(self, obj):
        color = "green" if obj.profit_usdt and obj.profit_usdt > 0 else "red"
        return format_html(f"<span style='color: {color};'>{obj.profit_usdt:.2f}%</span>")
    profit_display_usdt.short_description = "Profit"
    
    def profit_display_irt(self, obj):
        color = "green" if obj.profit_irt and obj.profit_irt > 0 else "red"
        return format_html(f"<span style='color: {color};'>{obj.profit_irt:.2f}%</span>")
    profit_display_irt.short_description = "Profit"


#====================================== BoughtCoin Model ==============================================

@admin.register(Analyst)
class AnalystAdmin(admin.ModelAdmin):
    list_display = ["topic", "analyst", "sentiment", "text", "image", "created_at"]
    list_filter = ["sentiment"]
    search_fields = ["topic", "sentiment", "analyst"]
    ordering = ["id"]
    
    
#====================================== MostBoughtCoin Model ==========================================

@admin.register(MostBoughtCoin)
class MostBoughtCoinAdmin(admin.ModelAdmin):
    list_display = ["coin", "rank", "source", "created_at"]
    search_fields = ["coin", "created_at"]
    ordering = ["id"]


#======================================================================================================