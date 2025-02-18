<template>
  <div class="explore-container flex">
    <ArtCard
      v-if="currentArtwork"
      :artwork="currentArtwork"
      :isLoading="isLoading"
      @like="handleLike"
      @dislike="handleDislike"
      @info="handleInfo"
    />
    <p>Test</p>
  </div>
</template>

<script>
import ArtCard from '../../components/ArtCard.vue';
import starryNight from '../../assets/art/The_Starry_Night_Van_Gogh.jpg';

export default {
  name: 'Explore',
  components: {
    ArtCard,
  },
  data() {
    return {
      artworks: [
        {
          title: 'Loading',
          artist: 'Vincent van Gogh',
          museum: 'Museum of Modern Art, New York City',
          imageUrl: starryNight,
          tags: ['Post-Impressionism', 'Nightscape', 'Swirling patterns'],
        },
      ],
      currentIndex: 0,
      isLoading: false
    };
  },
  computed: {
    currentArtwork() {
      return this.artworks[this.currentIndex];
    },
  },
  mounted() {
    this.fetchRecommendations();
  },
  methods: {
    handleLike(artwork) {
      console.log('Liked:', this.currentArtwork?.filename);
      this.fetchAfterLikes(true);
      this.nextArtwork();
    },
    handleDislike(artwork) {
      console.log('Disliked:', this.currentArtwork?.filename);
      this.fetchAfterLikes(false);
      this.nextArtwork();
    },
    handleInfo(artwork) {
      console.log('Info requested for:', artwork.title);
      // Implement info modal or navigation
    },
    nextArtwork() {
      if (this.currentIndex < this.artworks.length - 1) {
        this.currentIndex++;
      } else {
        // Handle end of artworks
        console.log('No more artworks to show');
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
        this.artworks.push({
          title: 'Loading',
        });
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      }
    },
    async fetchAfterLikes(like) {
      this.isLoading = true;
      try {
        const params = new URLSearchParams({
          userid: 'user1',
          image: this.currentArtwork?.filename || '',
          liked: like.toString()
        });
        const response = await fetch(`http://127.0.0.1:5000/api/swipe?${params}`);
        const data = await response.json();
        if (this.currentIndex > 9) {
          this.artworks = data.recommendations;
          this.artworks.push({
            title: 'Loading',
          });
          this.currentIndex = 0;
        }
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.explore-container {
  padding: 20px;
  margin: 0;
  width: 100%;
  max-height: 100%;
  max-width: 400px;
}
</style>
