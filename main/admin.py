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
    list_display = ["coin", "holding_value", "total_cost_usdt", "total_cost_irt_display", "avg_net_cost_usdt", "avg_net_cost_irt_display", "usdt_rate_buy_display", "usdt_rate_sell_display", "total_earn_usdt", "total_earn_irt_display", "profit_display_usdt", "profit_display_irt", "bought_at", "sold_at"]
    list_filter = ["is_available"]
    search_fields = ["coin", "bought_at", "sold_at"]
    ordering = ["id"]
    readonly_fields = ["profit_usdt", "profit_irt"]

    def profit_display_usdt(self, obj):
        if obj.profit_usdt is not None:
            color = "green" if obj.profit_usdt > 0 else "red"
            return format_html(f"<span style='color: {color};'>{obj.profit_usdt:.2f}</span>")
        return "-"
    profit_display_usdt.short_description = "Profit (USDT)"
    
    def profit_display_irt(self, obj):
        if obj.profit_irt is not None:
            color = "green" if obj.profit_irt > 0 else "red"
            return format_html(f"<span style='color: {color};'>{obj.profit_irt:,.0f}</span>")
        return "-"
    profit_display_irt.short_description = "Profit (IRT)"

    def total_cost_irt_display(self, obj):
        return f"{obj.total_cost_irt:,}" if obj.total_cost_irt is not None else "-"
    total_cost_irt_display.short_description = "Total Cost (IRT)"

    def avg_net_cost_irt_display(self, obj):
        return f"{obj.avg_net_cost_irt:,}" if obj.avg_net_cost_irt is not None else "-"
    avg_net_cost_irt_display.short_description = "AVG Net Cost (IRT)"
    
    def usdt_rate_buy_display(self, obj):
        return f"{obj.usdt_rate_buy:,}" if obj.usdt_rate_buy is not None else "-"
    usdt_rate_buy_display.short_description = "USDT Rate (Buy)"
    
    def usdt_rate_sell_display(self, obj):
        return f"{obj.usdt_rate_sell:,}" if obj.usdt_rate_sell is not None else "-"
    usdt_rate_sell_display.short_description = "USDT Rate (Sell)"
    
    def total_earn_irt_display(self, obj):
        return f"{obj.total_earn_irt:,}" if obj.total_earn_irt is not None else "-"
    total_earn_irt_display.short_description = "Total Earn (IRT)"


#====================================== BoughtCoin Model ==============================================

@admin.register(Analyst)
class AnalystAdmin(admin.ModelAdmin):
    list_display = ["analyst", "topic", "sentiment", "created_at"]
    list_filter = ["sentiment"]
    search_fields = ["topic", "sentiment", "analyst"]
    ordering = ["id"]
    
    
#====================================== MostBoughtCoin Model ==========================================

@admin.register(MostBoughtCoin)
class MostBoughtCoinAdmin(admin.ModelAdmin):
    list_display = ["created_at", "coins"]
    search_fields = ["coins", "created_at"]
    ordering = ["created_at"]


#======================================================================================================