from django.shortcuts import render

# Create your views here.
from .models import Category, Commodity, Anchor, SalesRecord
from django.http import JsonResponse
from .models import SalesRecord
from django.core.serializers import serialize
from django.views.generic.base import TemplateView
def sales_record_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    sales_records = SalesRecord.objects.all()

    if start_date and end_date:
        sales_records = sales_records.filter(sale_date__range=[start_date, end_date])

    data = serialize('json', sales_records)
    return JsonResponse(data, safe=False)

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_Category=[a.name for a in Category.objects.all()]
    num_Commodity=Commodity.objects.all().count()
    num_SalesRecord=SalesRecord.objects.all().count()
    num_SalesRecord_discount=SalesRecord.objects.filter(status__exact='d').count()
    num_anchors=Anchor.objects.count()  # The 'all()' is implied by default.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'在职主播数':num_anchors,'商品类型':num_Category,'商品数':num_Commodity,'折扣商品数':num_SalesRecord_discount,
        '历史直播订单数':num_SalesRecord,'访问量':num_visits}, # num_visits appended
    )

from django.views import generic
from django.http import JsonResponse

class CommodityListView(generic.ListView):
    model = Commodity
    paginate_by = 10
    context_object_name = 'Commodity_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='test')[:5] # Get 5 books containing the title war
    template_name = 'Commodities/On_sale_Commodity_list.html'  # Specify your own template name/location
    #将数据整合成JSON形式传输


class CommodityDetailView(generic.DetailView):
    model = Commodity


class AnchorListView(generic.ListView):
    model = Anchor
    context_object_name = 'anchor_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='test')[:5] # Get 5 books containing the title war
    #template_name = 'anchors/CompanyAnchor_list.html'  # Specify your own template name/location

class AnchorDetailView(generic.DetailView):
    model = Anchor
    
