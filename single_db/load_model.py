#使用kmeans算法对数据进行聚类，试图找到离聚类中心点最近的那个点，即为最具有代表性的点
#缺点---数据长度不一样怎么办，是不是也是随便选，要不要参考时间最长的那个
import numpy as np
import try1
import sys
np.set_printoptions(threshold=np.inf)
import pprint
import os
from numpy import *
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
import pandas as pd
import matplotlib.pyplot as plt
font = {
    'family' : 'SimHei'
}
plt.rc('font', **font)
import matplotlib
matplotlib.rcParams['axes.unicode_minus']=False

import pymssql   #sqlserver数据库


def kmeans(tf,time):
    km = KMeans(n_clusters=2,max_iter=500)
    label = km.fit_predict(tf)
    centroids = km.cluster_centers_  # 获取聚类中心
    #inertia = km.inertia_  # 获取聚类准则的总和
    ttf = csr_matrix(tf).toarray()
    # print(tf)
    # print(ttf)
    newtime0 = list()  #存放的是标签0的时间
    newtime1 = list()  #存放的是标签1的时间
    tttf0 = list()  # 存放的是label标签为0的数据。
    tttf1 = list()  # 存放的是label标签为1的数据。
    #tttf2 = list()  # 存放的是label标签为2的数据。
    #tttf3 = list()  # 存放的是label标签为3的数据。
    for i in range(len(ttf)):
        if label[i] == 1:
            newtime1.append(time[i])
            tttf1.append(ttf[i].tolist())
        elif label[i] == 0:
            newtime0.append(time[i])
            tttf0.append(ttf[i].tolist())
        #elif label[i] == 2:
            #tttf2.append(ttf[i].tolist())
        #else:
            #tttf3.append(ttf[i].tolist())
    return tttf0, tttf1,centroids,newtime0,newtime1
    #return tttf0,tttf1,tttf2,tttf3

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) # 求两个向量之间的距离



"""""
dataname_list = list()
path = "D:/untitled/nuaa-HT/8sdata"                           # 设置路径
dirs = os.listdir(path)                    # 获取指定路径下的文件
for i in dirs:                             # 循环读取路径下的文件并筛选输出
    if os.path.splitext(i)[1] == ".csv":   # 筛选csv文件
        dataname_list.append(path+'/'+i)                         # 输出所有的csv文件
"""""


#for index in range(38):
#6曲线聚类效果不好，9-9
#13,14,17效果一般10+-3+
#19,25，29，33，35是10-8
#31，36是18-0都是直线

