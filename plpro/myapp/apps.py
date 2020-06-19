from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'
    verbose_name = '数据管理'   #设置此应用在admin后台的站点名称
