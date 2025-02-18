<template>
  <div class="explore-container">
    <ArtCard
      v-if="currentArtwork"
      :artwork="currentArtwork"
      @like="handleLike"
      @dislike="handleDislike"
      @info="handleInfo"
    />
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
    };
  },
  computed: {
    currentArtwork() {
      return this.artworks[this.currentIndex];
    },
  },
  mounted() {
    this.fetchRecommendations()
  },
  methods: {
    handleLike(artwork) {
      console.log('Liked:', artwork.title);
      this.nextArtwork();
    },
    handleDislike(artwork) {
      console.log('Disliked:', artwork.title);
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
      try {
        const response = await fetch('http://127.0.0.1:5000/api/test/recommendations');
        const data = await response.json();
        console.log('Recommendations:', data);
        this.artworks = data.recommendations
        // TODO: Handle the recommendations data
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      }
    },
  },
};
</script>

<style scoped>
.explore-container {
  padding: 20px;
  margin: 0 auto;
  width: 100%;
  max-height: 100%;
}
</style>
