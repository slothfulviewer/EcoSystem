from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns

class Category(models.Model):
    """表示商品类别的模型（例如：日用品，食品）。"""
    name = models.CharField(
        max_length=200, 
        unique=True, 
        help_text="输入商品类别名称（例如：日用品，食品）")

    def get_absolute_url(self):
        """返回访问特定商品类别实例的 URL。"""
        return reverse('category-detail', args=[str(self.id)])  # 返回流派详情页的 URL

    def __str__(self):
        """用于表示模型对象的字符串（在管理界面等地方）。"""
        return self.name  # 返回商品类别   
    

         
class Commodity(models.Model):
    """表示商品信息的模型（但不是具体副本）。"""
    name = models.CharField('商品名称',max_length=200, help_text="输入商品名称")
    category = models.ForeignKey('category', on_delete=models.RESTRICT)
    price = models.DecimalField('商品价格(元)',max_digits=5, decimal_places=2, help_text="输入商品价格",default = 0)
    commission_rate = models.DecimalField('佣金比例（%）',max_digits=5, decimal_places=2,help_text="输入佣金比例(%)",default = 0)
    history_sell = models.DecimalField("过去30天销量(w件)",max_digits=5, decimal_places=2, help_text="输入过去30天销量(w件)",default = 0)
    history_amount = models.DecimalField("过去30天浏览量(w次)",max_digits=5, decimal_places=2,help_text="输入过去30天浏览量(w次)",default = 0)
    web_connect = models.CharField('商品网址',max_length=200, help_text="输入商品网址",default = 'www.buzhidao.com',null = True,blank=True)
    @property
    def gender(self):
        # 尝试返回与此Anchor实例关联的百分比属性
        # 如果没有找到，返回None或者默认值
        if hasattr(self, 'Commodity_gender'):
            return {
                '男': self.Commodity_gender.Male,
                '女': self.Commodity_gender.Female,
            }
        else:
            return {
                '男': 50,
                '女': 50,
                  }      # 返回一个包含默认值的字典
    @property
    def Age(self):
        # 尝试返回与此Anchor实例关联的百分比属性
        # 如果没有找到，返回None或者默认值
        if hasattr(self, 'Anchor_Age_Level'):
            return {
                '[18,23)': self.Anchor_Age_Level.mini,
                '[24,30)': self.Anchor_Age_Level.low,
                '[31,40)': self.Anchor_Age_Level.medi,
                '[41,50)': self.Anchor_Age_Level.high,
                '50+': self.Anchor_Age_Level.maxi,
            }
        else:
            return {
                '[18,23)': 20,
                '[24,30)': 20,
                '[31,40)': 20,
                '[41,50)': 20,
                '50+': 20,
            }            #返回一个包含默认值的字典
    
    class Meta:
            ordering = ['category','history_sell']  # 按商品名称和排序
            permissions = (("can_add_commodity", "增加商品数据"),)
            
    def save(self, *args, **kwargs):
        self.history_amount = self.history_amount
        super().save(*args, **kwargs)    
    def get_absolute_url(self):
        """返回访问特定商品记录的 URL。"""
        return reverse('Commodity-detail', args=[str(self.id)])  # 返回商品详情页的 URL

    def __str__(self):
        """用于表示模型对象的字符串。"""
        return self.name  # 返回商品名
import uuid  # 用于唯一直播实例
class CommodityGendered(models.Model):
    """表示商品受众性别百分比。"""
    Commodity = models.OneToOneField(Commodity, on_delete=models.CASCADE, related_name='Commodity_gender')
    Male = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    Female = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    def clean(self):
        # 确保的总和为100%
        total_percentage = self.Male + self.Female 
        if total_percentage != 100:
            raise ValidationError("总和必须为100%。当前总和为: {}".format(total_percentage))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)    
        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
class CommodityAge(models.Model): 
    """表示商品年龄百分比。"""    
    Commodity = models.OneToOneField(Commodity, on_delete=models.CASCADE, related_name='Commodity_Age_Level')
    mini = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    low = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    medi = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    high = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    maxi = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    def clean(self):
        # 确保总和为100%
        total_percentage = self.mini + self.low + self.medi + self.high + self.maxi
        if total_percentage != 100.00:
            raise ValidationError("总和必须为100%。当前总和为: {}".format(total_percentage))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)   
        

