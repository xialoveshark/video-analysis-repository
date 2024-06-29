<template>
  <div class="container-fluid">
    <!-- 侧边栏 -->
    <Sidebar :isDarkMode="isDarkMode" :isActive="isActive" :toggleTheme="toggleTheme" :logout="logout" />
    <div class="details-page">
      <h2>详情查询</h2>
      <div class="query-buttons">
        <button @click="fetchTeachers">查询教师</button>
        <button @click="fetchCourses">查询课程</button>
        <button @click="fetchCoursePlans">查询教学计划</button>
        <button @click="fetchVideos">查询视频</button>
      </div>
      <div class="result">
        <div v-if="teachers.length > 0" class="result-section">
          <h3>教师列表</h3>
          <ul>
            <li v-for="teacher in teachers" :key="teacher.teacher_id">
              {{ teacher.teacher_name }} - {{ teacher.department }} - {{ teacher.university }}
              <button @click="deleteTeacher(teacher.teacher_id, false)" class="btn btn-danger btn-sm">限制删除</button>
              <button @click="deleteTeacher(teacher.teacher_id, true)" class="btn btn-warning btn-sm">级联删除</button>
            </li>
          </ul>
        </div>
        <div v-if="courses.length > 0" class="result-section">
          <h3>课程列表</h3>
          <ul>
            <li v-for="course in courses" :key="course.course_id">
              {{ course.course_name }} - {{ course.university }} - {{ course.department }}
              <button @click="deleteCourse(course.course_id, false)" class="btn btn-danger btn-sm">限制删除</button>
              <button @click="deleteCourse(course.course_id, true)" class="btn btn-warning btn-sm">级联删除</button>
            </li>
          </ul>
        </div>
        <div v-if="coursePlans.length > 0" class="result-section">
          <h3>教学计划列表</h3>
          <ul>
            <li v-for="coursePlan in coursePlans" :key="`${coursePlan.course_id}-${coursePlan.teacher_id}-${coursePlan.week}`">
              课程名称: {{ coursePlan.course_name }}, 教师名称: {{ coursePlan.teacher_name }}, 周次: {{ coursePlan.week }}, 教学目标: {{ coursePlan.goal }}, 知识点: {{ coursePlan.key_point }}
              <button @click="deleteCoursePlan(coursePlan.course_id, coursePlan.teacher_id, coursePlan.week, false)" class="btn btn-danger btn-sm">限制删除</button>
              <button @click="deleteCoursePlan(coursePlan.course_id, coursePlan.teacher_id, coursePlan.week, true)" class="btn btn-warning btn-sm">级联删除</button>
            </li>
          </ul>
        </div>
        <div v-if="videos.length > 0" class="result-section">
          <h3>视频列表</h3>
          <ul>
            <li v-for="video in videos" :key="video.video_id">
              {{ video.title }} - {{ video.upload_account }} - {{ video.upload_date }}
              <button @click="deleteVideo(video.video_id, false)" class="btn btn-danger btn-sm">限制删除</button>
              <button @click="deleteVideo(video.video_id, true)" class="btn btn-warning btn-sm">级联删除</button>
            </li>
          </ul>
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
      teachers: [],
      courses: [],
      coursePlans: [],
      videos: []
    };
  },
  methods: {
    fetchTeachers() {
      axios.get('/api/teachers')
        .then(response => {
          this.teachers = response.data;
          this.clearOthers('teachers');
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchCourses() {
      axios.get('/api/courses')
        .then(response => {
          this.courses = response.data;
          this.clearOthers('courses');
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchCoursePlans() {
      axios.get('/api/course_plans')
        .then(response => {
          this.coursePlans = response.data;
          this.clearOthers('coursePlans');
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchVideos() {
      axios.get('/api/video_information')
        .then(response => {
          this.videos = response.data;
          this.clearOthers('videos');
        })
        .catch(error => {
          console.error(error);
        });
    },
    clearOthers(current) {
      if (current !== 'teachers') this.teachers = [];
      if (current !== 'courses') this.courses = [];
      if (current !== 'coursePlans') this.coursePlans = [];
      if (current !== 'videos') this.videos = [];
    },
    deleteTeacher(teacher_id, cascade) {
      axios.delete(`/api/teacher/${teacher_id}?cascade=${cascade}`)
        .then(() => {
          this.fetchTeachers();
        })
        .catch(error => {
          console.error(error);
        });
    },
    deleteCourse(course_id, cascade) {
      axios.delete(`/api/course/${course_id}?cascade=${cascade}`)
        .then(() => {
          this.fetchCourses();
        })
        .catch(error => {
          console.error(error);
        });
    },
    deleteCoursePlan(course_id, teacher_id, week, cascade) {
      axios.delete(`/api/course_plan/${course_id}/${teacher_id}/${week}?cascade=${cascade}`)
        .then(() => {
          this.fetchCoursePlans();
        })
        .catch(error => {
          console.error(error);
        });
    },
    deleteVideo(video_id, cascade) {
      axios.delete(`/api/video/${video_id}?cascade=${cascade}`)
        .then(() => {
          this.fetchVideos();
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>

<style>
.container-fluid {
  display: flex;
}

.details-page {
  flex-grow: 1;
  padding: 20px;
  margin-left: 10%; /* Sidebar width */
  background-color: #f7f8fc;
  min-height: 100vh;
  transition: margin-left 0.3s;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.query-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.query-buttons button {
  padding: 10px 20px;
  background-color: #FF4081;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.query-buttons button:hover {
  background-color: #0056b3;
}

.result {
  margin-top: 20px;
}

.result-section {
  margin-bottom: 20px;
}

h3 {
  margin-bottom: 10px;
  font-size: 1.2rem;
  color: #333;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  margin-bottom: 5px;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

li button {
  margin-left: 10px;
}
</style>
