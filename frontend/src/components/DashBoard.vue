<template>
  <div class="container-fluid" style="padding: 0;">
    <!-- 侧边栏 -->
    <Sidebar :isDarkMode="isDarkMode" :isActive="isActive" :toggleTheme="toggleTheme" :logout="logout" />

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 搜索框 -->
      <div class="d-flex search-box mt-5 align-items-center justify-content-center" style="width: 80%;">
        <input type="text" placeholder="搜索视频" v-model="searchQuery" class="search-input" @keyup.enter="searchVideos">
        <button @click="searchVideos" class="search-btn" style="background: #FF4081;">搜索</button>
      </div>

      <!-- 视频展示区域 -->
      <div class="video-grid" style="width: 100%; margin-top: 70px;">
        <div v-for="(video, index) in filteredVideos" :key="index" class="video-card">
          <video :src="video.video_path" :controls="true" muted width="170px" height="180px" ref="videos" 
          @mouseenter="handleMouseEnter(index)"
          @mouseleave="handleMouseLeave(index)"
          @click="goToVideoPage(video.video_id)"></video>
          <p class="video-title">{{ video.title }}</p>
        </div>
      </div>
    </div>

    <!-- 上传视频按钮 -->
    <button class="upload-btn" @click="showUploadModal = true">上传视频</button>
    <button class="add-class-btn" @click="showAddCourseModal = true">添加课程</button>
    <button class="add-teacher-btn" @click="showAddTeacherModal = true">添加教师</button>
    <button class="add-course-btn" @click="showAddCoursePlanModal = true">添加教学计划</button>

    <!-- 上传视频弹窗 -->
    <div v-if="showUploadModal" class="modal-overlay">
      <div style="background: white;" class="modal1">
        <h2>上传视频</h2>
        <form @submit.prevent="uploadVideo">
          <div class="form-box">
            <div class="col1">
              <div>
                <label for="title">视频标题</label>
                <div>
                  <input type="text" id="title" v-model="newVideo.title" required>
                </div>
              </div>
              <div>
                <label for="video_path">视频路径</label>
                <div>
                  <input style="width: 100%;" type="file" id="video_path" ref="video_path" @change="handleFileUpload" required>
                </div>
              </div>
              <div>
                <label for="upload_account">上传账号</label>
                <div>
                  <input type="text" id="upload_account" v-model="newVideo.upload_account" required>
                </div>
              </div>
              <div>
                <label for="upload_date">上传日期</label>
                <div>
                  <input style="width: 188px;height: 30px;" type="date" id="upload_date" v-model="newVideo.upload_date" required>
                </div>
              </div>
              <button type="submit" style="margin-top: 20px">提交</button>
            </div>
            <div class="col2">
              <div>
                <label for="course_name">课程名称</label>
                <div>
                  <input type="text" id="course_name" v-model="newVideo.course_name" required>
                </div>
              </div>
              <div>
                <label for="teacher_name">教师名称</label>
                <div>
                  <input type="text" id="teacher_name" v-model="newVideo.teacher_name" required>
                </div>
              </div>
              <div>
                <label for="week">周次</label>
                <div>
                  <input type="number" id="week" v-model="newVideo.week" required>
                </div>
              </div>
              <div>
                <label for="error_description">错误分析</label>
                <div>
                  <input type="text" id="error_description" v-model="newVideo.error_description" required>
                </div>
              </div>
              <button style="margin-top: 20px;" type="button" @click="showUploadModal = false">取消</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- 添加课程弹窗 -->
    <div v-if="showAddCourseModal" class="modal-overlay">
      <div style="background: white;" class="modal1">
        <h2>添加课程</h2>
        <form @submit.prevent="addCourse">
          <div class="form-box">
            <div class="col1">
              <div>
                <label for="course_name">课程名称</label>
                <div>
                  <input type="text" id="course_name" v-model="newCourse.course_name" required>
                </div>
              </div>
              <div>
                <label for="course_description">课程描述</label>
                <div>
                  <input type="text" id="course_description" v-model="newCourse.course_description" required>
                </div>
              </div>
              <div>
                <label for="duration">课程时长</label>
                <div>
                  <input type="number" id="duration" v-model="newCourse.duration" required>
                </div>
              </div>
              <div>
                <label for="university">大学</label>
                <div>
                  <input type="text" id="university" v-model="newCourse.university" required>
                </div>
              </div>
              <button type="submit" style="margin-top: 20px">提交</button>
            </div>
            <div class="col2">
              <div>
                <label for="department">部门</label>
                <div>
                  <input type="text" id="department" v-model="newCourse.department" required>
                </div>
              </div>
              <div>
                <label for="video_num">视频数量</label>
                <div>
                  <input type="number" id="video_num" v-model="newCourse.video_num" required>
                </div>
              </div>
              <div>
                <label for="avg_clarity_rating">平均清晰度评分</label>
                <div>
                  <input type="number" id="avg_clarity_rating" v-model="newCourse.avg_clarity_rating" required>
                </div>
              </div>
              <div>
                <label for="avg_interactivity_rating">平均互动性评分</label>
                <div>
                  <input type="number" id="avg_interactivity_rating" v-model="newCourse.avg_interactivity_rating" required>
                </div>
              </div>
              <div>
                <label for="avg_engagement_rating">平均参与度评分</label>
                <div>
                  <input type="number" id="avg_engagement_rating" v-model="newCourse.avg_engagement_rating" required>
                </div>
              </div>
              <div>
                <label for="avg_correctness_rating">平均正确性评分</label>
                <div>
                  <input type="number" id="avg_correctness_rating" v-model="newCourse.avg_correctness_rating" required>
                </div>
              </div>
              <div>
                <label for="avg_content_depth_rating">平均内容深度评分</label>
                <div>
                  <input type="number" id="avg_content_depth_rating" v-model="newCourse.avg_content_depth_rating" required>
                </div>
              </div>
              <button style="margin-top: 20px;" type="button" @click="showAddCourseModal = false">取消</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- 添加教师弹窗 -->
    <div v-if="showAddTeacherModal" class="modal-overlay">
      <div style="background: white;" class="modal1">
        <h2>添加教师</h2>
        <form @submit.prevent="addTeacher">
          <div class="form-box">
            <div class="col1">
              <div>
                <label for="teacher_name">教师名称</label>
                <div>
                  <input type="text" id="teacher_name" v-model="newTeacher.teacher_name" required>
                </div>
              </div>
              <div>
                <label for="department">部门</label>
                <div>
                  <input type="text" id="department" v-model="newTeacher.department" required>
                </div>
              </div>
              <div>
                <label for="university">大学</label>
                <div>
                  <input type="text" id="university" v-model="newTeacher.university" required>
                </div>
              </div>
              <button type="submit" style="margin-top: 20px">提交</button>
            </div>
            <div class="col2">
              <div>
                <label for="video_num">视频数量</label>
                <div>
                  <input type="number" id="video_num" v-model="newTeacher.video_num" required>
                </div>
              </div>
              <div>
                <label for="avg_clarity_rating">平均清晰度评分</label>
                <div>
                  <input type="number" id="avg_clarity_rating" v-model="newTeacher.avg_clarity_rating" required>
                </div>
              </div>
              <div>
                <label for="avg_interactivity_rating">平均互动性评分</label>
                <div>
                  <input type="number" id="avg_interactivity_rating" v-model="newTeacher.avg_interactivity_rating" required>
                </div>
              </div>
              <div>
                <label for="avg_engagement_rating">平均参与度评分</label>
                <div>
                  <input type="number" id="avg_engagement_rating" v-model="newTeacher.avg_engagement_rating" required>
                </div>
              </div>
              <div>
                <label for="avg_correctness_rating">平均正确性评分</label>
                <div>
                  <input type="number" id="avg_correctness_rating" v-model="newTeacher.avg_correctness_rating" required>
                </div>
              </div>
              <div>
                <label for="avg_content_depth_rating">平均内容深度评分</label>
                <div>
                  <input type="number" id="avg_content_depth_rating" v-model="newTeacher.avg_content_depth_rating" required>
                </div>
              </div>
              <button style="margin-top: 20px;" type="button" @click="showAddTeacherModal = false">取消</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- 添加教学计划弹窗 -->
    <div v-if="showAddCoursePlanModal" class="modal-overlay">
      <div style="background: white;" class="modal1">
        <h2>添加教学计划</h2>
        <form @submit.prevent="addCoursePlan">
          <div class="form-box">
            <div class="col1">
              <div>
                <label for="course_name">课程名称</label>
                <div>
                  <input type="text" id="course_name" v-model="newCoursePlan.course_name" required>
                </div>
              </div>
              <div>
                <label for="teacher_name">教师名称</label>
                <div>
                  <input type="text" id="teacher_name" v-model="newCoursePlan.teacher_name" required>
                </div>
              </div>
              <div>
                <label for="goal">教学目标</label>
                <div>
                  <input type="text" id="goal" v-model="newCoursePlan.goal" required>
                </div>
              </div>
              <div>
                <label for="week">周次</label>
                <div>
                  <input type="number" id="week" v-model="newCoursePlan.week" required>
                </div>
              </div>
              <div>
                <label for="key_point">知识点</label>
                <div>
                  <input type="text" id="key_point" v-model="newCoursePlan.key_point" required>
                </div>
              </div>
              <div>
                <label for="csvFile">上传CSV文件</label>
                <div>
                  <input type="file" id="csvFile" @change="handleCsvUpload">
                </div>
              </div>
              <button type="submit" style="margin-top: 20px">提交</button>
              <button style="margin-top: 20px;" type="button" @click="showAddCoursePlanModal = false">取消</button>
            </div>
          </div>
        </form>
      </div>
    </div>
    <!-- 添加成功的弹窗 -->
    <SuccessModal v-if="showSuccessModal" @close="showSuccessModal = false" />
  </div>