from pulp import LpProblem, LpMaximize, LpVariable, lpSum,LpStatus
import datetime,re
from numpy import polyval
from math import sqrt
from decimal import Decimal, getcontext,ROUND_HALF_UP
class AnchorStrategyView(TemplateView):
    template_name = 'catalog/strategy_view.html' 
    getcontext().prec = 4
    getcontext().rounding = ROUND_HALF_UP
    def parse_uv_function(self, uv_function_str):
        # 解析多项式，提取系数和对应的次幂
        terms = re.findall(r"([+-]?\d*\.?\d*)\s*\*?\s*x\^?(\d+)?", uv_function_str)
        coeffs = {}
        
        # 遍历所有匹配的项
        for term in terms:
            coef, power = term
            if coef == '' or coef == '+':
                coef = '1.0'  # 处理省略系数为1的情况
            elif coef == '-':
                coef = '-1.0'  # 处理省略系数为-1的情况
            coef = float(coef)
            
            if power == '':
                power = '1'  # 处理省略次幂的情况 (线性项)
            power = int(power) if power else 0  # 常数项的次幂为0
            
            coeffs[power] = coef

        # 确保从最高次幂到0次幂都有系数，缺失的系数用0填充
        max_power = max(coeffs.keys()) if coeffs else 0
        sorted_coeffs = [coeffs.get(power, 0.0) for power in range(max_power, -1, -1)]
        
        print(sorted_coeffs)  # 打印系数列表
        return sorted_coeffs

    def calculate_uv_values(self, anchor, time_point):
        # 调用主播UV函数
        getcontext().prec = 4
        coeffs = self.parse_uv_function(anchor.UV_func)
        # 计算每个时间点的UV值
        uv_value =  Decimal(str(polyval(coeffs, time_point)*10000))
        return uv_value


    def calculate_similarity(self, anchor, commodity):
        # 假设：anchor.gender 返回 {'男': percentage, '女': percentage}
        # 假设：commodity.gender 返回 {'男': percentage, '女': percentage}
        # 同理对于年龄 Age
        gender_distance = sqrt(sum((anchor.gender[g] - commodity.gender[g])**2 for g in ['男', '女']))
        age_distance = sqrt(sum((anchor.Age[a] - commodity.Age[a])**2 for a in commodity.Age.keys()))
        # 返回相似度，这里简化为 1 / (1 + 距离)
        return  1/(1+gender_distance+age_distance)

    def get_commodity_profit(self, anchor, commodity, uv_value):
        getcontext().prec = 4
        # 计算特定UV值下商品的预期利润
        similarity = self.calculate_similarity(anchor, commodity)
        if uv_value<=0:
            uv_value =Decimal('0')
        expected_sales = uv_value* Decimal(str((commodity.history_sell / commodity.history_amount))) * anchor.CTR*Decimal('0.01')
        k =10
        if 0<commodity.price and commodity.price<=25:
            profit_per_commodity = expected_sales * Decimal(str(similarity)) *k*anchor.RPM*Decimal(anchor.Cost["[0,25)"])
        elif 25<commodity.price and commodity.price<=50:
            profit_per_commodity = expected_sales * Decimal(str(similarity)) *k*anchor.RPM*Decimal(anchor.Cost["[25,50)"])
            
        elif 50<commodity.price and commodity.price<=100:
            profit_per_commodity = expected_sales * Decimal(str(similarity)) *k*anchor.RPM*Decimal(anchor.Cost["[50,100)"])
        elif 100<commodity.price and commodity.price<=200:
            profit_per_commodity = expected_sales * Decimal(str(similarity)) *k*anchor.RPM*Decimal(anchor.Cost["[100,200)"])
        elif 200<commodity.price and commodity.price<=500:
            profit_per_commodity = expected_sales * Decimal(str(similarity)) *k*anchor.RPM*Decimal(anchor.Cost["[200,500)"])
        elif  commodity.price>500:
            profit_per_commodity = expected_sales * Decimal(str(similarity)) *k*anchor.RPM*Decimal(anchor.Cost["500+"])

        anchor_profit = profit_per_commodity * commodity.commission_rate*Decimal('0.01')*anchor.commission*Decimal('0.01')
        # 计算总利润
        total_profit = profit_per_commodity *commodity.commission_rate*Decimal('0.01')
        pre = [profit_per_commodity,total_profit,anchor_profit]
        return pre#预期销售额，预期收入，预期主播收入

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anchor_id = kwargs.get('pk')
        anchor = Anchor.objects.get(pk=anchor_id)
        commodities = Commodity.objects.all()
        time_points = ['0:10', '0:20', '0:30', '0:40', '0:50', 
                       '1:00', '1:10', '1:20', '1:30', '1:40', '1:50',
                       '2:00', '2:10', '2:20', '2:30', '2:40', '2:50',
                       '3:00', '3:10', '3:20', '3:30', '3:40', '3:50', '4:00', '4:10']
        time_values = [int(hm.split(':')[0]) * 60 + int(hm.split(':')[1]) for hm in time_points]
        # 创建问题实例，这里以最大化为例
        problem = LpProblem("Anchor_Maximize_Revenue", LpMaximize)
        n =24
        # 决策变量：商品i在时间段j是否被选中
        x_vars = LpVariable.dicts("X", [(i.id, j) for i in commodities for j in range(len(time_points))], cat='Binary')

        # 目标函数：最大化总利润
        profit_expr = []
        for j, time_value in enumerate(time_values):
            uv_value = self.calculate_uv_values(anchor, time_value)
            for commodity in commodities:
                profit = self.get_commodity_profit(anchor,commodity, uv_value)
                profit_expr.append(x_vars[commodity.id, j] * profit[1])
        problem += lpSum(profit_expr)

        # 添加约束条件
        # 约束条件1：每件商品在一个时间段内只能被销售一次
        for i in commodities:
            problem += lpSum(x_vars[i.id, j] for j in range(len(time_points))) <= 1

        # 约束条件2：每个时间段只能销售一件商品
        for j in range(len(time_points)):
            problem += lpSum(x_vars[i.id, j] for i in commodities) <= 1

        # 约束条件3：销售的总商品数为n
        problem += lpSum(x_vars[i.id, j] for i in commodities for j in range(len(time_points))) == n

        # 求解问题
        status = problem.solve()
        if LpStatus[status] == 'Optimal':

            results = []
            for j, time_value in enumerate(time_values):
                for commodity in commodities:
                    if x_vars[commodity.id, j].varValue > 0:  # 商品在该时间段被选中
                        uv_value = self.calculate_uv_values(anchor, time_value)
                        profit_data = self.get_commodity_profit(anchor, commodity, uv_value)
                        results.append({
                            'time_slot': time_points[j],
                            'product_name': commodity.name,
                            'product_category': commodity.category,
                            'product_price': commodity.price,
                            'expected_sales': profit_data[0],
                            'expected_revenue': profit_data[1],
                            'expected_anchor_income': profit_data[2]
                        })

            context['strategy_results'] = results
            context['time_slots'] = [
            f"{hour}:{minute:02d} - {hour}:{minute+10:02d}"
            for hour in range(5) 
            for minute in range(0, 60, 10)
        ]
            return context
        else:
            results_d = ['0:10-0:20','A','B','24.3','500','1234','412']
            context['strategy_results'] = results_d
            context['time_slots'] = [
            f"{hour}:{minute:02d} - {hour}:{minute+10:02d}"
            for hour in range(5) 
            for minute in range(0, 60, 10)
        ]
            return context
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_date

