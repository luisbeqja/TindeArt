<script setup lang="ts">
import Login from './views/Login.vue'
import User from './views/User.vue'
</script>

<template>
  <div class="flex flex-col items-center justify-center h-screen w-screen">
    <Login />
    <!-- <User /> -->
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