def selectdata(linename,dataname_list):
    max_y = 0
    data = []
    time = []
    for i in range(len(dataname_list)):
        testdata = pd.read_csv(dataname_list[i],encoding='utf-8')
        rows = len(testdata['时间:'])
        if rows>=max_y:
            max_y = rows
        time_values = testdata.iloc[:rows, 0]
        # print(input_table_colunms_values)
        time_values_array = np.array(time_values)
        time.append([])
        for ech in time_values_array:
            try:
                s = str(ech)
                a = float(s)
                if np.isnan(a) == False:
                    time[i].append(a)
                # print(a)
            except:
                print("false")
        datas_values = testdata.iloc[:rows, linename]
        datas_values_array = np.array(datas_values)
        data.append([])
        for ech in datas_values_array:
            try:
                s = str(ech)
                a = float(s)
                if np.isnan(a) == False:
                    data[i].append(a)
                #print(a)
            except:
                print("false")

    x = len(data)
    #y = len(data[0])
    kmdata = np.zeros((x,max_y))
    for i in range(len(data)):
        for j in range(len(data[i])):
            kmdata[i][j] = data[i][j]

    #print(kmdata)
    #kmdatas = kmdata.T
    #print(kmdatas)

    newtime0 = list()
    newtime1 = list()
    tttf0 = list()  # 存放的是label标签为0的数据。
    tttf1 = list()  # 存放的是label标签为1的数据。
    #tttf2 = list()  # 存放的是label标签为2的数据。
    #tttf3 = list()  # 存放的是label标签为3的数据。
    #tttf0, tttf1, tttf2, tttf3 = kmeans(kmdata)
    tttf0, tttf1 ,centroids,newtime0,newtime1= kmeans(kmdata,time)
    print("类别1元素个数规模：%d" % len(tttf0))
    print("类别2元素个数规模：%d" % len(tttf1))
    #print(centroids.shape)
    #print(tttf1.shape)
    #print("类别3元素个数规模：%d" % len(tttf2))
    #print("类别4元素个数规模：%d" % len(tttf3))
    lastdata = []
    newtime = []
    max_distence = float(0)
    if len(tttf0)>len(tttf1):
        dist = [[], []]
        for i in range(len(tttf0)):
            vetor = np.array(tttf0[i])
            dis = distEclud(vetor,centroids[0])
            dist[0].append(i)
            dist[1].append(dis)
        min = dist[1][0]
        minnum = dist[0][0]
        for i in range(len(dist[1])):
            if dist[1][i] < min:
                min = dist[1][i]
                minnum = dist[0][i]
        lastdata = tttf0[minnum]
        newtime = newtime0[minnum]
        x = np.array(lastdata)
        for i in range(len(tttf0)):
            if i != minnum:
                vetor = np.array(tttf0[i])
                distence, path = fastdtw(x, vetor, dist=euclidean)
                print(distence)
                if distence > max_distence:
                    max_distence = distence
        for i in range(len(tttf1)):
            vetor = np.array(tttf1[i])
            distence, path = fastdtw(x, vetor, dist=euclidean)
            print(distence)
            if distence > max_distence:
                max_distence = distence

    else:
        dist = [[], []]
        for i in range(len(tttf1)):
            vetor = np.array(tttf1[i])
            dis = distEclud(vetor,centroids[1])
            dist[0].append(i)
            dist[1].append(dis)
        min = dist[1][0]
        minnum = dist[0][0]
        for i in range(len(dist[1])):
            if dist[1][i] < min:
                min = dist[1][i]
                minnum = dist[0][i]
        lastdata = tttf1[minnum]
        newtime = newtime1[minnum]
        x = np.array(lastdata)
        for i in range(len(tttf0)):
            vetor = np.array(tttf0[i])
            distence, path = fastdtw(x, vetor, dist=euclidean)
            print(distence)
            if distence > max_distence:
                max_distence = distence
        for i in range(len(tttf1)):
            if i != minnum:
                vetor = np.array(tttf1[i])
                distence, path = fastdtw(x, vetor, dist=euclidean)
                print(distence)
                if distence > max_distence:
                    max_distence = distence
    return data,time,lastdata,newtime,max_distence