class AnchorCategoryLink(models.Model):
    '''链接主播与产品类型'''
    anchor = models.ForeignKey('Anchor', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sales_percentage =models.DecimalField(max_digits=5, decimal_places=2, default=20.00,help_text="商品销售额占比")
    def clean(self):
        if self.sales_percentage >=100:
            raise ValidationError("占比不能超过100%。当前为: {}".format(self.sales_percentage))
    class Meta:
        unique_together = (('anchor', 'category'),)
        ordering = ['sales_percentage']
    def __str__(self):
        """用于表示模型对象的字符串。"""
        return f"{self.category} - {self.sales_percentage }"  # 返回商品名


class LivingTime(models.Model):
    start_time = models.IntegerField(default=0,null = True,help_text="输入主播的直播时间")
    finally_time = models.IntegerField(default=24,null = True,help_text="输入主播的下播时间")
    def __str__(self):
        """用于表示模型对象的字符串（在管理界面等地方）。"""
        return f"{self.start_time} - {self.finally_time}" # 返回商品类别   
    
        
class Anchor(models.Model):
    name = models.CharField(max_length=200, help_text="输入主播名称")
    hire_date = models.DateField(help_text="输入主播的入职时间",default = "2024/05/01")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=20.00,help_text="输入主播的粉丝量（W人）",null=True)
    live_house = models.CharField(max_length=200,null=True, blank=True,help_text="输入主播的直播间网址")
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, help_text="输入主播的基本工资(单场/元)",default = 5000)
    commission = models.DecimalField(max_digits=5, decimal_places=2,help_text="输入近三十天主播的佣金率(%)",default = 5)
    linked_Time = models.ManyToManyField(LivingTime,help_text="选择该主播的直播时间段(UTC8+)")
    linked_Commodity = models.ManyToManyField('Commodity', related_name='anchors',help_text="选择与该主播关联的商品")
    linked_Category = models.ManyToManyField('Category', through='AnchorCategoryLink', help_text="选择该主播历史热销商品类型")
    CTR= models.DecimalField(max_digits=5, decimal_places=2, default=10.00, help_text="历史平均穿透率")
    RPM = models.DecimalField(max_digits=10, decimal_places=2,default=1000,help_text="近期主播分均产出")
    UV_func = models.CharField(max_length=200,null=True, blank=True,help_text="输出近三十天UV拟合函数，格式为a*x^3+b*x^2+c*x+0.52")
    @property
    def gender(self):
        # 尝试返回与此Anchor实例关联的百分比属性
        # 如果没有找到，返回None或者默认值
        if hasattr(self, 'Anchor_gender'):
            return {
                '男': self.Anchor_gender.Male,
                '女': self.Anchor_gender.Female,
            }
        else:
            return {
                '男': 50,
                '女': 50,
                  }      # 返回一个包含默认值的字典
    @property
    def Cost(self):
        # 尝试返回与此Anchor实例关联的百分比属性
        # 如果没有找到，返回None或者默认值
        if hasattr(self, 'Cost_Level'):
            return {
                '[0,25)': self.Cost_Level.mini,
                '[25,50)': self.Cost_Level.low,
                '[50,100)': self.Cost_Level.medi,
                '[100,200)': self.Cost_Level.high,
                '[200,500)': self.Cost_Level.super,
                '500+': self.Cost_Level.maxi,
            }
        else:
            return {
                '[0,25)': 20,
                '[25,50)': 20,
                '[50,100)': 20,
                '[100,200)': 20,
                '[200,500)': 20,
                '500+': 0,
            }            #返回一个包含默认值的字典
    @property
    def Age(self):
        # 尝试返回与此Anchor实例关联的百分比属性
        # 如果没有找到，返回None或者默认值
        if hasattr(self, 'Anchor_Age_Level'):
            return {
                '[18,23)': self.Anchor_Age_Level.mini,
                '[24,30)': self.Anchor_Age_Level.low,
                '[31,40)': self.Anchor_Age_Level.medi,
                '[41,50)': self.Anchor_Age_Level.high,
                '50+': self.Anchor_Age_Level.maxi,
            }
        else:
            return {
                '[18,23)': 20,
                '[24,30)': 20,
                '[31,40)': 20,
                '[41,50)': 20,
                '50+': 20,
            }            #返回一个包含默认值的字典
    class Meta:
        ordering = ['name']  # 按姓名排序
        permissions = (("can_renew_anchor","主播待遇与信息修正"),)
    def display_Commodity(self):
        """为商品创建一个字符串。这是在管理界面中显示所必需的。"""
        return ', '.join([Commodity.name for Commodity in self.linked_Commodity.all()])  # 显示商品
    def display_Time(self):
        """为直播时间创建一个字符串。这是在管理界面中显示所必需的。"""
        return ', '.join([f"{Time.start_time} - {Time.finally_time}" for Time in self.linked_Time.all()])  # 显示直播时间段
    display_Commodity.short_description = '关联商品'  # 在管理界面中显示的列名
    def display_Category(self):
        """为热销商品类型创建一个字符串。这是在管理界面中显示所必需的。"""
        return ', '.join([f"{Category.category.name}-{Category.sales_percentage}" for Category in self.anchorcategorylink_set.all()])  # 显示商品    
    def get_absolute_url(self):
        """返回访问特定主播的 URL。"""
        return reverse('anchor-detail', args=[str(self.id)])  # 返回主播详情页的 URL

    def __str__(self):
        """用于表示模型对象的字符串（在管理界面等地方）。"""
        return self.name  # 返回主播名称  
    
