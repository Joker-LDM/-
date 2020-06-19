from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Table_Six,Notice,Table_Five
import json

# 主页函数
def index(request):
    # 查询数据库中所有的卷数，并且按照捐数排序去重
    volume = Table_Six.objects.values('volume').order_by('volume_num').distinct()
    # 将查询的数据集转化为列表
    set_volume = json.dumps(list(volume))
    get_volume = json.loads(set_volume)

    # 设置一个空列表，用来存储卷数及卷数下的表名
    list_volume = []
    # 循环卷数
    for v in get_volume:
        dict_volume = {}
        # 获取每个卷数下面的表名，并且按照标题大小进行排序，然后去重
        table = Table_Six.objects.filter(volume=v['volume']).values('title').order_by('title').distinct()
        # 构建字典
        dict_volume['volume'] = v['volume']
        dict_volume['title'] = table
        # 存入列表
        list_volume.append(dict_volume)

    # locals()代表将当前所有的变量传过去，是一种简写的方法
    return render(request, "index.html",locals())


# 图表详情页函数
def details(request,name):
    # 获取选择的表名
    table_name = name
    # 在数据库查询title字段中符合的表名，获取level1、level2的值，并进行去重
    table = Table_Six.objects.filter(title=table_name).values('level_1','level_2').distinct()
    # 将查询的数据集转化为列表
    set_table = json.dumps(list(table))
    get_table = json.loads(set_table)

    # 存储选项
    option_list = []
    # 循环获取字典中一级菜单与二级菜单数据
    for t in get_table:
        level_1 = t['level_1']
        level_2 = t['level_2']
        # 如果二级菜单不为空，那么拼接一级+二级菜单
        if level_2:
            all_level = level_1+ '-' + level_2
        # 否则选项为一级菜单
        else:
            all_level = level_1
        # 存入列表
        option_list.append(all_level)

    # 在数据库中查询当前表的mc列，并且进行去重
    mc_num = Table_Six.objects.filter(title=table_name).values('mc').distinct()
    # 将查询的数据集转化为列表
    set_mc = json.dumps(list(mc_num))
    get_mc = json.loads(set_mc)

    # 存储每个mc列的列名+当前列的数据
    mc_list_six = []
    # 循环的去查询表格中每个mcl列的数值，并且构成字典
    for m in get_mc:
        data_six = '第六次人口普查数据'
        mc_dict = {}
        m1 = Table_Six.objects.filter(Q(title=table_name) & Q(mc=m['mc'])).values('total')
        mc_dict['x_axit'] = m['mc']
        mc_dict['y_axit'] = m1
        mc_list_six.append(mc_dict)


    # 存储每个mc列的列名+当前列的数据
    mc_list_five = []
    # 循环的去查询第五次普查数据表中表格中每个mcl列的数值，并且构成字典
    for m in get_mc:
        data_five = '第五次人口普查数据'
        mc_dict_five = {}
        m1 = Table_Five.objects.filter(Q(title=table_name) & Q(mc=m['mc'])).values('total')
        mc_dict_five['x_axit'] = m['mc']
        mc_dict_five['y_axit'] = m1
        mc_list_five.append(mc_dict_five)


    # 查询当前表格的一级菜单+二级菜单，并且进行去重
    menus_six = Table_Six.objects.filter(title=table_name).values_list('level_1','level_2').distinct()
    # 将查询的数据集转化为列表
    set_menus = json.dumps(list(menus_six))
    get_menus = json.loads(set_menus)
    # 存储表格菜单
    menus_list = []
    #循环处理一级➕二级菜单
    for menu in get_menus:
        m_l = []
        # 处理每个字段中的空格
        for m in menu:
            # 将每个字段中的空格处理
            if m:
                c = m.replace(' ','')
                m_l.append(c)
        #用横杠链接一级+二级菜单
        menus_list.append('-'.join(m_l))
    return render(request,'details.html',locals())


