#给的数据是最长的。脉宽1.2和1都算异常，指令10秒发出11秒都异常。0点会给，卡的严。
#输入基准数据，创建规则库，存入本地放到数据库里。 2、数据自己找规则。3、告诉新的数据，告诉正确，存入新模板。4、判断新数据。
#要能够泛化。主要是方法能够使用。
#基于图形相似性识别率还不够高，但是普适性很好。要能够和其他曲线进行对比。
#不能太繁琐。弱化人为操作自己判断。
import sys
from testmain import Ui_MainWindow
from testsub import Ui_Dialog
from testsub2 import Ui_Dialog2
from testsub3 import Ui_Dialog3
from testsub4 import Ui_Dialog4
import work_code
import load_model
import test7_txt_csv
import related
import os
from PyQt5.QtGui import QPixmap
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QApplication,QMainWindow,QDialog
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
font = {
    'family' : 'SimHei'
}
plt.rc('font', **font)
matplotlib.rcParams['axes.unicode_minus']=False
import os
from PIL import Image
#filepath = ''

def process_image(filename, mwidth, mheight):
    image = Image.open(filename)
    w, h = image.size
    if w <= mwidth and h <= mheight:
        print(filename, 'is OK.')
        return
    if (1.0 * w / mwidth) > (1.0 * h / mheight):
        scale = 1.0 * w / mwidth
        new_im = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)

    else:
        scale = 1.0 * h / mheight
        new_im = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
    new_im.save(filename)



class CommonHelper:
    def __init__(self):
        pass
    @staticmethod
    def readQss(style):
        file = open(style, encoding='gb18030', errors='ignore')
        return file.read()
        #with open(style, 'r') as f:
            #return f.read()