</template>

<script>
import axios from 'axios';
import Sidebar from './SideBar.vue'; // 根据实际路径导入
import SuccessModal from './SuccessModal.vue'; // 导入添加成功的弹窗组件

export default {
  components: {
    Sidebar,
    SuccessModal
  },
  data() {
    return {
      searchQuery: '', // 搜索关键词
      videos: [], // 视频列表
      filteredVideos: [], // 过滤后的视频列表
      isDarkMode: false,
      showUploadModal: false, // 控制上传弹窗显示
      showAddCourseModal: false, // 控制添加课程弹窗显示
      showAddTeacherModal: false, // 控制添加教师弹窗显示
      showAddCoursePlanModal: false, // 控制添加教学计划弹窗显示
      showSuccessModal: false, // 控制添加成功弹窗的显示状态
      playingIndex: null,
      newVideo: {
        title: '',
        video_path:'',
        upload_account: '',
        upload_date: '',
        course_name: '', // 修改为课程名称
        teacher_name: '', // 修改为教师名称
        week: '',
        error_description: ''
      },
      newCourse: {
        course_name: '',
        course_description: '',
        duration: '',
        university: '',
        department: '',
        video_num: '',
        avg_clarity_rating: '',
        avg_interactivity_rating: '',
        avg_engagement_rating: '',
        avg_correctness_rating: '',
        avg_content_depth_rating: ''
      },
      newTeacher: {
        teacher_name: '',
        department: '',
        university: '',
        video_num: '',
        avg_clarity_rating: '',
        avg_interactivity_rating: '',
        avg_engagement_rating: '',
        avg_correctness_rating: '',
        avg_content_depth_rating: ''
      },
      newCoursePlan: {
        course_name: '', // 修改为课程名称
        teacher_name: '', // 修改为教师名称
        goal: '',
        week: '',
        key_point: ''
      }
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
    isActive(route) {
      return this.$route.path === route;
    },
    handleMouseEnter(index) {
      if (this.playingIndex !== null && this.playingIndex !== index) {
        this.$refs.videos[this.playingIndex].pause();
      }
      this.playingIndex = index;
      this.playVideo(index);
    },
    handleMouseLeave(index) {
      this.stopVideo(index);
    },
    playVideo(index) {
      setTimeout(() => {
        if (this.playingIndex === index) {
          this.$refs.videos[index].play();
        }
      }, 100); // 100ms 延迟
    },
    stopVideo(index) {
      if (this.playingIndex === index) {
        this.$refs.videos[index].pause();
        this.playingIndex = null;
      }
    },
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      if (this.isDarkMode) {
        document.body.classList.add('darkMode');
        document.documentElement.style.setProperty('--sidebar-bg-light', '#343a40'); // 深色模式
        document.documentElement.style.setProperty('--sidebar-bg-dark', '#f8f9fa'); // 反向设置，虽然在这里不会用到，但保持一致处理是个好习惯
      } else {
        document.body.classList.remove('darkMode');
        document.documentElement.style.setProperty('--sidebar-bg-light', '#f8f9fa'); // 浅色模式
        document.documentElement.style.setProperty('--sidebar-bg-dark', '#343a40');
      }
    },
    goToVideoPage(videoId) {
      const videoPath = `/video/${videoId}`;
      this.$router.push({ path: videoPath });
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.newVideo.video_path = `\\videos\\${file.name}`;  // 只获取文件名作为路径
      }
    },
    async uploadVideo() {
      try {
        const teacherResponse = await axios.get(`/api/teacher_name/${this.newVideo.teacher_name}`);
        const courseResponse = await axios.get(`/api/course_name/${this.newVideo.course_name}`);
        
        this.newVideo.teacher_id = teacherResponse.data.teacher_id;
        this.newVideo.course_id = courseResponse.data.course_id;

        const videoData = {
          title: this.newVideo.title,
          upload_account: this.newVideo.upload_account,
          upload_date: this.newVideo.upload_date,
          course_id: this.newVideo.course_id,
          teacher_id: this.newVideo.teacher_id,
          week: this.newVideo.week,
          error_description: this.newVideo.error_description,
          video_path: this.newVideo.video_path // 只发送文件路径
        };

        await axios.post('/api/video', videoData);
        this.fetchVideos(); // 上传成功后刷新视频列表
        this.showUploadModal = false; // 关闭弹窗
        // 假设添加成功后，显示成功弹窗
        this.showSuccessModal = true;
      } catch (error) {
        console.error(error);
      }
    },
    addCourse() {
      axios.post('/api/course', this.newCourse)
        .then(() => {
          this.showAddCourseModal = false; // 关闭弹窗
          // 假设添加成功后，显示成功弹窗
        this.showSuccessModal = true;
        })
        .catch(error => {
          console.error(error);
        });
    },
    addTeacher() {
      axios.post('/api/teacher', this.newTeacher)
        .then(() => {
          this.showAddTeacherModal = false; // 关闭弹窗
          // 假设添加成功后，显示成功弹窗
        this.showSuccessModal = true;
        })
        .catch(error => {
          console.error(error);
        });
    },
    async addCoursePlan() {
      try {
        const teacherResponse = await axios.get(`/api/teacher_name/${this.newCoursePlan.teacher_name}`);
        const courseResponse = await axios.get(`/api/course_name/${this.newCoursePlan.course_name}`);
        
        this.newCoursePlan.teacher_id = teacherResponse.data.teacher_id;
        this.newCoursePlan.course_id = courseResponse.data.course_id;

        const coursePlanData = {
          course_id: this.newCoursePlan.course_id,
          teacher_id: this.newCoursePlan.teacher_id,
          goal: this.newCoursePlan.goal,
          week: this.newCoursePlan.week,
          key_point: this.newCoursePlan.key_point
        };

        await axios.post('/api/course_plan', coursePlanData);
        this.showAddCoursePlanModal = false; // 关闭弹窗
        // 假设添加成功后，显示成功弹窗
        this.showSuccessModal = true;
      } catch (error) {
        console.error(error);
      }
    },
    handleCsvUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const contents = e.target.result;
          const rows = contents.split('\n').map(row => row.split(','));
          if (rows.length > 1) {
            const headers = rows[0];
            const values = rows[1];
            const data = {};
            headers.forEach((header, index) => {
              data[header.trim()] = values[index].trim();
            });
            this.newCoursePlan.course_name = data['course_name'] || '';
            this.newCoursePlan.teacher_name = data['teacher_name'] || '';
            this.newCoursePlan.goal = data['goal'] || '';
            this.newCoursePlan.week = data['week'] || '';
            this.newCoursePlan.key_point = data['key_point'] || '';
          }
        };
        reader.readAsText(file);
      }
    }
  }
};
</script>

<style>
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

.upload-btn {
  position: fixed;
  width: 10%;
  bottom: 20px;
  /* left: 20px; */
  background-color: #FF4081; /* 绿色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px; /* 确保按钮能装下文字 */
  font-size: 16px;
  cursor: pointer;
}
.add-class-btn {
  position: fixed;
  width: 10%;
  bottom: 80px;
  /* left: 20px; */
  background-color: #FF4081; /* 绿色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px; /* 确保按钮能装下文字 */
  font-size: 16px;
  cursor: pointer;
}
.add-teacher-btn {
  position: fixed;
  width: 10%;
  bottom: 140px;
  /* left: 20px; */
  background-color: #FF4081; /* 绿色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px; /* 确保按钮能装下文字 */
  font-size: 16px;
  cursor: pointer;
}
.add-course-btn {
  position: fixed;
  width: 10%;
  bottom: 200px;
  /* left: 20px; */
  background-color: #FF4081; /* 绿色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px; /* 确保按钮能装下文字 */
  font-size: 16px;
  cursor: pointer;
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
.modal-overlay label,h2{
  color: #333
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

.col1 div{
  width: 80%;
  justify-content: center;
  align-items: center;
}
</style>
