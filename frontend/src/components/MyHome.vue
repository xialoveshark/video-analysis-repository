<template>
    <div class="container-fluid" style="padding: 0;">
      <!-- 侧边栏 -->
    <Sidebar :isDarkMode="isDarkMode" :isActive="isActive" :toggleTheme="toggleTheme" :logout="logout" />
  
      <!-- 主内容区 -->
      <div class="main-content">
        <!-- 搜索框 -->
        <div class="d-flex search-box mt-5 align-items-center justify-content-center" style="width: 80%;">
          <input type="text" placeholder="搜索视频" v-model="searchQuery" class="search-input">
          <button @click="searchVideos" class="search-btn">搜索</button>
        </div>
  
        <!-- 视频展示区域 -->
        <div class="video-grid" style="width: 100%; margin-top: 70px;">
          <!-- 视频卡片 -->
          <div v-for="(video, index) in filteredVideos" :key="index" class="video-card">
            <video :src="video.video_path" muted width="170px" height="180px" ref="videos" @mouseenter="playVideo(index)"
              @mouseleave="stopVideo(index)"
              @click="goToVideoPage(video.video_id)"></video>
            <p class="video-title">{{ video.title }}</p>
          </div>
        </div>
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
        searchQuery: '', // 搜索关键词
        videos: [], // 视频列表
        filteredVideos: [], // 过滤后的视频列表
        isDarkMode: false
      };
    },
    created() {
      this.fetchVideos(); // 初始化时获取视频列表
    },
    methods: {
      fetchVideos() {
        axios.get('/api/videos')
          .then(response => {
            this.videos = response.data;
            this.filteredVideos = this.videos; // 初始化时显示所有视频
          })
          .catch(error => {
            console.error(error);
          });
      },
      searchVideos() {
        if (!this.searchQuery.trim()) {
          this.filteredVideos = this.videos; // 如果搜索关键词为空，则返回全部视频
        } else {
          this.filteredVideos = this.videos.filter(video => {
            return video.title.toLowerCase().includes(this.searchQuery.toLowerCase()); // 返回与搜索关键词匹配的视频标题
          });
        }
      },
      logout() {
        // 清除用户登录状态
        localStorage.removeItem('loggedIn');
        // 跳转回登录页面
        this.$router.push('/');
      },
      playVideo(index) {
        this.$refs.videos[index].play(); // 通过索引播放视频
      },
      stopVideo(index) {
        this.$refs.videos[index].pause(); // 暂停视频播放
      },
      toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        if (this.isDarkMode) {
          document.body.classList.add('darkMode');
          document.documentElement.style.setProperty('--sidebar-bg-light', '#343a40'); // 深色模式
          document.documentElement.style.setProperty('--sidebar-bg-dark', '#f8f9fa'); // 浅色模式
        } else {
          document.body.classList.remove('darkMode');
          document.documentElement.style.setProperty('--sidebar-bg-light', '#f8f9fa'); // 浅色模式
          document.documentElement.style.setProperty('--sidebar-bg-dark', '#343a40'); // 深色模式
        }
      },
      goToVideoPage(videoId) {
        const videoPath = `/video/${videoId}`;
        this.$router.push({ path: videoPath });
      }
    }
  };
  </script>
  
  <style scoped>
  /* 这里放置组件的样式 */
.container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin: 0;
}

.sidebar {
  width: 10%;
  background-color: #f8f9fa;
  position: fixed; /* 添加这一行，使侧边栏固定 */
  height: 100vh; /* 确保侧边栏高度与视口高度一致，可根据需要调整 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar li {
  /* 保持现有样式 */
  margin: 0.7rem;
}

/* 新增样式类用于图标下的注释 */
.sidebar .sidebar-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  font-size: 0.6em; /* 调整字体大小 */
  color: #6c757d; /* 示例颜色，注释文字的颜色 */
}

/* 如果需要，可以进一步优化图标与文字对齐等细节 */
.sidebar i + span {
  margin-top: 5px; /* 在图标和文字间增加一点间距 */
}
:root {
  --sidebar-bg-light: #f8f9fa; /* 浅色模式背景色 */
  --sidebar-bg-dark: #343a40; /* 深色模式背景色 */
}

