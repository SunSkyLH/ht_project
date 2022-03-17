import testsub
import testmain
import testsub2
import try1
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QApplication,QMainWindow,QDialog
import sys
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import pymssql
import time
from scipy import stats
import matplotlib.pyplot as plt
font = {
    'family' : 'SimHei'
}
plt.rc('font', **font)
import matplotlib
matplotlib.rcParams['axes.unicode_minus']=False

filepath = ""
#求出来的曲线图像和异常值诊断

def linefunc(a,b,c):
    #函数主体
    imgfile = "D:/untitled/nuaa-HT/type"+str(b)+"-img.jpg"
    print(imgfile)
    model = "D:/untitled/nuaa-HT/type"+str(b)+"-model.jpg"
    print(imgfile)
    print(model)
    #img ='test1.jpg'
    #img是根据数据画出的函数曲线图
    print(a)
    print(b)
    print(c)
    probability = 0.01
    #probability是根据数据求出的该数据可能为异常的概率

    #返回函数图像路径和可能为异常值的几率
    return imgfile,model,probability



#第一个直线型函数模板长什么样的函数
def line_1(p1,b,c):
    #参数p1是可视化界面上输入的管道阈值
    #参数b,c等是大佬们自己设置的
    #函数主体
    img = 'test1.jpg'
    #返回第一类型模板图像路径
    return img


def excel_one_line_to_list(i,tabel_name):
    connect = pymssql.connect('127.0.0.1', 'wxx', '12345678', 'mydbtest')  # 建立连接
    if connect:
        print("连接成功!")
    time_start = time.time()
    result = []
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    #sql = "select line8S0%d from wxx_data_test%d"%(i,i)
    s1 = "select line"+tabel_name+"%d "%i
    s2 = "from model_data_"+tabel_name+"_%d"%i
    sql = s1+s2
    cursor.execute(sql)  # 执行sql语句
    row = cursor.fetchone()  # 读取查询结果,
    while row:  # 循环读取所有结果
        result.append(row[0])
       # print(row[0])  # 输出结果
        row = cursor.fetchone()

    max_distance = float(0)
    # sql = "select line8S0%d from wxx_data_test%d"%(i,i)
    s1 = "select line_maxdistance" + tabel_name + "%d " % i
    s2 = "from model_data_" + tabel_name + "_%d" % i
    sql = s1 + s2
    cursor.execute(sql)  # 执行sql语句
    row = cursor.fetchone()  # 读取查询结果,
    max_distance = row[0]

    cursor.close()
    connect.close()
    time_end = time.time()
   # print(time_end-time_start)
    return result,max_distance
   # print(result)

def excel_one_line_to_list_test(filename,linename):
    time_start = time.time()
    #testdata = pd.read_csv(r"D:\untitled\nuaa-HT\8sdata\180103d-1-8s.csv", encoding='utf-8')
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
    #print(time_end - time_start)
    return data


def euclidean_ses(p, q, t, n):
    # 如果两数据集数目不同，计算两者之间都对应有的数
    summ = 0
    sumn = 0
    e = [0] * (t + 1)
    a = [0] * (t + 1)
    for k in range(1, t + 1):
        for i in range((k - 1) * n, k * n):
            e[k - 1] = e[k - 1] + ((p[i] - q[i]) ** 2) ** .5
        summ = summ + e[k - 1]
    # 计算欧几里德距离,并将其标准化
    if (summ != 0):
        for k in range(1, t + 1):
            a[k - 1] = e[k - 1]
            e[k - 1] = 1 / (1 + e[k - 1] / summ)
            if (e[k - 1] < 0.95):
                sumn = a[k - 1] + sumn
                a[k - 1], path = fastdtw(p[(k - 1) * 1000: k * 1000], q[(k - 1) * 1000: k * 1000], dist=euclidean)
        for k in range(1, t + 1):
            if (e[k - 1] < 0.95):
                e[k - 1] = 1 / (1 + a[k - 1] / summ)
    else:
        for k in range(1, t + 1):
            e[k - 1] = 1

    return e

def tryfunc(updata):
    updata_np = np.array(updata)
    updata_np_avg = np.sum(updata_np) / len(updata_np)
    print(updata_np_avg)
    newupdata = updata_np - updata_np_avg
    #print(newupdata)
    return (np.maximum(newupdata, -newupdata))

def tryfunc2(updata):
    updata_np = np.array(updata)
    updata_np_many = stats.mode(updata_np)[0][0]
    print(updata_np_many)
    newupdata = updata_np - updata_np_many
    # print(newupdata)
    return (np.maximum(newupdata, -newupdata))


def anomaly_detection(columns,tabel_name):
    #columns = 16
    N = 1000
    #filepath = "D:/untitled/nuaa-HT/8sdata/180103d-1-8s.csv"
    print(filepath)
    x,max_distance = np.array(excel_one_line_to_list(columns,tabel_name))#模板
    #print("====")
    y = np.array(excel_one_line_to_list_test(filepath,columns))#测试

    new_x = tryfunc2(x)
    new_y = tryfunc2(y)

    x_time = np.zeros(len(x))
    for i in range(len(x)):
        x_time[i]=i
    y_time = np.zeros(len(y))
    for i in range(len(y)):
        y_time[i]=i

    #print(imgfile)
    #print(model)
    x_length = len(x)
    y_length = len(y)

    euc = []
    time = 0
    if x_length < y_length:
        time = x_length
    else:
        time = y_length
    time = time // N
    print("time = %d"%time)
    euc = euclidean_ses(x,y,time,N)
    new_euc = euclidean_ses(new_x,new_y,time,N)

    low_xyi = []
    for i in range(0, time):
        s = "percent: %.2f%% \n" % (euc[i] * 100)
        if euc[i] * 100 < 90:
            low_xyi.append(i)
    low_newxyi = []
    for i in range(0, time):
        s = "percent: %.2f%% \n" % (euc[i] * 100)
        if new_euc[i] * 100 < 90:
            low_newxyi.append(i)
    if (len(low_xyi)<=len(low_newxyi)):
        xx = x
        yy = y
        final_euc = euc
    else:
        xx = new_x
        yy = new_y
        final_euc = new_euc
    distence, path = fastdtw(xx,yy,dist = euclidean)
    plt.figure(figsize=(8, 6), dpi=100)
    plt.title("遥测数据 S0%d 模板曲线" % columns)
    plt.xlabel("时间")
    plt.ylabel("数值")
    plt.plot(x_time, xx, color="blue", linestyle='-', linewidth=1)
    plt.legend(loc='best')
    plt.savefig('./model%d.jpg' % columns)
    plt.close()

    plt.title("遥测数据 S0%d 检测曲线" % columns)
    plt.xlabel("时间")
    plt.ylabel("数值")
    plt.plot(y_time, yy, color='red', linestyle='--', linewidth=1)
    plt.legend(loc='best')
    plt.savefig('./test%d.jpg' % columns)
    plt.close()

    imgfile = './test%d.jpg' % columns
    # print(imgfile)
    model = './model%d.jpg' % columns

    overall_similarity = float(0)
    if distence<=max_distance:
        overall_similarity = 100.0
    else:
        overall_similarity = (max_distance / (max_distance + abs(max_distance - distence))) * 100

    return overall_similarity,final_euc,time,imgfile,model
    #distance = dtw_se(x, y, dist_for_float)
    #print(distence)
    #for i in range(0, time):
        #print('percent: {:.2f}%'.format(euc[i] * 100))

#anomaly_detection(16)



