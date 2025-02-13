<script setup lang="ts">
import { onMounted } from 'vue';
import { supabase } from './utils/supabase';
import router from './router';

onMounted(async () => {
  // Handle OAuth callback
  const { data: { session } } = await supabase.auth.getSession()
  const { error } = await supabase.auth.getUser()
  
  if (!error && session) {
    // Remove token from URL
    window.location.hash = ''
    
    // Only redirect if there's a specific redirect_uri query parameter
    const redirectUri = router.currentRoute.value.query.redirect_uri as string
    if (redirectUri) {
      router.push(redirectUri)
    }
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
