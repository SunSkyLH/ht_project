import pandas as pd
import os
import prework
import numpy as np
import  xlwt
import csv
#两个函数：1、将所有要转换成csv文件的txt放在一个文件夹下，一起给转换了
#2、选择一个，转换一个

def single_txttocsv(filename):
    #filename = "D:/untitled/nuaa-HT/处理后的文件/02D/180102D装战斗部后联合测试_非密/9S01(9S01_9S02_9S03_9S04_9S41_9S42_9S43_9S44_9S45_9S46_9S05_9S06_9S07_9S08_9S09_9S10_9S11_9S48_9S49_9S50_9S51_9S52_9S12_).txt"
    #文件路径
     #savename = ""
    #savename = filename
    try:
        savename = ''
        for i in range (len(filename)):
            if filename[-i] == '.':
                savename = filename[0:-i]+".csv"
                break
        #print(savename)
        data = pd.read_csv(filename,encoding='gbk',low_memory=False,sep='\\s+',skiprows=0,error_bad_lines=False)
        #data = pd.read_csv(filename,encoding='gbk',sep='\s+')
        #print(data)
        print(data.shape[1])
        csv_columns = ["时间:"]
        for i in range(data.shape[1]-1):
            linename = i+1
            csv_columns.append("S%d"%linename)
        #print(csv_columns)
        #data.columns = ["时间:","8S01","8S02"  , "8S03"  ,  "8S04"  ,"8S05" ,  "8S06" ,   "8S07"  ,   "8S08",    "8S09" , "8S10"  , "8S11 " , "8S12" ,"8S13"   ,"8S14"   , "8S15 "   , " 8S16" ,  "8S17" ,  "8S18"   ,  "8S19" ,  "8S20" ,  "8S21", "8S22" , "8S23" , "8S24" ,"8S25", "8S26" ,"8S27" ,"8S28" , "8S29"  , "8S30","8S31","8S32","8S33","8S34","8S35","8S36","8S37","8S38"]
        data.columns = csv_columns
        #print(data)
        data.to_csv(savename, header= 1,index= 0)
        updata, newtime, ifnull, iferror = prework.chuli_data(savename, 0)
        lenth = len(updata)
        newdata = np.zeros((lenth, data.shape[1]))
        for j in range(len(newtime)):
            newdata[j][0] = newtime[j]
        for i in range(data.shape[1]-1):
            linenum = i + 1
            updata,newtime,ifnull,iferror = prework.chuli_data(savename,linenum)
            for j in range(len(updata)):
                newdata[j][linenum] = updata[j]
        #print(newdata)
        newframe = pd.DataFrame(newdata,columns=csv_columns)
        print(newframe)
        newframe.to_csv(savename, header=1, index=0)
        return ("文件转换成功！")
    except:
        return ("转换文件失败！请检查文件格式！")


