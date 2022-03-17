<template>
<!--  该模块对应“模块整合”-->
  <div id="ModuleIntegration">

    <el-row>
      <el-col :span="20" offset="2">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
              <el-row>
                <el-col :span="6">
                  <div><span style="font-size: larger;font-weight: bold">异常检测</span></div>
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
                    <el-button @click="abnormalDetectionClick" type="primary">异常检测</el-button>
                  </el-upload>
                </el-col>
              </el-row>

              <el-row>
                <el-checkbox
                  style="margin-bottom: 30px"
                  :indeterminate="isIndeterminate"
                  v-model="checkAll"
                  v-show="showCheckAll"
                  @change="handleCheckAllChange">
                  <span style="font-size: larger">全选</span>
                </el-checkbox>
                <el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">
                  <el-checkbox v-for="city in cities" :label="city" :key="city"><span style="font-size: larger">{{city}}</span></el-checkbox>
                </el-checkbox-group>
              </el-row>
          </div>

          <div>
            <el-card v-show="showText1" class="box-card1" style="display: inline-block">
              <div style="white-space: pre-line">{{printdata1}}</div>
            </el-card>
            <el-image
              v-show="showImage1"
              style="width: 400px; height: 350px; margin-left:30px; display: inline-block;"
              :src="url"
              :preview-src-list="srcList">
            </el-image>
          </div>

        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="20" offset="2" >
        <el-card class="box-card2">
          <div slot="header" class="clearfix2">
            <el-row>
              <el-col :span="10">
                <div><span style="font-size: larger;font-weight: bold">故障传播路径分析</span></div>
              </el-col>
              <el-col :span="4" :offset="10">
                <div style="display: inline-block;float: right;">
                  <el-button @click="pathForecast" type="primary">传播预测</el-button>
                </div>
              </el-col>
            </el-row>
          </div>

        <div>
          <el-card v-show="showText2" class="box-card3" style="display: inline-block">
            <div style="white-space: pre-line">{{printdata2}}</div>
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
export default {
  name: "ModuleIntegration",
  data() {
    return {
      checkAll: false,
      checkedCities: [],
      cities: [],
      isIndeterminate: true,
      fileList: [],
      treeurl: require("@/assets/moduleInte_prop/propTree.png"),
      shuList: [require("@/assets/moduleInte_prop/propTree.png")],
      url: require("@/assets/moduleInte_abnormal/AbnormalDet_sum.png"),
      srcList: [require("@/assets/moduleInte_abnormal/AbnormalDet_sum.png"),],
      printdata1: "异常检测结果如下：\n"+
      "参数 ['WX1001_IN17'、'WX1001_IN7'、'WX1001_TK38'、\n'WX1001_TK39'、'WX1001_TK36'、'WX1001_TK37'、\n'WX1001_ZK17'、'WX1001_ZK19']"+" 中存在异常，请及时检查！",
      printdata2: "参数因果关联关系挖掘结果如下：\n" +
        "[('WX1001_IN7', 'WX1001_ZK17', 'arrows': ['WX1001_ZK17']),\n" +
        "('WX1001_IN7', 'WX1001_TK38', 'arrows': ['WX1001_TK38']),\n" +
        "('WX1001_IN7', 'WX1001_TK36', 'arrows': ['WX1001_TK36']), \n" +
        "('WX1001_ZK19', 'WX1001_ZK17', 'arrows': ['WX1001_ZK19']),\n" +
        "('WX1001_TK37', 'WX1001_ZK17', 'arrows': ['WX1001_TK37']),\n" +
        "('WX1001_ZK17', 'WX1001_TK39', 'arrows': ['WX1001_TK39']),\n" +
        "('WX1001_TK39', 'WX1001_TK38', 'arrows': ['WX1001_TK39']),\n" +
        "('WX1001_IN17', 'WX1001_TK38', 'arrows': ['WX1001_IN17']),\n" +
        "('WX1001_TK36', 'WX1001_IN17', 'arrows': ['WX1001_IN17'])]\n",
      showText1:false,
      showImage1:false,
      showText2:false,
      showImage2:false,
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
    abnormalDetectionClick(){
      this.sleep(5000);
      this.showImage1 = true;
      this.showText1 = true;
    },
    pathForecast(){
      this.sleep(5000);
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
    handleSuccess(res){
      // this.showCheckAll = true;
      // this.cities = res['columns'];
    }
  },
}
</script>


<style scoped>
  #ModuleIntegration{
    padding: 30px;
  }
  .box-card1{
    width: 500px;
    height: 350px;
  }
  .box-card3{
    width: 550px;
    height: 350px;
  }

</style>
