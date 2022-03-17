import flask
import flask_cors
from flask import Flask
from flask_cors import *
import get

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(get.get_obj)  #需要添加的
app.register_blueprint(get.abnormalSeeData)  #需要添加的
app.register_blueprint(get.anomalyDetection)  #需要添加的
app.register_blueprint(get.detection_fromjson)  #需要添加的
app.register_blueprint(get.anomalyDetection_byjson)  #需要添加的
if __name__ == '__main__':
    app.run()
