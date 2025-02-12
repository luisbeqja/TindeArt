<template>
  <div class="min-h-screen bg-gradient-to-br from-[#0f0f0f] to-[#5457a5] p-6 w-full">
    <div v-if="authStore.user" class="max-w-md mx-auto bg-white rounded-3xl overflow-hidden shadow-xl p-6">
      <div class="relative">
        <div class="w-32 h-32 mx-auto rounded-full overflow-hidden border-4 border-indigo-600">
          <img
            :src="authStore.user.user_metadata?.avatar_url || 'https://placekitten.com/300/300'"
            alt="Profile"
            class="w-full h-full object-cover"
          />
        </div>
      </div>

      <div class="text-center mt-4 pb-8">
        <h2 class="text-xl font-semibold text-gray-800">
          {{ authStore.user.user_metadata?.full_name || 'Anonymous User' }}
        </h2>
        <div class="mt-6 px-6">
          <p class="text-gray-600">{{ authStore.user.email }}</p>
          <p class="text-sm text-gray-500 mt-2">
            Logged in via {{ authStore.user.app_metadata?.provider || 'unknown method' }}
          </p>
        </div>
      </div>
    </div>

    <div v-else class="text-center text-white mt-20">
      <p class="text-xl">No user logged in</p>
      <router-link 
        to="/login" 
        class="mt-4 inline-block px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
      >
        Go to Login
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const authStore = useAuthStore()
const router = useRouter()

// Initialize auth state when component mounts
onMounted(async () => {
  await authStore.initializeAuth()
  
  // Redirect to login if not authenticated
  if (!authStore.isAuthenticated) {
    router.push('/login')
  }
})
</script>

<style scoped>
/* Add any additional custom styles here if needed */
</style>