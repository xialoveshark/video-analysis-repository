import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginPage from '@/components/LoginPage.vue'
import DashBoard from '@/components/DashBoard.vue'
import VideoDetail from '@/components/VideoDetail.vue'; // 引入刚刚创建的组件
import DatabaseDetails from '@/components/DatabaseDetails.vue'
import MyHome from '@/components/MyHome.vue'
import LogsPage from '@/components/LogsPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/DashBoard',
    name: 'DashBoard',
    component: DashBoard
  },
  {
    path: '/details',
    name: 'details',
    component: DatabaseDetails
  },
  {
    path: '/mypage',
    name: 'mypage',
    component: MyHome
  },
  {
    path: '/log',
    name: 'log',
    component: LogsPage
  },
  {
    path: '/video/:id', // 使用动态路由参数:id来捕获视频ID
    name: 'videoDetail',
    component: VideoDetail,
    props: true // 使路由参数作为props传递给组件
  }
]

const router = new VueRouter({
  routes
})

export default router