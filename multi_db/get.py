import datetime
import json
import os

import backserver_v2
import flask
from flask import Blueprint, request
import pandas as pd
import load_json_v2
import numpy as np
get_obj = Blueprint("get_obj", __name__)
abnormalSeeData = Blueprint("abnormalSeeData", __name__)
anomalyDetection = Blueprint("anomalyDetection", __name__)
detection_fromjson = Blueprint("detection_fromjson", __name__)
anomalyDetection_byjson = Blueprint("anomalyDetection_byjson", __name__)

@get_obj.route("/get_obj", methods=['POST'])
def fun():
    file = request.files['file']
    name = file.filename
    file.save(name)
    csv_file = pd.read_csv(name)
    return {'columns': list(csv_file.columns)[1:]}

@abnormalSeeData.route("/abnormalSeeData", methods=['POST'])
def abnormal_seedata():
    request_json = request.get_json()
    #获取浏览器发送的请求数据，并转为JSON格式
    filename = request_json['filename']
    choose_columns = request_json['choose_columns']
    data_path = "./data/"
    all_data = pd.read_csv(data_path+filename)
    columns = all_data.columns
    choose_data = []
    for i in range(len(choose_columns)):
        item = all_data[choose_columns[i]].values.tolist()
        choose_data.append(item)
    # print(np.array(choose_data).shape)
    index = all_data[columns[0]].values.tolist()
    # index = list(map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"), index))
    return {"x": index,"y":choose_data}

@anomalyDetection.route("/anomalyDetection", methods=['POST'])
def anomaly_detection(): #这个函数和上面@后面的不能重名
    request_json = request.get_json()
    # 获取浏览器发送的请求数据，并转为JSON格式
    filename = request_json['filename']
    choose_columns = request_json['choose_columns']
    data_path = "./data/"
    filepath = data_path + filename
    all_data = pd.read_csv(filepath)
    columns = all_data.columns
    flag = False
    if len(columns)==len(choose_columns):
        flag = True
    check_feature = set()
    check_column = set(choose_columns)
    #columns把time当做了第0下标，因此算出的下标全部-1
    for i in range(len(columns)):
        if columns[i] in check_column:
            check_feature.add(i-1)
    df_index,realY,return_anomaly = backserver_v2.anomaly_detection(filepath,flag,check_feature)
    return {"x": df_index, "y": realY, "markArea": return_anomaly}

@anomalyDetection_byjson.route("/anomalyDetection_byjson", methods=['POST'])
def anomaly_detection_json():
    request_json = request.get_json()
    # 获取浏览器发送的请求数据，并转为JSON格式
    filename = request_json['filename']
    choose_columns = request_json['choose_columns']
    data_path = "./data/"
    filepath = data_path + filename
    json_path = data_path+'data.json'
    all_data = pd.read_csv(filepath)
    columns = all_data.columns
    flag = False
    if len(columns) == len(choose_columns):
        flag = True
    check_column = set(choose_columns)

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        if filename in json_data:
            anomaly_data = json_data[filename]
            return_anomaly = []
            for i in range(len(choose_columns)):
                for j in range(len(anomaly_data)):
                    if list(anomaly_data[j].keys())[0]==choose_columns[i]:
                        return_anomaly.append(anomaly_data[j][choose_columns[i]])
            realY = []
            all_data_list = all_data.values.T.tolist()
            df_index = all_data_list[0]
            for i in range(len(choose_columns)):
                for j in range(len(all_data_list)):
                    if choose_columns[i]==columns[j]:
                        realY.append(all_data_list[j])
            return {"x": df_index, "y": realY, "markArea": return_anomaly}

    check_feature = set()
    #columns把time当做了第0下标，因此算出的下标全部-1
    for i in range(len(columns)):
        if columns[i] in check_column:
            check_feature.add(i-1)
    df_index,realY,return_anomaly = backserver_v2.anomaly_detection(filepath,flag,check_feature)
    return {"x": df_index, "y": realY, "markArea": return_anomaly}



@detection_fromjson.route("/detection_fromjson", methods=['POST'])
def red_json(): #这个函数和上面@后面的不能重名？
    request_json = request.get_json()
    # 获取浏览器发送的请求数据，并转为JSON格式
    filename = request_json['filename']
    data_path = "./data/"
    filepath = data_path + filename
    json_path = data_path+'data.json'
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        if filename not in json_data:
            return_anomaly = load_json_v2.save_Asjson(filepath)
            json_data[filename] = return_anomaly
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(json_data, ensure_ascii=False))
            f.close()
    else:
        return_anomaly = load_json_v2.save_Asjson(filepath)
        json_data = {filename: return_anomaly}
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()
    return {"ifsavejson":True}







