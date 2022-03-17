<template>
<!--  该模块对应“异常检测”-->
  <div id="AbnormalDetection">
    <!--该el-row标签中对应的是异常检测中的“参数选择”模块。
        该模块采用card组件，点击“选取文件”按钮选择文件，文件会自动上传，展示所有参数；
        点击“查看数据”，可以对参数曲线图片进行查看(此功能目前还未连接后端)-->
    <el-row>
      <el-col :span="20" offset="2">
        <el-card class="box-card">
          <!-- 该div标签中为参数选择card组件的header部分。
               包括模块名称(参数选择)，“选取文件”按钮和“查看数据”按钮，
               点击“选取文件”后的参数列表也显示在header中-->
          <div slot="header" class="clearfix">
            <el-row>
              <el-col :span="6">
                <div><span style="font-size: larger;font-weight: bold">参数选择</span></div>
              </el-col>
              <el-col :span="6" :offset="12">
                <el-upload
                  style="display: inline-block; float: right"
                  class="upload"
                  action="http://127.0.0.1:5000/get_obj"
                  :on-preview="handlePreview"
                  :on-remove="handleRemove"
                  :before-remove="beforeRemove"
                  multiple
                  :on-success="handleSuccess"
                  :limit="1"
                  :on-exceed="handleExceed"
                  :file-list="fileList">
                  <el-button slot="trigger" type="primary">选取文件</el-button>
                  <el-button @click="abnormalSeeData" type="primary">查看数据</el-button>
                </el-upload>
              </el-col>
            </el-row>

            <el-row>
              <el-checkbox
                style="margin-bottom: 30px"
                :indeterminate="isIndeterminate"
                v-show="showCheckAll"
                v-model="checkAll"
                @change="handleCheckAllChange">
                <span style="font-size: larger">全选</span>
              </el-checkbox>
              <el-checkbox-group v-show="showCheck" v-model="checkedCities" @change="handleCheckedCitiesChange">
                <el-checkbox v-for="city in cities" :label="city" :key="city"><span style="font-size: larger">{{city}}</span></el-checkbox>
              </el-checkbox-group>
            </el-row>
          </div>
          <!-- 该div标签中为参数选择card组件的内容部分：点击“查看数据”后显示的image组件-->
<!--          <div style="text-align: center">-->
<!--            <el-image-->
<!--              v-show="showImage1"-->
<!--              style="width: 500px; height: 350px; "-->
<!--              :src="url"-->
<!--              :preview-src-list="srcList">-->
<!--            </el-image>-->
<!--          </div>-->
          <div id="div_group" v-show="showImage1"></div>


        </el-card>
      </el-col>
    </el-row>

    <!--该el-row标签中对应的是异常检测中的“异常检测”模块。
    点击“异常检测”，会出现异常检测的结果图片(此功能目前还未连接后端)-->
    <el-row>
      <el-col :span="20" offset="2" >
        <el-card class="box-card2">
          <!--该div标签中为异常检测card组件的header部分。
          包括模块名称(异常检测)和“异常检测”按钮-->
          <div slot="header" class="clearfix2">
            <el-row>
              <el-col span="10">
                <div><span style="font-size: larger;font-weight: bold">异常检测</span></div>
              </el-col>
              <el-col :span="4" :offset="10">
                <div style="display: inline-block;float: right;">
                  <el-button @click="abnormalDetectionClick" type="primary">异常检测</el-button>
                </div>
              </el-col>
            </el-row>
          </div>
          <!--该div标签中为异常检测card组件的内容部分：点击“异常检测”按钮后显示的image组件-->
<!--          <div style="text-align: center">-->
<!--            <el-image-->
<!--              v-show="showImage2"-->
<!--              style="width: 500px; height: 350px; "-->
<!--              :src="treeurl"-->
<!--              :preview-src-list="shuList">-->
<!--            </el-image>-->
<!--          </div>-->
          <div id="div_group_abnormal" v-show="showImage2"></div>

        </el-card>
      </el-col>
    </el-row>

  </div>
</template>

<script>
// const cityOptions = ['参数1', '参数2', '参数3', '参数4', '参数5', '参数6', '参数7', '参数8'];
import axios from "axios";
import * as echarts from "echarts";