def save_model(tabel_name,path):
    connect = pymssql.connect('127.0.0.1', 'wxx', '12345678', 'mydbtest') #服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    cursor = connect.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
    #sql = "create table wxx_test5(time float,primary key(time))"
    #cursor.execute(sql)   #执行sql语句创建一个表
    #connect.commit()  #提交
    dataname_list = list()
    #path = "D:/untitled/nuaa-HT/8sdata"  # 设置路径
    dirs = os.listdir(path)  # 获取指定路径下的文件
    for i in dirs:  # 循环读取路径下的文件并筛选输出
        if os.path.splitext(i)[1] == ".csv":  # 筛选csv文件
            dataname_list.append(path + '/' + i)  # 输出所有的csv文件
    #for j in range(len(dataname_list[0])):
    testdata = pd.read_csv(dataname_list[0],encoding='utf-8')
    #print(testdata.shape[1])
    for j in range(testdata.shape[1]-1):
        #linename = 4
        linename = j+1
        if linename<25:
            continue
        data,time,lastdata,newtime,max_distence = selectdata(linename,dataname_list)

        print("模板之间的最大距离%f"%max_distence)
        max_distence = max_distence*1.5

        data_array = np.array(data)
        time_array = np.array(time)
        lastdata_array = np.array(lastdata)
        newtime_array = np.array(newtime)

        #print(lastdata_array)
        #sql = "ALTER TABLE wxx_test5 ADD line8S0%d FLOAT NULL" % j  # 列名第一个字符不能是数字，必须是字母
        #cursor.execute(sql)  # 执行sql语句
        #connect.commit()  # 提交
        #建表并设置时间为主键
        ss = "create table model_data_"+tabel_name+"_%d(time float,primary key(time))"%linename
        sql = ss
        cursor.execute(sql)   #执行sql语句创建一个表
        connect.commit()  #提交
        #添加曲线值的列
        ss = "ALTER TABLE model_data_"+tabel_name+"_%d "%linename
        ss2 = "ADD line"+tabel_name+"%d FLOAT NULL" % linename  # 列名第一个字符不能是数字，必须是字母
        sql = ss+ss2
        cursor.execute(sql)  # 执行sql语句
        connect.commit()  # 提交
        #添加最大dtw距离列
        ss = "ALTER TABLE model_data_" + tabel_name + "_%d " % linename
        ss2 = "ADD line_maxdistance" + tabel_name + "%d FLOAT NULL" % linename  # 列名第一个字符不能是数字，必须是字母
        sql = ss + ss2
        cursor.execute(sql)  # 执行sql语句
        connect.commit()  # 提交
        #print(newtime_array)
        print(lastdata_array)
        #27曲线
        for i in range(len(newtime_array)):
            ss = "insert into model_data_"+tabel_name+"_%d " %linename
            ss2 = "(time,line" + tabel_name + "%d," % linename
            ss3 = "line_maxdistance" + tabel_name + "%d)values(%f,%f,%f)" % (linename, newtime_array[i], lastdata_array[i], max_distence)
            sql = ss + ss2 + ss3
            cursor.execute(sql)  # 执行sql语句
            connect.commit()  # 提交
        #try1.Sub2Window.outlist2 = "model_data_"+tabel_name+"_%d数据的表格已经建好"%linename
        print("model_data_"+tabel_name+"_%d数据的表格已经建好"%linename)
        """""
        cnames = {
            'aliceblue':            '#F0F8FF',
            'antiquewhite':         '#FAEBD7',
            'aqua':                 '#00FFFF',
            'aquamarine':           '#7FFFD4',
            'azure':                '#F0FFFF',
            'beige':                '#F5F5DC',
            'bisque':               '#FFE4C4',
            'black':                '#000000',
            'blanchedalmond':       '#FFEBCD',
            'blue':                 '#0000FF',
            'blueviolet':           '#8A2BE2',
            'brown':                '#A52A2A',
            'burlywood':            '#DEB887',
            'cadetblue':            '#5F9EA0',
            'chartreuse':           '#7FFF00',
            'chocolate':            '#D2691E',
            'coral':                '#FF7F50',
            'cornflowerblue':       '#6495ED',
            'cornsilk':             '#FFF8DC',
            'crimson':              '#DC143C',
            'cyan':                 '#00FFFF',
            'darkblue':             '#00008B',
            'darkcyan':             '#008B8B',
            'darkgoldenrod':        '#B8860B',
            'darkgray':             '#A9A9A9',
            'darkgreen':            '#006400',
            'darkkhaki':            '#BDB76B',
            'darkmagenta':          '#8B008B',
            'darkolivegreen':       '#556B2F',
            'darkorange':           '#FF8C00',
            'darkorchid':           '#9932CC',
            'darkred':              '#8B0000',
            'darksalmon':           '#E9967A',
            'darkseagreen':         '#8FBC8F',
            'darkslateblue':        '#483D8B',
            'darkslategray':        '#2F4F4F',
            'darkturquoise':        '#00CED1',
            'darkviolet':           '#9400D3',
            'deeppink':             '#FF1493',
            'deepskyblue':          '#00BFFF',
            'dimgray':              '#696969',
            'dodgerblue':           '#1E90FF',
            'firebrick':            '#B22222',
            'floralwhite':          '#FFFAF0',
            'forestgreen':          '#228B22',
            'fuchsia':              '#FF00FF',
            'gainsboro':            '#DCDCDC',
            'ghostwhite':           '#F8F8FF',
            'gold':                 '#FFD700',
            'goldenrod':            '#DAA520',
            'gray':                 '#808080',
            'green':                '#008000',
            'greenyellow':          '#ADFF2F',
            'honeydew':             '#F0FFF0',
            'hotpink':              '#FF69B4',
            'indianred':            '#CD5C5C',
            'indigo':               '#4B0082',
            'ivory':                '#FFFFF0',
            'khaki':                '#F0E68C',
            'lavender':             '#E6E6FA',
            'lavenderblush':        '#FFF0F5',
            'lawngreen':            '#7CFC00',
            'lemonchiffon':         '#FFFACD',
            'lightblue':            '#ADD8E6',
            'lightcoral':           '#F08080',
            'lightcyan':            '#E0FFFF',
            'lightgoldenrodyellow': '#FAFAD2',
            'lightgreen':           '#90EE90',
            'lightgray':            '#D3D3D3',
            'lightpink':            '#FFB6C1',
            'lightsalmon':          '#FFA07A',
            'lightseagreen':        '#20B2AA',
            'lightskyblue':         '#87CEFA',
            'lightslategray':       '#778899',
            'lightsteelblue':       '#B0C4DE',
            'lightyellow':          '#FFFFE0',
            'lime':                 '#00FF00',
            'limegreen':            '#32CD32',
            'linen':                '#FAF0E6',
            'magenta':              '#FF00FF',
            'maroon':               '#800000',
            'mediumaquamarine':     '#66CDAA',
            'mediumblue':           '#0000CD',
            'mediumorchid':         '#BA55D3',
            'mediumpurple':         '#9370DB',
            'mediumseagreen':       '#3CB371',
            'mediumslateblue':      '#7B68EE',
            'mediumspringgreen':    '#00FA9A',
            'mediumturquoise':      '#48D1CC',
            'mediumvioletred':      '#C71585',
            'midnightblue':         '#191970',
            'mintcream':            '#F5FFFA',
            'mistyrose':            '#FFE4E1',
            'moccasin':             '#FFE4B5',
            'navajowhite':          '#FFDEAD',
            'navy':                 '#000080',
            'oldlace':              '#FDF5E6',
            'olive':                '#808000',
            'olivedrab':            '#6B8E23',
            'orange':               '#FFA500',
            'orangered':            '#FF4500',
            'orchid':               '#DA70D6',
            'palegoldenrod':        '#EEE8AA',
            'palegreen':            '#98FB98',
            'paleturquoise':        '#AFEEEE',
            'palevioletred':        '#DB7093',
            'papayawhip':           '#FFEFD5',
            'peachpuff':            '#FFDAB9',
            'peru':                 '#CD853F',
            'pink':                 '#FFC0CB',
            'plum':                 '#DDA0DD',
            'powderblue':           '#B0E0E6',
            'purple':               '#800080',
            'red':                  '#FF0000',
            'rosybrown':            '#BC8F8F',
            'royalblue':            '#4169E1',
            'saddlebrown':          '#8B4513',
            'salmon':               '#FA8072',
            'sandybrown':           '#FAA460',
            'seagreen':             '#2E8B57',
            'seashell':             '#FFF5EE',
            'sienna':               '#A0522D',
            'silver':               '#C0C0C0',
            'skyblue':              '#87CEEB',
            'slateblue':            '#6A5ACD',
            'slategray':            '#708090',
            'snow':                 '#FFFAFA',
            'springgreen':          '#00FF7F',
            'steelblue':            '#4682B4',
            'tan':                  '#D2B48C',
            'teal':                 '#008080',
            'thistle':              '#D8BFD8',
            'tomato':               '#FF6347',
            'turquoise':            '#40E0D0',
            'violet':               '#EE82EE',
            'wheat':                '#F5DEB3',
            'white':                '#FFFFFF',
            'whitesmoke':           '#F5F5F5',
            'yellow':               '#FFFF00',
            'yellowgreen':          '#9ACD32'}#画图曲线的颜色
        color = list()
        for key,value in cnames.items():
            color.append(str(key))

        plt.figure(figsize=(8, 6), dpi=100)
        plt.title("遥测数据 model_data_"+tabel_name+"_%d 曲线" % linename)
        plt.xlabel("时间")
        plt.ylabel("数值")
        for i in range(len(time_array)):
            plt.plot(time_array[i], data_array[i][0:len(time_array[i])], color=color[i], linestyle='-', linewidth=0.5)

        plt.plot(newtime_array, lastdata_array[0:len(newtime_array)], color='red', linestyle='--', linewidth=2)
        plt.legend(loc='best')
        #plt.savefig('./test%d.jpg' %linename)
        plt.show()
        """""


    cursor.close()   #关闭游标
    connect.close()  #关闭连接

#path = "D:/untitled/nuaa-HT/8sdata"
#tabel_name = "8S"
#save_model(tabel_name,path)