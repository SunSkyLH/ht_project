import csv
import re
import numpy as np


def is_number(num):
    """判断num是否为数字形式"""
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


def chuli_data(filename, column):
    """数据预处理，返回数据有效位、异常检测位、起飞零点之后数据、起飞零点之后时间四个数组"""
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_row = next(reader)

        ifnull = []  # 数据有效位:有效数据为1,无效为0
        iferror = []  # 异常检测位:初始默认全部为0
        updata = []  # 记录起飞零点后的数据
        newtime = []  # 记录起飞零点后的时间
        temp = 0
        for i in reader:
            # 根据测试数据第一列判断是否为起飞零点之后数据
            if is_number(i[0]) and float(i[0]) >= 0.0:
                # 若为起飞零点之后的数据,判断要处理的维数列，并更新四个数位
                if is_number(i[column]):
                    temp = i[column]
                    updata.append(float(i[column]))
                    newtime.append(float(i[0]))
                    ifnull.append(1)
                    iferror.append(0)
                # 若不是数字形式时,数据预处理
                # 将数据有效位设置为0,再利用上一行数据进行填充
                else:
                    ifnull.append(0)
                    i[column] = temp
                    updata.append(float(i[column]))
            else:
                continue
        #print(ifnull)
        #print(iferror)

        #print(np.array(newtime))
        #print(updata)
    return updata,newtime,ifnull,iferror


#chuli_data('180102d-2-8s.csv', 9)
