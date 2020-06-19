from django.urls import path
from myapp import views
app_name = 'myapp'



urlpatterns = [
    path('',views.index,name = 'index'),
    path('details/<str:name>',views.details,name='details'),  #图表详情页
    path('visualization/',views.visualization,name='visualization'),  #图表可视化页
    path('notice/',views.notice,name='notice')  #公告
]