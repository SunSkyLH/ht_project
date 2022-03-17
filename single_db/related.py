import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import pymssql
import time

filepath = ""
def excel_one_line_to_list(i,tabel_name):
    connect = pymssql.connect('127.0.0.1', 'wxx', '12345678', 'mydbtest')  # 建立连接
    if connect:
        print("连接成功!")
    time_start = time.time()
    result = []
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    # sql = "select line8S0%d from wxx_data_test%d"%(i,i)
    s1 = "select line" + tabel_name + "%d " % i
    s2 = "from model_data_" + tabel_name + "_%d" % i
    sql = s1 + s2
    cursor.execute(sql)  # 执行sql语句
    row = cursor.fetchone()  # 读取查询结果,
    while row:  # 循环读取所有结果
        result.append(row[0])
        # print(row[0])  # 输出结果
        row = cursor.fetchone()

    cursor.close()
    connect.close()
    time_end = time.time()
    # print(time_end-time_start)
    return result
   # print(result)

def excel_one_line_to_list_test(filename,linename):
    time_start = time.time()
    # testdata = pd.read_csv(r"D:\untitled\nuaa-HT\8sdata\180103d-1-8s.csv", encoding='utf-8')
    testdata = pd.read_csv(filename, encoding='utf-8')
    rows = len(testdata['时间:'])
    datas_values = testdata.iloc[:rows, linename]
    datas_values_array = np.array(datas_values)
    data = []
    for ech in datas_values_array:
        try:
            s = str(ech)
            a = float(s)
            if np.isnan(a) == False:
                data.append(a)
            # print(a)
        except:
            pass
    time_end = time.time()
    # print(time_end - time_start)
    return data

def euclidean_ses(p, q, t, n):
    # 如果两数据集数目不同，计算两者之间都对应有的数
    summ = 0
    e = [0] * (t + 1)
    for k in range(1, t + 1):
        for i in range((k - 1) * n, k * n):
            e[k - 1] = e[k - 1] + ((p[i] - q[i]) ** 2) ** .5
        summ = summ + e[k - 1]
    # 计算欧几里德距离,并将其标准化
    if(summ != 0 ):
        for k in range(1, t + 1):
            e[k - 1] = 1 / (1 + e[k - 1] / summ)
            if(e[k - 1] < 0.9):
                e[k - 1], path = fastdtw(p[(k - 1) * 1000 : k * 1000], q[(k - 1) * 1000 : k * 1000], dist=euclidean)
                e[k - 1] = 1 / (1 + e[k - 1] / summ)
    else:
        for k in range(1, t + 1):
            e[k - 1] = 1
    return e

def signifying(p):
    k = [''] * (len(p) - 2)
    for i in range(1,len(p) - 1):
        if (p[i - 1] < p[i]) & (p[i] < p[i + 1]):
            k[i - 1] = 'A'
        elif (p[i - 1] == p[i]) & (p[i] == p[i + 1]):
            k[i - 1] = 'B'
        elif (p[i - 1] > p[i]) & (p[i] > p[i + 1]):
            k[i - 1] = 'C'
        elif (p[i - 1] == p[i]) & (p[i] < p[i + 1]):
            k[i - 1] = 'D'
        elif (p[i - 1] == p[i]) & (p[i] > p[i + 1]):
            k[i - 1] = 'E'
        elif (p[i - 1] < p[i]) & (p[i] == p[i + 1]):
            k[i - 1] = 'F'
        elif (p[i - 1] > p[i]) & (p[i] == p[i + 1]):
            k[i - 1] = 'G'
        elif (p[i - 1] < p[i]) & (p[i] > p[i + 1]):
            k[i - 1] = 'H'
        elif (p[i - 1] > p[i]) & (p[i] < p[i + 1]):
            k[i - 1] = 'I'
    return k

def find_lcsubstr(s1, s2):
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]  #生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax=0   #最长匹配的长度
    p=0  #最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                m[i+1][j+1]=m[i][j]+1
                if m[i+1][j+1]>mmax:
                    mmax=m[i+1][j+1]
                    p=i+1
    return mmax   #返回最长子串及其长度


def find_lcseque(s1, s2):
    # 生成字符串长度加1的0矩阵，m用来保存对应位置匹配的结果
    m = [[0 for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]
    # d用来记录转移方向
    d = [[None for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]

    for p1 in range(len(s1)):
        for p2 in range(len(s2)):
            if s1[p1] == s2[p2]:  # 字符匹配成功，则该位置的值为左上方的值加1
                m[p1 + 1][p2 + 1] = m[p1][p2] + 1
                d[p1 + 1][p2 + 1] = 'ok'
            elif m[p1 + 1][p2] > m[p1][p2 + 1]:  # 左值大于上值，则该位置的值为左值，并标记回溯时的方向
                m[p1 + 1][p2 + 1] = m[p1 + 1][p2]
                d[p1 + 1][p2 + 1] = 'left'
            else:  # 上值大于左值，则该位置的值为上值，并标记方向up
                m[p1 + 1][p2 + 1] = m[p1][p2 + 1]
                d[p1 + 1][p2 + 1] = 'up'
    (p1, p2) = (len(s1), len(s2))
    print(np.array(d))
    s = []
    while m[p1][p2]:  # 不为None时
        c = d[p1][p2]
        if c == 'ok':  # 匹配成功，插入该字符，并向左上角找下一个
            s.append(s1[p1 - 1])
            p1 -= 1
            p2 -= 1
        if c == 'left':  # 根据标记，向左找下一个
            p2 -= 1
        if c == 'up':  # 根据标记，向上找下一个
            p1 -= 1
    s.reverse()
    return ''.join(s),len(s)


def association_analysis(columns1,columns2,tabel_name):

    #columns1 = 14
    #columns2 = 16

    out1 = []
    out2 = []
    print(filepath)
    x = np.array(excel_one_line_to_list(columns1,tabel_name))
    y = np.array(excel_one_line_to_list(columns2,tabel_name))
    print(x)
    print(y)
    out1 = signifying(x)
    out2 = signifying(y)

    strout1 = ''.join(out1)
    strout2 = ''.join(out2)

    #print(find_lcsubstr(strout1,strout2))
    maxsub_length = find_lcsubstr(strout1,strout2)
    return maxsub_length

def file_analysis(columns1,columns2,filename):

    #columns1 = 14
    #columns2 = 16

    out1 = []
    out2 = []
    print(filepath)
    x = np.array(excel_one_line_to_list_test(filename,columns1))
    y = np.array(excel_one_line_to_list_test(filename,columns2))
    print(x)
    print(y)
    out1 = signifying(x)
    out2 = signifying(y)

    strout1 = ''.join(out1)
    strout2 = ''.join(out2)

    #print(find_lcsubstr(strout1,strout2))
    maxsub_length = find_lcsubstr(strout1,strout2)
    return maxsub_length