class SaleListView(generic.ListView):
    model = SalesRecord

    context_object_name = 'SalesRecord_list'
    template_name = 'SalesRecords/SalesRecord_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取主播列表，去重并按名称排序
        all_anchors = SalesRecord.objects.all().values_list('anchor__name', flat=True)
        context['unique_anchors'] = sorted(set(all_anchors))
        # 获取分类列表，去重并排序
        all_categories = SalesRecord.objects.all().values_list('category', flat=True)
        context['unique_categories'] = sorted(set(all_categories))
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(sale_date__gte=start_date)
        
        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(sale_date__lte=end_date)

        return queryset

class SaleDetailView(generic.DetailView):
    model = SalesRecord
    
class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'Category_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='test')[:5] # Get 5 books containing the title war
    template_name = 'Categories/Category_list.html'  # Specify your own template name/location

    
class CategoryDetailView(generic.DetailView):
    model = Category # your own name for the list as a template variable
    

from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SalesRecord,Anchor
from .serializers import SalesRecordSerializer

class SalesRecordList(APIView):
    """
    List all SalesRecords, or create a new SalesRecord, with filtering options.
    """
    def get(self, request, format=None):
        # 获取查询参数
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        anchor_name = request.query_params.get('anchorname')
        category = request.query_params.get('category')

        # 基于查询参数筛选SalesRecord对象
        sales_records = SalesRecord.objects.all()

        if start_date:
            start_date = parse_date(start_date)
            sales_records = sales_records.filter(sale_date__gte=start_date)
        
        if end_date:
            end_date = parse_date(end_date)
            sales_records = sales_records.filter(sale_date__lte=end_date)

        if anchor_name:
            anchors = Anchor.objects.filter(name__icontains=anchor_name)  # 使用icontains来做不区分大小写的包含查询
            sales_records = sales_records.filter(anchor__in=anchors)

        if category:
            sales_records = sales_records.filter(category=category)
        # 序列化并返回筛选后的销售记录
        serializer = SalesRecordSerializer(sales_records, many=True)
        return Response(serializer.data)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from django.contrib.auth.mixins import PermissionRequiredMixin

class AuthorCreate(PermissionRequiredMixin,CreateView):
    model = Anchor
    permission_required = 'catalog.can_renew_anchor'
    fields = '__all__'
    initial={'hire_date':'2024/04/30',}

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.can_renew_anchor'
    model = Anchor
    fields = ['name','amount','live_house','base_salary','commission','linked_Time','linked_Category']
class AuthorDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.can_renew_anchor'
    model = Anchor
    success_url = reverse_lazy('Anchors')

