<template>
  <div
    class="login-container flex flex-col items-center justify-center h-screen w-screen"
  >
    <h1 class="text-4xl font-bold">TindArt</h1>
    <div class="flex flex-col items-center justify-center gap-4 mt-7">
      <button @click="signInWithGoogle" class="sign-in-button">
        SIGN IN WITH GOOGLE
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { supabase } from '../utils/supabase.ts'

// Google Login
const signInWithGoogle = async () => {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: 'http://localhost:5173' // Adjust your redirect URL
    }
  })
  if (error) console.error('Google login error:', error)
}

</script>

<style scoped>
.login-container {
  background: linear-gradient(35deg, #0f0f0f, #5457a5);
}

.sign-in-button {
  background-color: transparent; /* Dark blue/purple color from the image */
  color: white;
  border: 1.5px solid white;
  border-radius: 9999px; /* Fully rounded corners */
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;
  max-width: 400px;
  text-transform: uppercase;
}

.sign-in-button:hover {
  background-color: #363b5e; /* Slightly lighter on hover */
}
</style>
