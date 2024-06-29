<template>
  <div class="sidebar">
    <nav class="navigation">
      <ul class="d-flex flex-column">
        <!-- 首页按钮 -->
        <router-link class="nav-link" :to="{ name: 'DashBoard' }">
          <li class="sidebar-item" :class="{ 'active': isActive('DashBoard') }">
            <i class="bi bi-house-door" :class="{ 'text-pink': isActive('/DashBoard') }"></i>
            <span class="sidebar-comment">首页</span>
          </li>
        </router-link>
        <!-- 动态按钮 -->
        <router-link class="nav-link" :to="{ name: 'log' }">
          <li class="sidebar-item" :class="{ 'active': isActive('log') }">
            <i class="bi bi-wind" :class="{ 'text-pink': isActive('/log') }"></i>
            <span class="sidebar-comment">日志</span>
          </li>
        </router-link>
        <!-- 我的按钮 -->
        <router-link class="nav-link" :to="{ name: 'mypage' }">
          <li class="sidebar-item" :class="{ 'active': isActive('mypage') }">
            <i class="bi bi-person" :class="{ 'text-pink': isActive('/mypage') }"></i>
            <span class="sidebar-comment">我的</span>
          </li>
        </router-link>
        <!-- 切换按钮 -->
        <router-link class="nav-link" :to="{ name: 'DashBoard' }">
          <li class="sidebar-item" @click="toggleTheme">
            <div :class="{ darkMode: isDarkMode }" id="toggletheme">
              <i :class="isDarkMode ? 'bi bi-sun-fill' : 'bi bi-moon-fill'"></i>
              <span class="sidebar-comment">切换</span>
            </div>
          </li>
        </router-link>
        
        <!-- 详情按钮 -->
        <router-link class="nav-link" :to="{ name: 'details' }">
          <li class="sidebar-item" :class="{ 'active': isActive('details') }">
            <i class="bi bi-envelope-fill" :class="{ 'text-pink': isActive('/details') }"></i>
            <span class="sidebar-comment">详情</span>
          </li>
        </router-link>
        <!-- 注销按钮 -->
         <!-- 详情按钮 -->
        <router-link class="nav-link" :to="{ name: 'login' }">
          <li class="sidebar-item">
            <button class="btn btn-link nav-link" @click="logout" style="outline: none;">
              <i class="bi bi-box-arrow-left"></i>
              <span class="sidebar-comment">注销</span>
            </button>
          </li>
        </router-link>
        
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDarkMode: false,
    };
  },
  methods: {
    isActive(route) {
      return this.$route.name === route;
    },
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      if (this.isDarkMode) {
        document.body.classList.add('darkMode');
        document.documentElement.style.setProperty('--sidebar-bg-light', '#343a40');
        document.documentElement.style.setProperty('--sidebar-bg-dark', '#f8f9fa');
        document.documentElement.style.setProperty('--icon-color', '#ff4081'); // 设置夜间模式下图标颜色
      } else {
        document.body.classList.remove('darkMode');
        document.documentElement.style.setProperty('--sidebar-bg-light', '#f8f9fa');
        document.documentElement.style.setProperty('--sidebar-bg-dark', '#343a40');
        document.documentElement.style.setProperty('--icon-color', '#007bff'); // 设置白天模式下图标颜色
      }
    },
    logout() {
      localStorage.removeItem('loggedIn');
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 10%;
  background-color: var(--sidebar-bg-light);
  position: fixed;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navigation {
  width: 100%;
  padding: 10px 0;
  position: absolute;
  top: 0;
  left: 0;
}

.navigation ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sidebar-item {
  width: 100%; /* 确保按钮宽度一致 */
  margin: 0.7rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.sidebar-item.active {
  background: pink;
  scale: 1.1;
}

.sidebar i {
  font-size: 1.5rem; /* 图标大小 */
}

.sidebar .sidebar-comment {
  font-size: 0.8em;
  color: #6c757d;
  margin-top: 5px;
}

.darkMode {
  background-color: #333;
  color: #fff;
}

.darkMode .sidebar-item i {
  color: var(--icon-color); /* 夜间模式下的图标颜色 */
}
#toggletheme{
  background: #fff;
}
.navigation a{
  margin-left: 0;
  width: 100%;
}
.navigation li{
  margin-left: 0;
  /* width: 100%; */
}
</style>
