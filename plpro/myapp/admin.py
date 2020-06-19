from django.contrib import admin
from myapp.models import Table_Six,Notice,Table_Five
# Register your models here.
# 设置数据表的展示

# 第六次数据表格后台设置
class TableAdmin_Six(admin.ModelAdmin):
    list_display = ('volume', 'title','total') # 设置展示哪些内容

    search_fields = ('title',) #设置以哪个字段为搜索内容

    # 设置增删改查的页面
    fieldsets = [
        ('卷数信息', {'fields': ['volume_num','volume']}),
        ('表格信息', {'fields': ['title','mc','level_1','level_2']}),
        ('数值', {'fields': ['total']}),
    ]

# 第五次数据表格后台设置
class TableAdmin_Five(admin.ModelAdmin):
    list_display = ('volume', 'title','total') # 设置展示哪些内容

    search_fields = ('title',) #设置以哪个字段为搜索内容

    # 设置增删改查的页面
    fieldsets = [
        ('卷数信息', {'fields': ['volume_num', 'volume']}),
        ('表格信息', {'fields': ['title', 'mc', 'level_1', 'level_2']}),
        ('数值', {'fields': ['total']}),
    ]


# 公告后台设置
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['notice_title','notice_time'] # 设置展示哪些内容

    search_fields = ('notice_title',) #设置以哪个字段为搜索内容
    # 设置增删改查的页面
    fieldsets = [
        ('公告标题', {'fields': ['notice_title']}),
        ('发布时间', {'fields': ['notice_time']}),
        ('发布内容', {'fields': ['content']}),
    ]

admin.site.register(Table_Six,TableAdmin_Six)   #将表格模型与后台模型一起注册
admin.site.register(Table_Five,TableAdmin_Five)   #将表格模型与后台模型一起注册
admin.site.register(Notice,NoticeAdmin) #将公告模型与后台模型一起注册

admin.site.site_header = '人口数据分析系统' #设置后台的标题
admin.site.site_title = '人口数据分析系统'  #设置登录后台时的标题


