<script setup lang="ts">
import { onMounted } from 'vue';
import Login from './views/Login.vue'
import User from './views/User.vue'
import { supabase } from './utils/supabase';
import router from './router';

onMounted(async () => {
  // Handle OAuth callback
  const { data: { session } } = await supabase.auth.getSession()
  const { error } = await supabase.auth.getUser()
  
  if (!error) {
    // Remove token from URL
    window.location.hash = ''
    
    // Redirect to protected route
    const returnPath = (router.currentRoute.value.query.redirect_uri as string) || '/profile'
    router.push(returnPath)
  }
})

</script>

<template>
  <div class="flex flex-col items-center justify-center h-screen w-screen">
    <router-view />
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
