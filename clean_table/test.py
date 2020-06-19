import xlrd
import csv
import os


csvFile = open("people_info_five.csv", 'w', newline='')
writer = csv.writer(csvFile)

#读取data文件夹下面的所有文件夹与文件名称，返回给read_excel
def func():
    file_list = []
    fileDir = './data_five' # 以分隔符连接路径名
    file_dict = {}
    for root, dirs, files in os.walk(fileDir):
        if root.split('/')[-1] != 'data_five':
            valume = root.split('/')[-1]
            file_dict[valume] = files
    for f in file_dict:
        for file in file_dict[f]:
            f_list = []
            if 'DS_Store' not in file:
                f_list.extend([file.split('-')[0],f,file])
                file_list.append(f_list)
    return file_list

# 读取数据并且整理，返回整理好的列表
def read_excel(valume_num,valume,file_path):
    # 去除表格的后缀，提取表格的名字
    file_name = file_path.replace('.xls','')
    # 获取数据
    data = xlrd.open_workbook('./data_five/' + valume +'/' + file_path)
    # 获取sheet
    table = data.sheet_by_name('Sheet1')
    # 获取总行数
    nrows = table.nrows  # 包括标题
    # 获取总列数
    ncols = table.ncols
    # 计算出合并的单元格有哪些
    colspan = {}
    if table.merged_cells:
        for item in table.merged_cells:
            for row in range(item[0], item[1]):
                for col in range(item[2], item[3]):
                    # 合并单元格的首格是有值的，所以在这里进行了去重
                    if (row, col) != (item[0], item[2]):
                        colspan.update({(row, col): (item[0], item[2])})

    # 读取每列数据
    mc = []
    all_l = []
    for j in range(ncols):
        col = []

        for i in range(0, nrows):
            # 假如碰见合并的单元格坐标，取合并的首格的值即可
            if colspan.get((i, j)):
                col.append(table.cell_value(*colspan.get((i, j))))
            else:
                col.append(table.cell_value(i, j))
        if j == 0:
            mc = col
        else:
            all_l.append(col)
    # 去除主列前两个数据
    del mc[0:2]

    level1_list = []
    new_date = []
    totol_list = []
    for i in all_l:
        try:
            i[0] = i[0].replace(' ','')
            # 如果等级一有值的话，那么保存等级一的值到level1列表
            if i[0]:
                level1_list.append(i[0])
            # 如果等级一没有值，说明是合并单元，获取level1列表的最后一个值
            elif i[0] == '':
                i[0] = level1_list[-1]
        except:
            print('不可解析-----',file_name,i)
        new_date.append(i[0:2])
        totol_list.append(i[-len(mc):])

    data_list = []
    for n1,n2 in zip(new_date,totol_list):
        for n3,n4 in zip(n2,mc):
            d_list = []
            d_list.append(valume_num)
            d_list.append(valume)
            d_list.append(file_name)
            d_list.append(n4.replace(' ',''))
            d_list.append(n1[0].replace(' ',''))
            d_list.append(n1[1].replace(' ',''))
            d_list.append(n3)
            data_list.append(d_list)

    return data_list

# 接收read_excel整理好的列表，循环插入csv表格
def data_writer(date_list):
    for date in date_list:
        valume_num = date[0]
        valume = date[1]
        title = date[2]
        mc = date[3]
        lavel_1 = date[4].replace('-','.')
        lavel_2 = date[5].replace('-','.')
        total = date[6]
        writer.writerow((valume_num,valume,title,mc,lavel_1,lavel_2,total))


if __name__ == "__main__":

    count = 0
    for files in func():
        data_writer(read_excel(files[0],files[1],files[2]))
        print('{}数据写入成功'.format(files[2]))
        count += 1
    print('共写入{}张表格'.format(count))




