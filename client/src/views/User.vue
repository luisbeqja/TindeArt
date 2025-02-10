<template>
  <div class="min-h-screen bg-gradient-to-br from-[#0f0f0f] to-[#5457a5] p-6 w-full">
    <div class="max-w-md mx-auto bg-white rounded-3xl overflow-hidden shadow-xl p-6">
      <div class="relative">
        <div class="w-32 h-32 mx-auto rounded-full overflow-hidden border-4 border-indigo-600">
          <img
            src="https://placekitten.com/300/300"
            alt="Profile"
            class="w-full h-full object-cover"
          />
        </div>
      </div>

      <div class="text-center mt-4 pb-8">
        <h2 class="text-xl font-semibold text-gray-800">Matched Artist 21</h2>
        <div class="mt-6 px-6">
          <p class="text-gray-600">usertest@gmail.com</p>
          <p class="text-gray-600 mt-2">login with Google</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
// Mock data could be added here if needed
const userData = {
  name: 'Matched Artist 21',
  email: 'usertest@gmail.com',
  loginMethod: 'login with Google',
  profileImage: 'https://placekitten.com/300/300'
}
</script>

<style scoped>
/* Add any additional custom styles here if needed */
</style>
