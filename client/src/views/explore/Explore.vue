<template>
  <div class="explore-container flex justify-start gap-4">
    <ArtCard
      v-if="currentArtwork"
      :artwork="currentArtwork"
      :isLoading="isLoading"
      @like="handleLike"
      @dislike="handleDislike"
      @info="handleInfo"
    />
    <div class="neural-network-container">
      <h3 class="text-lg font-semibold mb-2 text-gray-800">
        AI Learning Progress
      </h3>
      <NeuralNetwork :isLearning="isLoading" />
      <div class="stats mt-4">
        <p class="text-xl text-gray-800">{{ userEmail }}</p>
        <p class="text-sm text-gray-600">
          Liked: {{ userPreferences.liked.length }} artworks
        </p>
        <p class="text-sm text-gray-600">
          Disliked: {{ userPreferences.disliked.length }} artworks
        </p>
      </div>
    </div>
    <Documentation />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { supabase } from '../../utils/supabase';
import ArtCard from '../../components/ArtCard.vue';
import NeuralNetwork from '../../components/NeuralNetwork.vue';
import Documentation from '../../components/Documentation.vue';

export default {
  name: 'Explore',
  components: {
    ArtCard,
    NeuralNetwork,
    Documentation,
  },
  data() {
    return {
      user: null,
      artworks: [
        {
          title: 'Loading',
          artist: 'Vincent van Gogh',
          museum: 'Museum of Modern Art, New York City',
          imageUrl: '',
          tags: ['Post-Impressionism', 'Nightscape', 'Swirling patterns'],
        },
      ],
      currentIndex: 0,
      isLoading: false,
      userPreferences: {
        liked: [],
        disliked: [],
      },
    };
  },
  computed: {
    currentArtwork() {
      return this.artworks[this.currentIndex];
    },
    userEmail() {
      return this.user?.email || 'Guest';
    },
  },
  async mounted() {
    await this.fetchUserData();
    this.fetchRecommendations();
    this.fetchUserPreferences();
  },
  methods: {
    async fetchUserData() {
      try {
        const {
          data: { user },
        } = await supabase.auth.getUser();
        this.user = user;
        console.log('User data fetched:', user?.email);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    handleLike(artwork) {
      this.userPreferences.liked.push(this.currentArtwork?.filename);
      this.fetchAfterLikes(true);
      this.nextArtwork();
    },
    handleDislike(artwork) {
      this.userPreferences.disliked.push(this.currentArtwork?.filename);
      this.fetchAfterLikes(false);
      this.nextArtwork();
    },
    handleInfo(artwork) {
      console.log('Info requested for:', artwork.title);
    },
    nextArtwork() {
      if (this.currentIndex < this.artworks.length - 1) {
        this.currentIndex++;
      } else {
        console.log('No more artworks to show');
      }
    },
    async fetchUserPreferences() {
      try {
        const response = await fetch(
          'http://127.0.0.1:5000/api/user_preferences'
        );
        const data = await response.json();
        this.userPreferences = data[this.user?.id] || {
          liked: [],
          disliked: [],
        };
      } catch (error) {
        console.error('Error fetching user preferences:', error);
      }
    },
    async fetchRecommendations() {
      console.log('Fetching recommendations');
      try {
        const response = await fetch(
          'http://127.0.0.1:5000/api/recommendations'
        );
        const data = await response.json();
        this.artworks = data.recommendations;
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      }
    },
    async fetchAfterLikes(like) {
      this.isLoading = true;
      try {
        const params = new URLSearchParams({
          userid: this.user?.id || 'user1',
          image: this.currentArtwork?.filename || '',
          liked: like.toString(),
        });
        const response = await fetch(
          `http://127.0.0.1:5000/api/swipe?${params}`
        );
        const data = await response.json();
        if (data.recommendations && this.currentIndex > 8) {
          this.artworks = data.recommendations;
          this.currentIndex = 0;
        }
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setTimeout(() => {
          this.isLoading = false;
        }, 1000);
      }
    },
  },
};
</script>

<style scoped>
.explore-container {
  padding: 20px;
  width: 100%;
}

.neural-network-container {
  flex: 1;
  min-width: 400px;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 400px;
}

.stats {
  padding: 10px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}
</style>
