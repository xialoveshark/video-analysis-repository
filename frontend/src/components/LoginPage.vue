<template>
  <div class="current-page" :style="{ backgroundImage: backgroundImage }">
    <div class="col-md-6" style="width:60%">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card mt-5">
            <div class="card-body">
              <div v-if="!isRegistering">
                <h2 class="text-center">登录</h2>
                <form @submit.prevent="login">
                  <div class="mb-3">
                    <label for="loginUsername" class="form-label">用户名:</label>
                    <input type="text" id="loginUsername" class="form-control" v-model="loginUsername" required>
                  </div>
                  <div class="mb-3">
                    <label for="loginPassword" class="form-label">密码:</label>
                    <input type="password" id="loginPassword" class="form-control" v-model="loginPassword" required>
                  </div>
                  <button type="submit" class="btn btn-primary w-100">登录</button>
                </form>
                <p v-if="loginError" class="text-danger text-center mt-3">{{ loginError }}</p>
                <button @click="toggleRegistration" class="btn btn-link mt-3">还没有账号？点击注册</button>
              </div>
              <div v-else>
                <h2 class="text-center">注册</h2>
                <form @submit.prevent="register">
                  <div class="mb-3">
                    <label for="registerUsername" class="form-label">用户名:</label>
                    <input type="text" id="registerUsername" class="form-control" v-model="registerUsername" required>
                  </div>
                  <div class="mb-3">
                    <label for="registerPassword" class="form-label">密码:</label>
                    <input type="password" id="registerPassword" class="form-control" v-model="registerPassword" required>
                  </div>
                  <div class="mb-3">
                    <label for="confirmPassword" class="form-label">确认密码:</label>
                    <input type="password" id="confirmPassword" class="form-control" v-model="confirmPassword" required>
                  </div>
                  <div class="mb-3">
                    <label for="university" class="form-label">学校:</label>
                    <input type="text" id="university" class="form-control" v-model="university" required>
                  </div>
                  <div class="mb-3">
                    <label for="department" class="form-label">部门:</label>
                    <input type="text" id="department" class="form-control" v-model="department" required>
                  </div>
                  <button type="submit" class="btn btn-primary w-100">注册</button>
                </form>
                <p v-if="registerError" class="text-danger text-center mt-3">{{ registerError }}</p>
                <button @click="toggleRegistration" class="btn btn-link mt-3">返回登录</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isRegistering: false,
      loginUsername: '',
      loginPassword: '',
      registerUsername: '',
      registerPassword: '',
      confirmPassword: '',
      university: '',
      department: '',
      loginError: '',
      registerError: '',
      backgroundImages: ['loginImg/1.jpg', 'loginImg/2.jpg', 'loginImg/3.jpg'],
      currentBackgroundIndex: 0,
      backgroundImage: ''
    };
  },
  created() {
    setInterval(this.nextBackground, 3000); // 5000毫秒（5秒）切换一次背景图片
    this.backgroundImage = `url('${this.backgroundImages[this.currentBackgroundIndex]}')`;
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/login', {
          username: this.loginUsername,
          password: this.loginPassword
        });
        const { account_id } = response.data;
        sessionStorage.setItem('userId', account_id);  // 存储用户 ID
        this.loginError = '';
        this.$router.push('/dashboard');
        alert('登录成功！');
      } catch (error) {
        if (error.response && error.response.data) {
          this.loginError = error.response.data.message;
        } else {
          this.loginError = '登录失败，请稍后再试。';
        }
      }
    },
    async register() {
      if (this.registerPassword !== this.confirmPassword) {
        this.registerError = '两次输入的密码不一致';
        return;
      }

      try {
        await axios.post('/api/register', {
          username: this.registerUsername,
          password: this.registerPassword,
          university: this.university,
          department: this.department
        });
        this.registerError = '';
        alert('注册成功！');
        this.toggleRegistration();
      } catch (error) {
        if (error.response && error.response.data) {
          this.registerError = error.response.data.message;
        } else {
          this.registerError = '注册失败，请稍后再试。';
        }
      }
    },
    toggleRegistration() {
      this.isRegistering = !this.isRegistering;
      this.loginUsername = '';
      this.loginPassword = '';
      this.registerUsername = '';
      this.registerPassword = '';
      this.confirmPassword = '';
      this.university = '';
      this.department = '';
      this.loginError = '';
      this.registerError = '';
    },
    nextBackground() {
      this.currentBackgroundIndex = (this.currentBackgroundIndex + 1) % this.backgroundImages.length;
      this.backgroundImage = `url('${this.backgroundImages[this.currentBackgroundIndex]}')`;
    }
  }
};
</script>

<style>
.current-page {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  transition: background-image 1s ease-in-out;
}
</style>