from django.core.exceptions import ValidationError    

    
    
class AvgCostLevel(models.Model):
    """表示客单量水平占比。"""
    anchor = models.OneToOneField(Anchor, on_delete=models.CASCADE, related_name='Cost_Level')
    mini = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    low = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    medi = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    high = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    super = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    maxi = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    def clean(self):
        # 确保总和为100%
        total_percentage = self.mini + self.low + self.medi + self.high + self.maxi+ self.super
        if total_percentage != 100.00:
            raise ValidationError("总和必须为100%。当前总和为: {}".format(total_percentage))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)   


        
class Gendered(models.Model):
    """表示性别百分比。"""
    anchor = models.OneToOneField(Anchor, on_delete=models.CASCADE, related_name='Anchor_gender')
    Male = models.DecimalField(max_digits=5, decimal_places=2, default=50.00)
    Female = models.DecimalField(max_digits=5, decimal_places=2, default=50.00)
    def clean(self):
        # 确保的总和为100%
        total_percentage = self.Male + self.Female 
        if total_percentage != 100:
            raise ValidationError("总和必须为100%。当前总和为: {}".format(total_percentage))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)   


class AnchorAge(models.Model): 
    """表示主播年龄百分比。"""    
    anchor = models.OneToOneField(Anchor, on_delete=models.CASCADE, related_name='Anchor_Age_Level')
    mini = models.DecimalField(max_digits=5, decimal_places=2,default=20)
    low = models.DecimalField(max_digits=5, decimal_places=2,default=20)
    medi = models.DecimalField(max_digits=5, decimal_places=2,default=20)
    high = models.DecimalField(max_digits=5, decimal_places=2,default=20)
    maxi = models.DecimalField(max_digits=5, decimal_places=2,default=20)
    def clean(self):
        # 确保总和为100%
        total_percentage = self.mini + self.low + self.medi + self.high + self.maxi
        if total_percentage != 100:
            raise ValidationError("总和必须为100%。当前总和为: {}".format(total_percentage))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)      
             
           
class SalesRecord(models.Model):
    """表示某场直播的商品的特定副本的模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="整场直播内商品的唯一ID")  # 唯一 ID
    sale_date = models.DateField(help_text="输入直播日期")
    soldon_date = models.TimeField(help_text="输入上架时间",null=True)
    soldout_date = models.TimeField(help_text="输入下架时间",null=True)
    anchor = models.ForeignKey('Anchor', on_delete=models.CASCADE)
    commodity = models.ForeignKey('Commodity', on_delete=models.CASCADE)
    category = models.CharField(max_length=200, editable=False)
    price = models.FloatField(null=True, editable=False)
    count = models.FloatField(null=True,help_text="输入折扣率%",default = 0)
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2,help_text="输入销售量")
    extra_commission = models.DecimalField(max_digits=10, decimal_places=2,help_text="输入坑位费")
    total_amount = models.DecimalField('销售额',max_digits=10, decimal_places=2, help_text="销售额", editable=False,default = 0)
    total_income = models.DecimalField('订单收入', max_digits=10, decimal_places=2,help_text="订单收入", editable=False)
    imprint = models.CharField(null=True, blank=True,max_length=200)  # 印记
    @property
    def is_count(self):
        return bool(self.count and self.count >0 and self.count <100)
    LOAN_STATUS = (
        ('o','原价'),
        ('d', '折扣'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='o',
        help_text='商品折扣与否', 
        editable=False
    )
    def save(self, *args, **kwargs):
        # 在保存销售信息前计算总收入收益
        if self.commodity:
            self.category = self.commodity.category.name
            self.price = self.commodity.price
        if self.is_count:
            self.status='d'
            self.price = self.commodity.price*(1-self.count*0.01)
        else:
            self.price_now = self.commodity.price
        if self.commodity:  # 确保 commodity 已经关联
            self.total_amount =self.commodity.price * self.sale_amount            
            self.total_income = (self.commodity.price * self.commodity.commission_rate*0.01 * self.sale_amount) + self.extra_commission
        super(SalesRecord, self).save(*args, **kwargs)

    class Meta:
        ordering = ['sale_date']  # 按销售日期排序
        permissions = (("can_mark_returned", "标记商品打折"),)  # 设置用户权限

    def get_absolute_url(self):
        """返回访问特定销售记录的 URL。"""
        return reverse('salesrecord-detail', args=[str(self.id)])  # 返回销售记录详情页的 URL

    def __str__(self):
        return f"{self.sale_date} - {self.anchor.name if self.anchor else 'Unknown'}- {self.category if self.category else 'Unknown'} - {self.commodity.name if self.commodity else 'Unknown'}"
