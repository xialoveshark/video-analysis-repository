import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// 设置 Axios 的默认配置
axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.withCredentials = true

// 将 Axios 挂载到 Vue 实例上，这样在任何地方都可以使用 this.$axios 进行请求
Vue.prototype.$axios = axios

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