export default {
  name: "AbnormalDetection",
  data() {
    return {
      checkAll: false,
      checkedCities: [],
      cities: [],
      isIndeterminate: true,
      fileList: [],
      treeurl: require("@/assets/abnormalDet/AbnormalDet_sum.png"),
      shuList: [require("@/assets/abnormalDet/AbnormalDet_sum.png"),require("@/assets/abnormalDet/AbnormalDet_1.png"),require("@/assets/abnormalDet/AbnormalDet_2.png"),require("@/assets/abnormalDet/AbnormalDet_3.png"),require("@/assets/abnormalDet/AbnormalDet_4.png"),require("@/assets/abnormalDet/AbnormalDet_5.png"),require("@/assets/abnormalDet/AbnormalDet_6.png"),require("@/assets/abnormalDet/AbnormalDet_7.png"),require("@/assets/abnormalDet/AbnormalDet_8.png")],
      url: require("@/assets/abnormalSee/AbnormalSee_1.png"),
      srcList: [require("@/assets/abnormalSee/AbnormalSee_1.png"),require("@/assets/abnormalSee/AbnormalSee_2.png"),require("@/assets/abnormalSee/AbnormalSee_3.png"),require("@/assets/abnormalSee/AbnormalSee_4.png"),require("@/assets/abnormalSee/AbnormalSee_5.png"),require("@/assets/abnormalSee/AbnormalSee_6.png"),require("@/assets/abnormalSee/AbnormalSee_7.png"),require("@/assets/abnormalSee/AbnormalSee_8.png")],
      printdata: "这里显示文本输出结果",
      showImage1:false,
      showImage2:false,
      showCheckAll:false,
      showCheck:false
    };
  },
  methods: {
    handleRemove(file, fileList) {
      this.fileList = [];
      this.checkedCities = [];
      let div_group_seedata = document.getElementById("div_group");
      div_group_seedata.innerHTML = "";
      this.showImage1 = false;
      let div_group_detection = document.getElementById("div_group_abnormal");
      div_group_detection.innerHTML = "";
      this.showImage2 = false;
      this.showCheckAll = false;
      this.showCheck = false;
    },
    handlePreview(file) {
      console.log(file);
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${ file.name }？`);
    },
    //全选
    handleCheckAllChange(val) {
      this.checkedCities = val ? this.cities : [];
      this.isIndeterminate = false;
    },
    handleCheckedCitiesChange(value) {
      let checkedCount = value.length;
      this.checkAll = checkedCount === this.cities.length;
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length;
    },
    pathForecast(){
      // this.sleep(1000);
      this.showText2 = true;
      this.showImage2 = true;
    },
    // 设置进程暂停一段时间：1000=1S
    sleep(milliSeconds) {
      var startTime = new Date().getTime();
      while (new Date().getTime() < startTime + milliSeconds) {
        console.log(new Date().getTime());
      }
    },
    // 文件上传成功，接收返回的值
    handleSuccess(res,file){
      this.fileList = [];
      this.checkedCities = [];
      this.fileList.push(file['name']);
      let div_group_seedata = document.getElementById("div_group");
      div_group_seedata.innerHTML = "";
      this.showImage1 = false;
      let div_group_detection = document.getElementById("div_group_abnormal");
      div_group_detection.innerHTML = "";
      this.showImage2 = false;
      this.showCheckAll = true;
      this.showCheck = true;
      this.cities = res['columns'];
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/detection_fromjson',
        data: {
          filename:this.fileList[0],
        },
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        }
      }).then(res=>{
        console.log(res.data)
      });
    },
    abnormalSeeData(){
      this.showImage1 = true;
      let checked_cities= this.checkedCities;
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/abnormalSeeData',
        data: {
          filename:this.fileList[0],
          choose_columns: checked_cities
        },
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        }
      }).then(res=>{
        let div_group = document.getElementById("div_group");
        div_group.innerHTML = "";
        for(let i=0;i<checked_cities.length;i++){
          //<div id="echarts1" style="text-align: center;width: 1500px; height: 350px;" v-show="showImage1"></div>
          div_group.innerHTML+='<div id='+ checked_cities[i] +' style=" text-align:center; width:1000px; height:350px;"></div>';
        }
        for(let i=0;i<checked_cities.length;i++) {
          let see_data = echarts.init(document.getElementById(checked_cities[i]));
          // 指定图表的配置项和数据
          let option = {
            xAxis: {
              type: 'category',
              data: res.data['x']
            },
            yAxis: {
              type: 'value'
            },
            series: [
              {
                data: res.data['y'][i],
                type: 'line'
              }
            ],
            title: [
              {
                left: 'center',
                text: ""+checked_cities[i]
              }
            ],
          };
          // 使用刚指定的配置项和数据显示图表。
          see_data.setOption(option);
        }
      });
    },
    abnormalDetectionClick(){
      this.showText2 = true;
      this.showImage2 = true
      let checked_cities= this.checkedCities;
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/anomalyDetection_byjson',
        data: {
          filename:this.fileList[0],
          choose_columns: checked_cities
        },
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        }
      }).then(res=>{
        let div_group = document.getElementById("div_group_abnormal");
        div_group.innerHTML = "";
        for(let i=0;i<checked_cities.length;i++){
          //<div id="echarts1" style="text-align: center;width: 1500px; height: 350px;" v-show="showImage1"></div>
          div_group.innerHTML+='<div id='+ checked_cities[i] +'_abnormal'+ ' style=" text-align:center; width:1000px; height:350px;"></div>';
        }
        console.log(div_group)
        for(let i=0;i<checked_cities.length;i++) {
          let dom_item = document.getElementById(checked_cities[i]+"_abnormal")
          console.log(dom_item)
          let see_data = echarts.init(dom_item);
          // 指定图表的配置项和数据
          let option = {
            xAxis: {
              type: 'category',
              data: res.data['x']
            },
            yAxis: {
              type: 'value'
            },
            series: [
              {
                data: res.data['y'][i],
                type: 'line',
                markArea: {
                  itemStyle: {
                    color: 'red'
                  },
                  data: res.data['markArea'][i]
                }
              }
            ],
            title: [
              {
                left: 'center',
                text: ""+checked_cities[i]
              }
            ],
          };
          // 使用刚指定的配置项和数据显示图表。
          see_data.setOption(option);
        }
      });
    },
  },
}
</script>


<style scoped>
#AbnormalDetection{
  padding: 30px;
}

</style>
