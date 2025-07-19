from django.contrib import admin
from django.utils.html import format_html
from .models import *


#====================================== TargetCoin Model ==============================================

@admin.register(TargetCoin)
class TargetCoinAdmin(admin.ModelAdmin):
    list_display = ["coin", "min_target_price", "max_target_price", "significance", "created_at"]
    list_filter = ["significance", "created_at"]
    search_fields = ["coin", "significance"]
    ordering = ["id"]
    

#====================================== BoughtCoin Model ==============================================

@admin.register(BoughtCoin)
class BoughtCoinAdmin(admin.ModelAdmin):
    list_display = ["coin", "bought_price", "sold_price", "is_available", "profit_display", "bought_at", "sold_at"]
    list_filter = ["is_available",]
    search_fields = ["coin", "bought_at", "sold_at"]
    ordering = ["id"]
    list_editable = ["is_available"]
    readonly_fields = ["profit"]

    def profit_display(self, obj):
        color = "green" if obj.profit and obj.profit > 0 else "red"
        return format_html(f"<span style='color: {color};'>{obj.profit:.2f}%</span>")
    profit_display.short_description = "Profit"


#====================================== MostBoughtCoin Model ==========================================

@admin.register(MostBoughtCoin)
class MostBoughtCoinAdmin(admin.ModelAdmin):
    list_display = ["coin", "rank", "source", "created_at"]
    search_fields = ["coin", "created_at"]
    ordering = ["id"]


#======================================================================================================