#把总体相似度的100.00调成正常的百分比形式
#as的3，20,23，24，25
class Sub1Window(QDialog,Ui_Dialog):
    def __init__(self):
        super(Sub1Window,self).__init__()
        self.setupUi(self)
    #filepath = ''
    def onClick_Button_backtomain(self):
        self.close()
        self.textEdit.setPlainText("")
        self.textEdit_2.setPlainText("")
        self.textEdit_3.setPlainText("")
        self.label_2.setPixmap(QPixmap(""))
        self.label_3.setPixmap(QPixmap(""))
        mainwindow.show()
    def onClick_Button_Openfile(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        work_code.filepath = fileName
        #fh = open('filename.txt', 'w', encoding='utf-8')
        #fh.write(fileName)
        #fh.close()
    def onClick_Button_Work(self):
        p1 = int(self.textEdit.toPlainText())
        p2 = str(self.textEdit_3.toPlainText())
        print(p1)
        print(work_code.filepath)
        overall_similarity,euc,linetime,img,model = work_code.anomaly_detection(p1,p2)
        outlist =  "该数据的曲线如左图所示，该数据的模板曲线如右图所示\n"
        outlist = outlist + "当前检测的是数据的第 %d 维:\n"%p1
        #outlist = outlist + "该数据的模板曲线如右图所示\n该数据的曲线如左图所示\n该数据与模板曲线的相似度为:\n"
        #outlist = outlist + "各段局部相似度为: \n"
        lastlist = "各段局部相似度为: \n"
        low_i = []
        for i in range(0, linetime):
            s = "percent: %.2f%% \n" % (euc[i] * 100)
            if euc[i]*100<90:
                low_i.append(i)
            lastlist = lastlist + s
        #print(outlist)
        if len(low_i)!=0:
            outlist = outlist + "数据局部相似度较低的片段：\n"
            for i in range(len(low_i)):
                l = (int(low_i[i]))*1000
                r = (int(low_i[i])+1)*1000
                if i != (len(low_i)-1):
                    outlist = outlist + " %d 至 %d 、"%(l,r)
                else:
                    outlist = outlist + " %d 至 %d \n"%(l,r)
            outlist = outlist + "数据上述片段局部相似度较低！请及时检查！\n"
        else:
            outlist = outlist + "数据无相似度较低片段。\n"
        outlist = outlist + "该数据与模板曲线的相似度为:\n"
        print("总体距离为 %.2f%%" % overall_similarity)
        if overall_similarity<90:
            outlist = outlist + "总体相似度为: %.2f%%\n" % overall_similarity
        else:
            outlist = outlist + "总体相似度合格！\n"
        outlist = outlist + lastlist
        #img,model, p = workfile.linefunc(p1, 1, 1)
        #outlist = "该数据的模板曲线如右图所示\n该数据的曲线如左图所示\n该数据可能为异常数据的概率为%f"%p
        self.textEdit_2.setPlainText(outlist)

        #img = "D:/untitled/nuaa-HT/wxxtest/test%d.jpg" %p1
        # print(imgfile)
        #model = "D:/untitled/nuaa-HT/wxxtest/model%d.jpg" %p1
        process_image(img,252,249)
        self.label_2.setPixmap(QPixmap(img))

        process_image(model, 252, 249)
        self.label_3.setPixmap(QPixmap(model))



#加入其它曲线和模板曲线进行dtw计算，找出最大乘以二加入模板
#需要对AS4重新建模板（AS4一个是0一个是1）
class Sub2Window(QDialog,Ui_Dialog2):
    def __init__(self):
        super(Sub2Window,self).__init__()
        self.setupUi(self)
    modelpath = ''
    #outlist2 = ''
    def onClick_Button_backtomain(self):
        self.close()
        self.textEdit.setPlainText("")
        #self.textEdit_2.setPlainText("")
        self.textEdit_3.setPlainText("")
        #self.label_4.setPixmap(QPixmap(""))
        #self.label_3.setPixmap(QPixmap(""))
        mainwindow.show()
    def onClick_Button_Openfile(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        for i in range(len(fileName)):
            if fileName[-(i+1)] == '/':
                self.modelpath = fileName[0:-(i+1)]
                break
        print(self.modelpath)
        #self.modelpath = fileName
        #fh = open('filename.txt', 'w', encoding='utf-8')
        #fh.write(fileName)
        #fh.close()
    def onClick_Button_Work(self):
        p1 = str(self.textEdit.toPlainText())
        #p2 = float(self.textEdit_2.toPlainText())
        load_model.save_model(p1,self.modelpath)
        outlist = "新模板 %s 已经建立完毕并成功存入数据库！"%p1
        self.textEdit_3.setPlainText(outlist)

        #image1 = cv2.imread(img)
        #imagereshape1 = cv2.resize(image1, (252, 249))
        #cv2.imwrite(img, imagereshape1)
        # cv2.imshow("123",imagereshape)
        #process_image(img,217,249)
        #self.label_3.setPixmap(QPixmap(img))
        #self.lable_2.setScaledContents(True)

        #img2 = workfile.line_1(1, 2, 3)
        #image2 = cv2.imread(model)
        #imagereshape2 = cv2.resize(image2, (252, 249))
        #cv2.imwrite(model, imagereshape2)
        #process_image(model, 217, 249)
        #self.label_4.setPixmap(QPixmap(model))
        #self.lable_3.setScaledContents(True)

#输入至日志，还要判断谁比较低并显示
class Sub3Window(QDialog,Ui_Dialog3):
    def __init__(self):
        super(Sub3Window,self).__init__()
        self.setupUi(self)
    def onClick_Button_backtomain(self):
        self.hide()
        self.textEdit.setPlainText("")
        self.textEdit_2.setPlainText("")
        self.textEdit_3.setPlainText("")
        self.textEdit_5.setPlainText("")
        #self.textEdit_4.setPlainText("")
        #self.label_5.setPixmap(QPixmap(""))
        #self.label_6.setPixmap(QPixmap(""))
        mainwindow.show()
    def onClick_Button_Openfile(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        work_code.filepath = fileName
        #fh = open('filename.txt', 'w', encoding='utf-8')
        #fh.write(fileName)
        #fh.close()
    def onClick_Button_Work(self):
        p1 = str(self.textEdit.toPlainText())
        p2 = int(self.textEdit_2.toPlainText())
        p3 = int(self.textEdit_3.toPlainText())
        #p4 = float(self.textEdit_4.toPlainText())
        outlist = ""
        lowsimilarity_line = set()
        low_wholesimilarity = set()
        for linenum in range(p2,p3+1):
            overall_similarity, euc, linetime, img, model = work_code.anomaly_detection(linenum, p1)
            outlist = outlist + "-----当前检测的是数据的第 %d 维-----\n" % linenum
            outlist = outlist + "该数据与模板曲线的相似度为:\n"
            #outlist = outlist + "该数据的模板曲线如右图所示\n该数据的曲线如左图所示\n该数据可能为异常数据的概率为:\n"
            print("总体相似度为 %.2f%%" % overall_similarity)
            if overall_similarity < 90:
                outlist = outlist + "总体相似度较低！相似度为: %.2f%%\n" % overall_similarity
            else:
                outlist = outlist + "总体相似度合格！\n"
            if overall_similarity<90:
                low_wholesimilarity.add(linenum)
            outlist = outlist + "各段局部相似度为: \n"
            for i in range(0, linetime):
                s = "percent: %.2f%% \n" % (euc[i] * 100)
                if euc[i]<0.90:
                    lowsimilarity_line.add(linenum)
                outlist = outlist + s
            print(outlist)

        low_line = list(lowsimilarity_line)
        low_wholeline = list(low_wholesimilarity)
        signal = ""
        if (len(low_line)==0)and(len(low_wholeline)==0):
            signal = "数据 第%d维 至 第%d维 检测完毕，检测数据无异常，符合标准。\n"%(p2,p3)
        else:
            if (len(low_wholeline)!=0):
                signal = signal + "数据 第%d维 至 第%d维 检测完毕，出现整体相似度较低的属性：\n" % (p2, p3)
                for j in range(len(low_wholeline)):
                    if j != (len(low_wholeline) - 1):
                        signal = signal + "第 %d 维 、" % int(low_wholeline[j])
                    else:
                        signal = signal + "第 %d 维" % int(low_wholeline[j])
                signal = signal + "\n上述属性整体相似度较低！请及时检查！\n"
            if (len(low_line)!=0):
                signal = signal + "数据 第%d维 至 第%d维 检测完毕，出现局部相似度较低的属性：\n"%(p2,p3)
                for j in range(len(low_line)):
                    if j != (len(low_line)-1):
                        signal = signal + "第 %d 维 、"%int(low_line[j])
                    else:
                        signal = signal + "第 %d 维"%int(low_line[j])
                signal = signal + "\n上述属性局部相似度较低！请及时检查！\n"

        outlist = signal +outlist
        with open("%s.txt" % p1, "w") as f:  # 格式化字符串还能这么用！
            f.write(outlist)

        self.textEdit_5.setPlainText(outlist)

        #image1 = cv2.imread(img)
        #imagereshape1 = cv2.resize(image1, (252, 249))
        #cv2.imwrite(img, imagereshape1)
        # cv2.imshow("123",imagereshape)
        #process_image(img,242,299)
        #self.label_5.setPixmap(QPixmap(img))
        #self.lable_2.setScaledContents(True)

        #img2 = workfile.line_1(1, 2, 3)
        #image2 = cv2.imread(model)
        #imagereshape2 = cv2.resize(image2, (252, 249))
        #cv2.imwrite(model, imagereshape2)
        #process_image(model, 242, 299)
        #self.label_6.setPixmap(QPixmap(model))
        #self.lable_3.setScaledContents(True)

class Sub4Window(QDialog,Ui_Dialog4):
    def __init__(self):
        super(Sub4Window,self).__init__()
        self.setupUi(self)
    #modelpath = ''
    #outlist2 = ''
    def onClick_Button_backtomain(self):
        self.close()
        self.textEdit.setPlainText("")
        self.textEdit_2.setPlainText("")
        self.textEdit_3.setPlainText("")
        #self.label_4.setPixmap(QPixmap(""))
        #self.label_3.setPixmap(QPixmap(""))
        mainwindow.show()
    def onClick_Button_Openfile(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")

        linename_str = str(self.textEdit_2.toPlainText())
        linename_list = linename_str.split(",")
        columns1 = int(linename_list[0])
        minlength = 100000000  # 几个最长公共子序列取最小值
        for columns2 in range(1, len(linename_list)):
            submaxlength = related.file_analysis(columns1, int(columns2), fileName)
            if submaxlength < minlength:
                minlength = submaxlength

        outlist = "输入属性的最长公共子序列为：\n"
        outlist = outlist + str(minlength)
        self.textEdit_3.setPlainText(outlist)

    def onClick_Button_Work(self):
        tabel_name = str(self.textEdit.toPlainText())
        linename_str = str(self.textEdit_2.toPlainText())
        linename_list = linename_str.split(",")
        columns1 = int(linename_list[0])
        minlength = 100000000 #几个最长公共子序列取最小值
        for columns2 in range(1,len(linename_list)):
            submaxlength = related.association_analysis(columns1,int(columns2),tabel_name)
            if submaxlength<minlength:
                minlength = submaxlength

        outlist = "输入属性的最长公共子序列为：\n"
        outlist = outlist + str(minlength)
        self.textEdit_3.setPlainText(outlist)




#所有关于画图的程序，标题记得改了，现在都是默认8s要改成s
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
    def onClick_Button_Jumptosub1(self):
        self.hide()
        self.textEdit.setPlainText("本系统建议使用CSV格式的文件进行操作。")
        sub1window.show()
    def onClick_Button_Jumptosub2(self):
        self.hide()
        self.textEdit.setPlainText("本系统建议使用CSV格式的文件进行操作。")
        sub2window.show()
    def onClick_Button_Jumptosub3(self):
        self.hide()
        self.textEdit.setPlainText("本系统建议使用CSV格式的文件进行操作。")
        sub3window.show()
    def onClick_Button_Jumptosub4(self):
        self.hide()
        self.textEdit.setPlainText("本系统建议使用CSV格式的文件进行操作。")
        sub4window.show()
    def openfile(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                      "All Files(*);;Text Files(*.txt)")
        global filename
        filename = fileName
        #观察待测数据



    def s_txttocsv(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        signaltext = test7_txt_csv.single_txttocsv(fileName)
        self.textEdit.setPlainText(signaltext)
        #单个txt文件转csv文件

    def m_txttocsv(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        signaltext = test7_txt_csv.many_txttocsv(fileName)
        self.textEdit.setPlainText(signaltext)
        #一个文件夹的txt文件转csv文件

    def showdata(self):
        # print(filename)
        if len(filename) > 0:
            global input_table
            input_table = pd.read_csv(filename)
            # print(input_table)
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.shape[1]
            # print(input_table_rows)
            # print(input_table_colunms)
            input_table_header = input_table.columns.values.tolist()
            # print(input_table_header)

            ###===========读取表格，转换表格，============================================
            ###======================给tablewidget设置行列表头============================
            self.tableWidget.setColumnCount(input_table_colunms)
            self.tableWidget.setRowCount(input_table_rows)
            self.tableWidget.setHorizontalHeaderLabels(input_table_header)
            ###======================给tablewidget设置行列表头============================

            ###================遍历表格每个元素，同时添加到tablewidget中========================
            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]
                # print(input_table_rows_values)
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                # print(input_table_rows_values_list)
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]
                    # print(input_table_items_list)
                    # print(type(input_table_items_list))

                    ###==============将遍历的元素添加到tablewidget中并显示=======================

                    input_table_items = str(input_table_items_list)
                    newItem = QtWidgets.QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, newItem)

                    ###================遍历表格每个元素，同时添加到tablewidget中========================
            # else:
            # self.centralWidget.show()

    def Showdata(self):
        j = self.tableWidget.currentColumn()
        # print(j)
        # print(input_table)
        rows = self.tableWidget.rowCount()
        """""
        #input_table_colunms_values = input_table.iloc[:rows, j]
        #time_values = input_table.iloc[:rows, 0]
        datas_values = input_table.iloc[:rows, j]
        time_values = input_table.iloc[:rows, 0]
        # print(input_table_colunms_values)
        time_values_array = np.array(time_values)
        input_table_colunms_values_array = np.array(input_table_colunms_values)
        input_table_colunms_values_list = input_table_colunms_values_array.tolist()
        time = time_values_array.tolist()
        # print(time_values_array)
        # print(input_table_colunms_values_array)
        """""
        #j = self.tableWidget.currentColumn()
        # print(j)
        # print(input_table)
        #rows = self.tableWidget.rowCount()
        # input_table_colunms_values = input_table.iloc[:rows, j]
        # time_values = input_table.iloc[:rows, 0]
        datas_values = input_table.iloc[:rows, j]
        time_values = input_table.iloc[:rows, 0]
        time_values_array = np.array(time_values)
        datas_values_array = np.array(datas_values)
        time = list()
        i = 0
        for ech in time_values_array:
            try:
                s = str(ech)
                a = float(s)
                time.append(a)
                # print(a)
            except:
                print("false")
        data = list()
        for ech in datas_values_array:
            try:
                s = str(ech)
                a = float(s)
                data.append(a)
                # print(a)
            except:
                print("false")
        time_array = np.array(time)
        data_array = np.array(data)
        # print(time_array)
        # print(data_array[0])
        # print(type(data_array[0]))
        plt.figure(figsize=(8, 6), dpi=100)
        plt.title("遥测数据 S0%d 曲线" %j)
        plt.xlabel("时间")
        plt.ylabel("数值")
        plt.plot(time_array, data_array[0:-1], color='red', linestyle='-', linewidth=1,
                 label="S0%d 数据的曲线" %j)
        plt.legend(loc='best')
        #plt.savefig('./test2.jpg')
        plt.show()
        # plt.show()
        # 折线图，一图两线
        # print(input_table_colunms_values_list)

        """""
        self.hide()  # 如果没有self.form.show()这一句，关闭Demo1界面后就会关闭程序
        form1 = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(form1)
        form1.show()
        form1.exec_()
        self.show()
        """""



if __name__ == '__main__':
    app = QApplication(sys.argv)
    sub1window = Sub1Window()
    sub2window = Sub2Window()
    sub3window = Sub3Window()
    sub4window = Sub4Window()
    mainwindow = MainWindow()
    #styleFile = 'D:/untitled/QSS-master/AMOLED.qss'
    #styleFile = 'D:/untitled/QSS-master/MaterialDark.qss'
    #styleFile = 'D:/untitled/QSS-master/Ubuntu.qss'
    #styleFile = 'D:/untitled/QSS-master/uuchen.qss'
    #styleFile = 'D:/untitled/qss/abc.qss'
    #styleFile = 'D:/untitled/qss/style2.qss'
    #styleFile = 'D:/untitled/qss/stylesheet2.qss'
    #styleFile = 'D:/untitled/qss/qss/stylesheet2.qss'
    styleFile = 'D:/untitled/qss/qss/QDarkStyleSheet.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    mainwindow.setStyleSheet(qssStyle)
    sub1window.setStyleSheet(qssStyle)
    sub2window.setStyleSheet(qssStyle)
    sub3window.setStyleSheet(qssStyle)
    sub4window.setStyleSheet(qssStyle)
    mainwindow.show()
    sys.exit(app.exec_())


