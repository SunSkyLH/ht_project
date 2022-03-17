import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import  ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false

Vue.use(VueAxios,axios)
Vue.use(ElementUI)


new Vue({
  render: h => h(App),
  router,
}).$mount('#app')