.sidebar {
  background-color: var(--sidebar-bg-light); /* 默认为浅色模式背景色 */
  /* ... 其他样式 ... */
}
.navigation{
  width: 100%; /* 让导航铺满侧边栏 */
  padding: 10px 0; /* 适当的上下内边距 */
  position: absolute;
  top: 0; /* 确保导航在侧边栏顶部 */
  left: 0;
}
.navigation ul {
  list-style-type: none; /* 去掉默认的列表样式 */
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column; /* 垂直排列项目 */
  align-items: center; /* 水平居中项目 */
}
.navigation li {
  margin: 10px 0; /* 调整每个选项之间的间距 */
}
#toggletheme {
  background-color: var(--sidebar-bg-light);
}
/* 新增样式类用于图标下的注释 */
.sidebar .sidebar-comment {
  display: block; /* 将注释作为块级元素展示，方便控制间距 */
  font-size: 0.8em; /* 调整注释文字的大小 */
  color: #6c757d; /* 注释文字的颜色 */
  text-align: center; /* 文本居中对齐 */
  margin-top: 5px; /* 在图标和注释之间添加一些间距 */
  margin-right: 30px;
}

.main-content {
  width: calc(85% - 30px); /* 减去侧边栏宽度和可能的间距，确保内容不被遮挡 */
  margin-left: 15%; /* 侧边栏宽度，确保内容从侧边栏右侧开始 */
  overflow-y: auto; /* 为主内容区添加滚动条，以防内容溢出 */
}

.search-box {
  margin-bottom: 20px;
  position: fixed; /* 添加这一行，使搜索框固定在顶部 */
  top: 0; /* 设置搜索框距离顶部的距离 */
  left: 15%; /* 调整左侧距离，确保与侧边栏对齐，根据实际情况调整 */
  width: calc(85% - 30px); /* 调整宽度，与主内容区宽度一致，确保不遮挡 */
  z-index: 100; /* 确保搜索框在其他内容之上，避免被遮挡 */
}

.video-grid {
  display: flex;
  flex-wrap: wrap;
}

.video-card {
  margin-right: 10px;
  margin-bottom: 10px;
}

.search-input {
  width: 70%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
/* 新增样式类用于视频标题 */
.video-title {
  text-align: center; /* 文本居中对齐 */
  margin-top: 5px; /* 在视频和标题之间添加一些间距 */
  color: #333; /* 标题文字颜色 */
  font-size: 0.8em; /* 调整标题文字的大小 */
}
.darkMode .video-title {
  color: #f8f9fa; /* 在夜间模式下，将文字颜色改为浅色，以确保与深色背景有足够对比度 */
}

.darkMode {
  background-color: #333;
  color: #fff;
}

.upload-btn{
  position: fixed;
  bottom: 20px;
  left: 20px;
  background-color: #28a745; /* 绿色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px; /* 确保按钮能装下文字 */
  font-size: 16px;
  cursor: pointer;
}
.add-class-btn {
  position: fixed;
  bottom: 80px;
  left: 20px;
  background-color: #28a745; /* 绿色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px; /* 确保按钮能装下文字 */
  font-size: 16px;
  cursor: pointer;
}
.add-teacher-btn{
  position: fixed;
  bottom: 140px;
  left: 20px;
  background-color: #28a745; /* 绿色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px; /* 确保按钮能装下文字 */
  font-size: 16px;
  cursor: pointer;
}
.add-course-btn {
  position: fixed;
  bottom: 200px;
  left: 20px;
  background-color: #28a745; /* 绿色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px; /* 确保按钮能装下文字 */
  font-size: 16px;
  cursor: pointer;
}
.add-btn {
  left: auto;
  right: 20px;
  margin-left: 10px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal1 {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}

.modal1 h2 {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.modal1 form {
  display: flex;
  flex-direction: column;
}

.modal1 .form-group {
  margin-bottom: 20px;
}

.modal1 .form-group label {
  font-size: 16px;
  margin-bottom: 10px;
}

.modal1 .form-group input[type="text"],
.modal1 .form-group input[type="date"],
.modal1 .form-group input[type="number"] {
  width: 100%; /* 输入框宽度100% */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.modal1 .form-group:nth-child(odd) {
  display: flex;
  justify-content: space-between;
}

.modal1 .form-group:nth-child(even) {
  display: flex;
  justify-content: space-between;
}

.modal1 button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.modal1 button[type="submit"] {
  margin-right: 10px;
}

.modal1 button[type="button"] {
  background-color: #dc3545; /* 红色 */
}

.form-box {
  display: flex;
  justify-content: space-between; /* 将两列水平间距平分 */
}

.col1,
.col2 {
  flex-basis: 48%; /* 每列占据父级元素的 48% 宽度 */
  margin: 10px;
  display: flex; /* 将内容居中 */
  flex-direction: column;
  align-items: center; /* 垂直居中 */
  justify-content: center;
}
  </style>
  