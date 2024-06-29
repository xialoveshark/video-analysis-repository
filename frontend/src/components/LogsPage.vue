<template>
  <div class="container-fluid">
    <Sidebar :isDarkMode="isDarkMode" :isActive="isActive" :toggleTheme="toggleTheme" :logout="logout" />
    <div class="logs-page">
      <h2>用户操作日志</h2>
      <ul v-if="logs.length">
        <li v-for="log in logs" :key="log.id">
          {{ log.timestamp }} - {{ log.action_type }} - {{ log.description }}
        </li>
      </ul>
      <p v-else>没有日志记录。</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Sidebar from './SideBar.vue'; // 根据实际路径导入

export default {
  components: {
    Sidebar
  },
  data() {
    return {
      logs: [],
      isDarkMode: false, // 根据应用的主题设置调整
      isActive: false // 根据应用的侧边栏设置调整
    };
  },
  methods: {
    fetchLogs() {
      const userId = this.getUserId();
      console.log(`Retrieved user_id from sessionStorage: ${userId}`);
      if (userId) {
        console.log(`Fetching logs for user_id: ${userId}`);
        axios.get(`/api/logs?user_id=${userId}`)
          .then(response => {
            this.logs = response.data;
          })
          .catch(error => {
            console.error(error);
          });
      } else {
        console.error('User ID is null');
      }
    },
    getUserId() {
      // 实现获取当前用户 ID 的方法
      return sessionStorage.getItem('userId');
    }
  },
  created() {
    this.fetchLogs();
  }
};
</script>

<style>
.container-fluid {
  display: flex;
}

.logs-page {
  flex-grow: 1;
  padding: 20px;
  margin-left: 10%; /* 侧边栏宽度 */
  background-color: #f7f8fc;
  min-height: 100vh;
  transition: margin-left 0.3s;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  background-color: #fff;
  margin-bottom: 5px;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
