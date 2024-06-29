<template>
  <div class="video-page container-fluid">
    <div class="mainvideo-box">
      <!-- 返回首页按钮 -->
    <button @click="returnToHome" class="home-btn">
      <i class="fas fa-arrow-left"></i>
    </button>
      <h2 style="text-align: center; font-weight: 600;">{{ video.title }}</h2>
      <!-- 视频 -->
      <div class="video-container" v-if="video" style="height: auto;">
        <video :src="video.video_path" class="main-video" controls style="max-width: 740px;"></video>
      </div>
      <!-- 分析视频按钮 -->
      <button @click="analyzeVideo" :class="{ 'analyze-btn': true, 'analyzing': analyzing }">
        <span v-if="!analyzing">分析视频</span>
        <span v-else>
          <i class="fas fa-circle-notch fa-spin"></i> 分析中...
        </span>
      </button>
      <!-- 左下角内容 -->
      <div class="content">
        <div class="content-column">
          <div class="description-box">
            <p>上传日期: {{ video.upload_date }}</p>
            <p>清晰度评分: {{ video.clarity_rating }}</p>
            <p>互动性评分: {{ video.interactivity_rating }}</p>
            <p>正确性评分: {{ video.correctness_rating }}</p>
          </div>
        </div>
        <div class="content-column">
          <div class="description-box">
            <p>参与度评分: {{ video.engagement_rating }}</p>
            <p>内容深度评分: {{ video.content_depth_rating }}</p>
            <p>错误描述: {{ video.error_description }}</p>
            <p>更正: {{ video.correction }}</p>
            <p>评论: {{ video.comments }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 右侧视频列表 -->
    <div class="video-list">
      <ul>
        <li v-for="video in otherVideos" :key="video.video_id" @mouseover="playVideo(video)" @mouseleave="pauseVideo(video)" @click="navigateToVideoDetail(video)">
          <video :src="video.video_path" ref="videoRefs" muted></video>
          <p style="text-align: center;">标题: {{ video.title }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      video: null,
      otherVideos: [], // 其他视频列表
      analysisResult: null, // 分析结果
      analyzing:false
    };
  },
  created() {
    this.fetchVideoDetail();
  },
  watch: {
    '$route.params.id': 'fetchVideoDetail'
  },
  methods: {
    fetchVideoDetail() {
      const videoId = this.$route.params.id;
      axios.get(`/api/video/${videoId}`)
        .then(response => {
          this.video = response.data;
          this.fetchAllVideos(); // 获取所有视频信息
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchAllVideos() {
      // 发起请求获取所有视频信息
      axios.get(`/api/videos`)
        .then(response => {
          this.otherVideos = response.data.filter(video => video.video_id !== this.video.video_id); // 过滤掉当前视频
        })
        .catch(error => {
          console.error(error);
        });
    },
    navigateToVideoDetail(video) {
      this.$router.push({ name: 'videoDetail', params: { id: video.video_id } }); // 假设路由配置为 ideo/:id
    },
    playVideo(video) {
      const videoElement = this.$refs.videoRefs.find(el => el.src.includes(video.video_path));
      videoElement.play();
    },
    pauseVideo(video) {
      const videoElement = this.$refs.videoRefs.find(el => el.src.includes(video.video_path));
      videoElement.pause();
    },
    analyzeVideo() {
      // 开始分析，显示加载指示器
      this.analyzing = true;

      axios.post('/api/analyze_video', { video_id: this.video.video_id })
        .then(response => {
          this.analysisResult = response.data;
          // 更新视频对象的评分字段
          this.video.clarity_rating = this.analysisResult.评分.清晰度;
          this.video.interactivity_rating = this.analysisResult.评分.互动性;
          this.video.engagement_rating = this.analysisResult.评分.参与度;
          this.video.correctness_rating = this.analysisResult.评分.正确性;
          this.video.content_depth_rating = this.analysisResult.评分.内容深度;
          this.video.error_description = this.analysisResult.错误;
          this.video.correction = this.analysisResult.改正后的文本;
          this.video.comments = this.analysisResult.总体评价;
          // 保存分析结果到数据库
          axios.put(`/api/video/${this.video.video_id}`, {
            clarity_rating: this.video.clarity_rating,
            interactivity_rating: this.video.interactivity_rating,
            engagement_rating: this.video.engagement_rating,
            correctness_rating: this.video.correctness_rating,
            content_depth_rating: this.video.content_depth_rating,
            error_description: this.video.error_description,
            correction: this.video.correction,
            comments: this.video.comments
          })
            .then(() => {
              console.log('视频分析结果已保存到数据库');
              // 开始分析，显示加载指示器
              this.analyzing = false;
            })
            .catch(error => {
              console.error('保存视频分析结果时出错:', error);
              // 开始分析，显示加载指示器
              this.analyzing = false;
            });
        })
        .catch(error => {
          console.error('分析视频时出错:', error);
          // 开始分析，显示加载指示器
          this.analyzing = false;
        });
    },
    returnToHome() {
      this.$router.push({ name: 'DashBoard' }); // Replace 'home' with your actual home route name
    }
  }
};
</script>

<style scoped>
.video-page {
  display: flex;
  font-family: Arial, sans-serif;
  font-weight: 600;
  padding: 60px;
  padding-top: 0;
  padding-bottom: 0;
  justify-content: center;
}

.video-container {
  border-radius: 4px;
  margin-top: 5px;
  margin-left: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.home-btn {
    position: fixed;
    top: 20px;
    left: 20px;
    width: 70px;
    height: 70px;
    font-size: 30px;
    background-color: #FF4081; /* Green */
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 50%;
    z-index: 1000; /* Ensure it's above other content */
    transition: transform 0.2s ease; /* 添加过渡效果 */
  }

  .home-btn:hover {
    /* background-color: #45a049; */
    transform: scale(1.1);
  }
.mainvideo-box {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
  gap: 10px;
  width: 70%;
}

.content {
  display: flex;
  max-height:100vh; 
  justify-content: start;
  margin-right: 30px;
  margin-top: 0px;
  
}

.content-column {
  flex: 1;
  margin-left: 30px;
  font-size: larger;
}

.video-list {
  max-height: 100vh;
  flex: 1;
  margin-top: 20px;
  margin-left: 20px;
  overflow-y: auto;
  overflow-x: hidden;
}

.main-video {
  height: 430px;
  width: auto;
  border-radius: 0.7rem;
}

.video-list h2 {
  margin-top: 0;
}

.video-list ul {
  padding: 0;
  list-style: none;
}
.video-list li{
  flex-direction: column;
}
.video-list video {
  width: 100%;
  margin-bottom: 10px;
}

.description-box {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
  height: 35vh;
  padding-top: 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.video-list video {
  border-radius: 0.7rem;
}

.analyze-btn {
  margin-top: 20px;
  background-color: #ff69b4; /* 粉色 */
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  width: 80%;
  margin-left: 10%;
}

.analyze-btn:hover {
  background-color: #ff85c0;
}
</style>
