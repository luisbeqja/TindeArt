<template>
  <div
    class="login-container flex flex-col items-center justify-center h-screen w-screen"
  >
    <h1 class="text-4xl font-bold">TindArt</h1>
    <div class="flex flex-col items-center justify-center gap-4 mt-7">
      <button 
        @click="signInWithGoogle" 
        class="sign-in-button"
        :disabled="authStore.isLoading"
      >
        {{ authStore.isLoading ? 'SIGNING IN...' : 'SIGN IN WITH GOOGLE' }}
      </button>
      <p v-if="authStore.error" class="text-red-500">
        {{ authStore.error }}
      </p>
    </div>
  </div>
</template>


<script setup lang="ts">
import { onMounted } from 'vue'
import { supabase } from '../utils/supabase.ts'
import { useAuthStore } from '../stores/authStore'

const authStore = useAuthStore()

// Initialize auth state when component mounts
onMounted(() => {
  authStore.initializeAuth() // Initialize auth state listeners
})

const signInWithGoogle = async () => {
  try {
    authStore.isLoading = true
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: 'http://localhost:5173' // Adjust your redirect URL
      },
    })
    
    if (error) throw error
  } catch (error) {
    authStore.error = error instanceof Error ? error.message : 'Authentication failed'
  } finally {
    authStore.isLoading = false
  }
}
</script>

<style scoped>
.login-container {
  background: linear-gradient(35deg, #0f0f0f, #5457a5);
}

.sign-in-button {
  background-color: transparent;
  color: white;
  border: 1.5px solid white;
  border-radius: 9999px;
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
  max-width: 400px;
  text-transform: uppercase;
}

.sign-in-button:hover:not(:disabled) {
  background-color: #363b5e;
}

.sign-in-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>