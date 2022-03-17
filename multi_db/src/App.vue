<template>
  <div id="app">
    <div id="aside">
      <el-menu
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
        background-color="#545c64"
        text-color="#FFFFFF"
        default-active=this.$router.path
        router>

        <el-menu-item index="/Introduction" class="asideitem">
          <i class="el-icon-eleme"></i>
          <span style="font-size: larger" slot="title">系统介绍</span>
        </el-menu-item>
        <el-menu-item index="/Instruction" class="asideitem">
          <i class="el-icon-collection"></i>
          <span style="font-size: larger" slot="title">使用说明</span>
        </el-menu-item>
        <el-menu-item index="/AbnormalDetection" class="asideitem">
          <i class="el-icon-s-opportunity"></i>
          <span style="font-size: larger" slot="title">异常检测</span>
        </el-menu-item>
        <el-menu-item index="/FaultPropagation" class="asideitem">
          <i class="el-icon-s-grid"></i>
          <span style="font-size: larger" slot="title">传播路径挖掘</span>
        </el-menu-item>
        <el-menu-item index="/ModuleIntegration" class="asideitem">
          <i class="el-icon-document"></i>
          <span style="font-size: larger" slot="title">模块整合</span>
        </el-menu-item>

<!--        style="height: 80px;line-height: 80px" index="/FaultPropagation"-->

      </el-menu>
    </div>

    <div id="content">
      <router-view></router-view>
    </div>

  </div>
</template>

<script>
  export default {
    name: 'app'
  }
</script>

<style>
.el-menu {
  width: 200px;
}

.asideitem{
  height: 80px;
  line-height: 80px
}

#aside {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 200px;
  background-color: #545c64;
}

#content {
  position: absolute;
  top: 0;
  left: 200px;
  right: 0;
  bottom: 0;
  overflow-y: scroll;
}

/*隐藏滚动条*/
#content::-webkit-scrollbar {
  display: none;
}
</style>