# 图表可视化函数
def visualization(request):
    if request.method == 'POST':
        table = request.POST.get('table_name')  #当前表名
        option = request.POST.get('option') #数据选项
        vis = request.POST.get('visualization') #可视化选项
        # 判断选项是否有两集菜单
        if '-' in option:
            options = option.split('-')
            level_1 = options[0]
            level_2 = options[1]
            # 如果有二级菜单，那么分隔以后查询符合条件的表名+一级菜单+二级菜单
            date_six = Table_Six.objects.filter(Q(title=table) & Q(level_1=level_1) & Q(level_2=level_2))
            date_five = Table_Five.objects.filter(Q(title=table) & Q(level_1=level_1) & Q(level_2=level_2))
        else:
            # 否则直接查询符合条件的表名+一级菜单
            date_six = Table_Six.objects.filter(Q(title=table) & Q(level_1=option))
            date_five = Table_Five.objects.filter(Q(title=table) & Q(level_1=option))
        # 获取值与mc字段，用来生成图表中的x轴+y轴

        x_axis_dict = date_six.values('mc')
        six_total_dict = date_six.values('total')
        five_total_dict = date_five.values('total')

        # 将mc字段转为字典
        set_x_axis = json.dumps(list(x_axis_dict))
        get_x_axis = json.loads(set_x_axis)

        six_set_total = json.dumps(list(six_total_dict))
        six_get_total = json.loads(six_set_total)

        five_set_total = json.dumps(list(five_total_dict))
        five_get_total = json.loads(five_set_total)

        mc_list = []    #mc列表
        y_list_six = [] #第六次数据列表
        y_list_five = []    #第五次数据列表

        # 图表的x列，循环获取mc及第五次、第六次的字典的值，分别存入上面三个列表
        for item in get_x_axis: mc_list.append(item['mc'])
        for item in six_get_total: y_list_six.append(item['total'])
        for item in five_get_total: y_list_five.append(item['total'])

        # 折线图数据列表
        lie_five_data = []
        lie_six_data = []

        # 象形图数据列表
        pic_five_data = []
        pic_six_data = []

        # 饼图数据列表
        pie_six_data = []
        pie_five_data = []

        if vis == 'bar':
            bar = 1
        elif vis == 'lie':
            lie = 1
            # 循环获取mc列表与第六次数据列表，组成键值对列表。供给折线图的第六次数据用
            for six_data,mc in zip(y_list_six,mc_list):
                lie_six_list = []
                lie_six_list.append(mc)
                lie_six_list.append(six_data)
                lie_six_data.append(lie_six_list)
            # 判断第五次数据是否存在，然后获取mc列表与第五次数据列表，组成键值对列表。供给折线图的第五次数据用
            if y_list_five:
                for five_data, mc in zip(y_list_five,mc_list):
                    lie_five_list = []
                    lie_five_list.append(mc)
                    lie_five_list.append(five_data)
                    lie_five_data.append(lie_five_list)
        elif vis == 'pic':
            # 将mc列表反转，以适应x列的排序
            mc_list = list(reversed(mc_list))
            pic = 1
            # 将第六次的数据转换成浮点数，并且进行排序
            y_list_six = list(map(float, y_list_six))
            y_list_six = sorted(y_list_six, reverse=False)
            for six_data in y_list_six:
                six_dict = {}
                six_dict['value'] = six_data
                pic_six_data.append(six_dict)
            if y_list_five:
                # 将第五次的数据转换成浮点数，并且进行排序
                y_list_five = list(map(float, y_list_five))
                y_list_five = sorted(y_list_five, reverse=False)
                for five_data in y_list_five:
                    five_dict = {}
                    five_dict['value'] = five_data
                    pic_five_data.append(five_dict)
        elif vis == 'pie':
            pie = 1
            for six_data,mc in zip(y_list_six,mc_list):
                six_dict = {}
                six_dict['name'] = mc
                six_dict['value'] = six_data
                pie_six_data.append(six_dict)
            if y_list_five:
                for five_data, mc in zip(y_list_five, mc_list):
                    five_dict = {}
                    five_dict['name'] = mc
                    five_dict['value'] = five_data
                    pie_five_data.append(five_dict)

        # 如果第五次的数据存在，那么计算差值
        if y_list_five:
            # 将第六次与第五次的值都转化为浮点数
            six_value_list = list(map(float, y_list_six))
            five_value_list = list(map(float, y_list_five))

            subtract_list = []
            # 循环获取主列，第六次、第五次的数据
            for m, s, f in zip(mc_list, six_value_list, five_value_list):
                # 创建一个字典，保存每个mc主列与差值
                subtract_dict = {}
                subtract_dict['mc'] = m
                subtract_dict['value'] = '{}%'.format(round((s-f)/s,2)) #计算第六次与第五次的差值
                subtract_list.append(subtract_dict) #存入列表

    return render(request,'visualization.html',locals())

# 公告函数
def notice(request):
    # 获取所有公告
    content = Notice.objects.all()
    return render(request,'notice.html',locals())