def many_txttocsv(fileName):
    #filename = "D:/untitled/nuaa-HT/处理后的文件/02D/180102D装战斗部后联合测试_非密/9S01(9S01_9S02_9S03_9S04_9S41_9S42_9S43_9S44_9S45_9S46_9S05_9S06_9S07_9S08_9S09_9S10_9S11_9S48_9S49_9S50_9S51_9S52_9S12_).txt"
    #文件路径
     #savename = ""
    #savename = filename
    path = ""
    for i in range(len(fileName)):
        if fileName[-(i + 1)] == '/':
            path = fileName[0:-(i + 1)]
            break
    filename_list = list()
    print(path)
    #path = "D:/untitled/nuaa-HT/8sdata"  # 设置路径
    dirs = os.listdir(path)  # 获取指定路径下的文件
    for i in dirs:  # 循环读取路径下的文件并筛选输出
        if os.path.splitext(i)[1] == ".txt":  # 筛选csv文件
            filename_list.append(path + '/' + i)  # 输出所有的csv文件
    print(filename_list)
    try:
        for j in range(len(filename_list)):
            savename = ''
            for i in range (len(filename_list[j])):
                if filename_list[j][-i] == '.':
                    savename = filename_list[j][0:-i]+".csv"
                    break
            print(savename)
            data = pd.read_csv(filename_list[j],encoding='gbk',low_memory=False,sep='\\s+',skiprows=0,error_bad_lines=False)
            #data = pd.read_csv(filename,encoding='gbk',sep='\s+')
            #print(data)
            print(data.shape[1])
            csv_columns = ["时间:"]
            for i in range(data.shape[1]-1):
                linename = i+1
                csv_columns.append("S%d"%linename)
            #print(csv_columns)
            #data.columns = ["时间:","8S01","8S02"  , "8S03"  ,  "8S04"  ,"8S05" ,  "8S06" ,   "8S07"  ,   "8S08",    "8S09" , "8S10"  , "8S11 " , "8S12" ,"8S13"   ,"8S14"   , "8S15 "   , " 8S16" ,  "8S17" ,  "8S18"   ,  "8S19" ,  "8S20" ,  "8S21", "8S22" , "8S23" , "8S24" ,"8S25", "8S26" ,"8S27" ,"8S28" , "8S29"  , "8S30","8S31","8S32","8S33","8S34","8S35","8S36","8S37","8S38"]
            data.columns = csv_columns
            #print(data)
            data.to_csv(savename, header= 1,index= 0)
            updata, newtime, ifnull, iferror = prework.chuli_data(savename, 0)
            lenth = len(updata)
            newdata = np.zeros((lenth, data.shape[1]))
            for j in range(len(newtime)):
                newdata[j][0] = newtime[j]
            for i in range(data.shape[1] - 1):
                linenum = i + 1
                updata, newtime, ifnull, iferror = prework.chuli_data(savename, linenum)
                for j in range(len(updata)):
                    newdata[j][linenum] = updata[j]
            #print(newdata)
            newframe = pd.DataFrame(newdata, columns=csv_columns)
            print(newframe)
            newframe.to_csv(savename, header=1, index=0)
            #newdata = pd.read_csv(savename,encoding='utf-8')
        return ("文件转换成功！")
    except:
        return ("转换文件失败！请检查文件格式！")


#fileName = "D:/untitled/nuaa-HT/处理后的文件/HS/HS-10.txt"
#s = single_txttocsv(fileName)
#print(s)

"""""
#文件路径
file_dir = r'D:/untitled/nuaa-HT/处理后的文件/06D'
index = 4
for ii in range(index):
    #构建新的表格名称
    i = ii+1
    dataname = "\\8S01(8S01_8S02_8S03_8S04_8S05_8S06_8S07_8S08_8S09_8S10_8S11_8S12_8S13_8S14_8S15_8S16_8S17_8S18_8S19_8S20_8S21_8S22_8S23_).txt"
    savename = file_dir + "\\180106d-%d-8s.csv"%i
    #找到文件路径下的所有表格名称，返回列表
    filename = file_dir+'\\%d\\'%i+dataname
    print(filename)
    data = pd.read_csv(filename,encoding='gbk',low_memory=False,sep='\\s+',skiprows=0)
    #data = pd.read_csv(filename,encoding='gbk',sep='\s+')
    #print(data)
    data.columns = ["时间:","8S01","8S02"  , "8S03"  ,  "8S04"  ,"8S05" ,  "8S06" ,   "8S07"  ,   "8S08",    "8S09" , "8S10"  , "8S11 " , "8S12" ,"8S13"   ,"8S14"   , "8S15 "   , " 8S16" ,  "8S17" ,  "8S18"   ,  "8S19" ,  "8S20" ,  "8S21", "8S22" , "8S23" , "8S24" ,"8S25", "8S26" ,"8S27" ,"8S28" , "8S29"  , "8S30","8S31","8S32","8S33","8S34","8S35","8S36","8S37","8S38"]
    #print(data)
    data.to_csv(savename, header= 1,index= 0)
    newdata = pd.read_csv(savename,encoding='utf-8')
    #print(newdata)
"""""























