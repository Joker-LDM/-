from django.db import models
from tinymce.models import HTMLField  # 使用富文本编辑框要在settings文件中安装
# Create your models here.



# 第六次数据表格模型
class Table_Six(models.Model):
    id = models.AutoField(primary_key=True)
    volume_num = models.CharField(max_length=128, verbose_name='卷数', blank=False)
    volume = models.CharField(max_length=128,verbose_name='卷名',blank=False)
    title = models.CharField(max_length=128,verbose_name='表名',blank=False)
    mc = models.CharField(max_length=128,verbose_name='图表X列',blank=False)
    level_1 = models.CharField(max_length=128,verbose_name='一级',blank=False)
    level_2 = models.CharField(max_length=128,verbose_name='二级',blank=False)
    total = models.CharField(max_length=128,verbose_name='数值',blank=False)

    class Meta:
        verbose_name_plural = '第六次人口普查' #设置这个模型在后台的名字

# 第五次数据表格模型
class Table_Five(models.Model):
    id = models.AutoField(primary_key=True)
    volume_num = models.CharField(max_length=128, verbose_name='卷数', blank=False)
    volume = models.CharField(max_length=128,verbose_name='卷名',blank=False)
    title = models.CharField(max_length=128,verbose_name='表名',blank=False)
    mc = models.CharField(max_length=128,verbose_name='图表X列',blank=False)
    level_1 = models.CharField(max_length=128,verbose_name='一级',blank=False)
    level_2 = models.CharField(max_length=128,verbose_name='二级',blank=False)
    total = models.CharField(max_length=128,verbose_name='数值',blank=False)

    class Meta:
        verbose_name_plural = '第五次人口普查' #设置这个模型在后台的名字


# 公告模型
class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    notice_title = models.CharField(max_length=128,verbose_name="公告标题",blank=False)
    notice_time = models.DateField(verbose_name="发布时间", blank=False)
    content = HTMLField(max_length=10000, verbose_name="公告内容")

    class Meta:
        verbose_name_plural = '公告'  # 设置这个模型在后台的名字


