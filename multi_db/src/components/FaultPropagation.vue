<template>
<!--  该模块对应“故障传播”-->
  <div id="FaultPropagation">
    <!--该el-row标签中对应的是故障传播中的“参数选择”模块。
        该模块采用card组件，点击“选取文件”按钮选择文件，文件会自动上传，展示所有参数；
        点击“查看数据”，可以对参数曲线图片进行查看(此功能目前还未连接后端)-->
    <el-row>
      <el-col :span="20" offset="2">
        <el-card class="box-card">
          <!-- 该div标签中为故障传播card组件的header部分。
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
                  :limit="3"
                  :on-exceed="handleExceed"
                  :file-list="fileList">
                  <el-button slot="trigger" type="primary">选取文件</el-button>
                  <el-button @click="faultSeeData" style="display: inline-block" type="primary">查看数据</el-button>
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
              <el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">
                <el-checkbox v-for="city in cities" :label="city" :key="city"><span style="font-size: larger">{{city}}</span></el-checkbox>
              </el-checkbox-group>
            </el-row>
          </div>
          <!-- 该div标签中为参数选择card组件的内容部分：点击“查看数据”后显示的image组件-->
<!--          <div style="text-align: center">-->
<!--            <el-image-->
<!--              v-show="showImage1"-->
<!--              style="width: 500px; height: 350px"-->
<!--              :src="url"-->
<!--              :preview-src-list="srcList">-->
<!--            </el-image>-->
<!--          </div>-->
          <div id="div_group" v-show="showImage1"></div>

        </el-card>
      </el-col>
    </el-row>

    <!--该el-row标签中对应的是故障传播中的“故障传播路径分析”模块。
    点击“路径分析”，会出现分析的文本内容；点击“可视化”，会出现结果图片-->
    <el-row>
      <el-col :span="20" offset="2" >
        <el-card class="box-card2">
          <!--该div标签中为故障传播card组件的header部分。
          包括模块名称(故障传播路径分析)、“路径分析”和“可视化”按钮-->
          <div slot="header" class="clearfix2">
            <el-row>
              <el-col :span="6">
                <div><span style="font-size: larger;font-weight: bold">传播路径挖掘</span></div>
              </el-col>
              <el-col :span="6" offset="12">
                <div style="display: inline-block; float: right;">
                  <el-button @click="faultPathAnalysis"  type="primary">关联分析</el-button>
                  <el-button @click="faultVisualization" type="primary">可视化</el-button>
                </div>
              </el-col>
            </el-row>
          </div>

          <!--该div标签中为故障传播card组件的内容部分：点击“路径分析”按钮后显示的card组件和点击“可视化”按钮后显示的image组件-->
          <div>
            <el-card v-show="showText" class="box-card3" style="display: inline-block">
              <div style="white-space: pre-line">{{printdata}}</div>
            </el-card>
            <el-image
              v-show="showImage2"
              style="width: 400px; height: 350px; margin-left:30px; display: inline-block;"
              :src="treeurl"
              :preview-src-list="shuList">
            </el-image>
          </div>

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
  name: "FaultPropagation",
  data() {
    return {
      checkAll: false,
      checkedCities: [],
      cities: [],
      isIndeterminate: true,
      fileList: [],
      treeurl: require("@/assets/propagation_2.png"),
      shuList: [require("@/assets/propagation_2.png")],
      url: require("@/assets/faultPropaSee/FaultPropa_1.png"),
      srcList: [require("@/assets/faultPropaSee/FaultPropa_1.png"),require("@/assets/faultPropaSee/FaultPropa_2.png"),require("@/assets/faultPropaSee/FaultPropa_3.png"),require("@/assets/faultPropaSee/FaultPropa_4.png"),require("@/assets/faultPropaSee/FaultPropa_5.png"),require("@/assets/faultPropaSee/FaultPropa_6.png"),require("@/assets/faultPropaSee/FaultPropa_7.png"),require("@/assets/faultPropaSee/FaultPropa_8.png")],
      printdata: "参数关联关系挖掘结果如下：\n" +
        "[('WX1001_IN17', 'WX1001_TK38', 'arrows': ['WX1001_IN17']),\n" +
        "('WX1001_IN17', 'WX1001_TK36', 'arrows': ['WX1001_IN17']), \n" +
        "('WX1001_IN7', 'WX1001_ZK17', 'arrows': ['WX1001_ZK17']),\n" +
        "('WX1001_TK37', 'WX1001_ZK17', 'arrows': ['WX1001_TK37'])]\n" +
        "闭合模式挖掘结果如下：\n" +
        "[(2, ['WX1001_IN17']),\n" +
        " (1, ['WX1001_IN7', 'WX1001_ZK17', 'WX1001_TK37']),\n" +
        " (1, ['WX1001_TK36', 'WX1001_IN17']), \n" +
        "(1, ['WX1001_TK38', 'WX1001_IN17'])]",
      showImage1: false,
      showImage2: false,
      showText:false,
      showCheckAll:false,
    };
  },
  methods: {
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
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
    faultSeeData(){
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
    faultVisualization(){
      this.sleep(10000)
      this.showImage2 = true;
    },
    faultPathAnalysis(){
      this.sleep(10000)
      this.showText = true;
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
      this.showCheckAll = true;
      this.cities = res['columns'];
      this.fileList.push(file['name']);
    },
  },
}
</script>

<style scoped>
#FaultPropagation{
  padding: 30px;
}
.box-card3{
  width: 550px;
  height: 350px;
}
</style>
