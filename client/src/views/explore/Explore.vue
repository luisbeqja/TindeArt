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
import portraitJeanne from '../../assets/art/Portrait_of_Jeanne_Modigliani.jpg';
import monaLisa from '../../assets/art/monalisa.jpg';
import theScream from '../../assets/art/the-scheam.jpg';

export default {
  name: 'Explore',
  components: {
    ArtCard,
  },
  data() {
    return {
      artworks: [
        {
          title: 'The Starry Night',
          artist: 'Vincent van Gogh',
          museum: 'Museum of Modern Art, New York City',
          imageUrl: starryNight,
          tags: ['Post-Impressionism', 'Nightscape', 'Swirling patterns'],
        },
        {
          title: 'Portrait of Jeanne',
          artist: 'Amedeo Modigliani',
          museum: 'Kunsthaus Zürich',
          imageUrl: portraitJeanne,
        },
        {
          title: 'Mona Lisa',
          artist: 'Leonardo da Vinci',
          museum: 'Louvre Museum, Paris',
          imageUrl: monaLisa,
          tags: ['Renaissance', 'Portrait', 'Sfumato'],
        },
        {
          title: 'The Scream',
          artist: 'Edvard Munch',
          museum: 'National Museum, Oslo',
          imageUrl: theScream,
          tags: ['Expressionism', 'Anxiety', 'Landscape'],
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
