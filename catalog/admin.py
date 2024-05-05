from django.contrib import admin
from .models import Category, Commodity, Anchor, SalesRecord,LivingTime,Gendered,AvgCostLevel,AnchorCategoryLink,CommodityAge,CommodityGendered,AnchorAge

# 注册 Category 模型
admin.site.register(Category)
admin.site.register(LivingTime)
admin.site.register(Gendered)
admin.site.register(AvgCostLevel)
admin.site.register(AnchorCategoryLink)
admin.site.register(CommodityAge)
admin.site.register(CommodityGendered)

class AnchorCategoryLinkInline(admin.TabularInline):
    model = AnchorCategoryLink 
class AvgCostLevelInline(admin.TabularInline):
    model = AvgCostLevel
class AnchorAgeInline(admin.TabularInline):
    model = AnchorAge
class GenderedInline(admin.TabularInline):
    model = Gendered
class CommodityGenderedInline(admin.TabularInline):
    model = CommodityGendered
class CommodityAgeInline(admin.TabularInline):
    model = CommodityAge
# 注册 SalesRecord 模型
@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('sale_date','anchor', 'category','commodity', 'soldon_date', 'soldout_date', 'price','status','sale_amount', 'extra_commission', 'total_amount','total_income')
    list_filter = ('sale_date', 'anchor', 'commodity', 'category','status','imprint')
    search_fields = ['sale_date', 'anchor', 'commodity', 'category','status']
    ordering = ['sale_date']
    
class SalesRecordAdminInline(admin.TabularInline):
    model = SalesRecord    
# 注册 Commodity 模型
@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'commission_rate', 'history_sell','history_amount','web_connect')
    list_filter = ('category',)
    search_fields = ['name']
    ordering = ['name']
    inlines = [SalesRecordAdminInline,CommodityGenderedInline,CommodityAgeInline]   
    
@admin.register(Anchor)
class AnchorAdmin(admin.ModelAdmin):
    list_display = ('name','amount', 'hire_date', 'base_salary','display_Category','display_Time','gender','Cost','commission', 'display_Commodity')
    search_fields = ['name']
    list_filter = ('hire_date',)
    ordering = ['name','amount',]
    inlines = [GenderedInline,AvgCostLevelInline,AnchorCategoryLinkInline,AnchorAgeInline]
    #inlines = [AvgCostLevelInline]
    
    


