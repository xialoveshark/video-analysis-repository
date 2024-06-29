<template>
    <div class="modal-overlay">
      <div class="modal1" style="background: white;">
        <h2>添加成功</h2>
        <p>您的课程已成功添加。</p>
        <button @click="closeModal">关闭</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      closeModal() {
        this.$emit('close'); // 发送关闭事件给父组件
      }
    }
  };
  </script>
  
  <style scoped>
  /* 样式可以根据需要进行调整 */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal1 {
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }
  </style>