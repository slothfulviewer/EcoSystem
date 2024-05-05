from django.urls import path
from catalog import views

urlpatterns = [
    path('indexs', views.index, name='indexs'),
    path('Commodities/', views.CommodityListView.as_view(), name='Commodities'),
    path('Commodity/<int:pk>', views.CommodityDetailView.as_view(), name='Commodity-detail'),
    path('anchors/', views.AnchorListView.as_view(), name='anchors'),
    path('anchors/<int:pk>', views.AnchorDetailView.as_view(), name='anchor-detail'),
    path('SalesRecords/', views.SaleListView.as_view(), name='SalesRecords'),
    path('SalesRecord/<str:pk>', views.SaleDetailView.as_view(), name='salesrecord-detail'),
    path('Categories/', views.CategoryListView.as_view(), name='Categories'),
    path('Category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('api/sales_records/', views.SalesRecordList.as_view(), name='sales_records_api'),
]
urlpatterns += [
    path('anchors/create/', views.AuthorCreate.as_view(), name='anchor_create'),
    path('anchors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='anchor_update'),
    path('anchors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='anchor_delete'),
]
urlpatterns += [ 
    path('anchors/<int:pk>/strategy/', views.AnchorStrategyView.as_view(), name='anchor-strategy'),
]