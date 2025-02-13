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
        /* 
        {
          title: 'The Persistence of Memory',
          artist: 'Salvador Dalí',
          museum: 'Museum of Modern Art, New York City',
          imageUrl: persistenceOfMemory,
          tags: ['Surrealism', 'Melting Clocks', 'Time'],
        },
        {
          title: 'Girl with a Pearl Earring',
          artist: 'Johannes Vermeer',
          museum: 'Mauritshuis, The Hague',
          imageUrl: girlWithPearlEarring,
          tags: ['Dutch Golden Age', 'Portrait', 'Tronie'],
        },
        {
          title: 'The Kiss',
          artist: 'Gustav Klimt',
          museum: 'Belvedere Museum, Vienna',
          imageUrl: theKiss,
          tags: ['Art Nouveau', 'Gold Leaf', 'Love'],
        },
        {
          title: 'Guernica',
          artist: 'Pablo Picasso',
          museum: 'Museo Reina Sofía, Madrid',
          imageUrl: guernica,
          tags: ['Cubism', 'Anti-War', 'Political'],
        },
        {
          title: 'The Birth of Venus',
          artist: 'Sandro Botticelli',
          museum: 'Uffizi Gallery, Florence',
          imageUrl: birthOfVenus,
          tags: ['Renaissance', 'Mythology', 'Nude'],
        },
        {
          title: 'The Night Watch',
          artist: 'Rembrandt van Rijn',
          museum: 'Rijksmuseum, Amsterdam',
          imageUrl: nightWatch,
          tags: ['Dutch Golden Age', 'Group Portrait', 'Baroque'],
        },
        {
          title: 'American Gothic',
          artist: 'Grant Wood',
          museum: 'Art Institute of Chicago',
          imageUrl: americanGothic,
          tags: ['Regionalism', 'Rural Life', 'Portrait'],
        },
        {
          title: 'The School of Athens',
          artist: 'Raphael',
          museum: 'Vatican Museums, Vatican City',
          imageUrl: schoolOfAthens,
          tags: ['Renaissance', 'Fresco', 'Philosophy'],
        },
        {
          title: 'Campbell’s Soup Cans',
          artist: 'Andy Warhol',
          museum: 'Museum of Modern Art, New York City',
          imageUrl: campbellSoupCans,
          tags: ['Pop Art', 'Consumerism', 'Repetition'],
        },
        {
          title: 'The Two Fridas',
          artist: 'Frida Kahlo',
          museum: 'Museo de Arte Moderno, Mexico City',
          imageUrl: twoFridas,
          tags: ['Surrealism', 'Identity', 'Dualism'],
        },
        {
          title: 'Water Lilies',
          artist: 'Claude Monet',
          museum: 'Musée de l’Orangerie, Paris',
          imageUrl: waterLilies,
          tags: ['Impressionism', 'Nature', 'Reflection'],
        },
        {
          title: 'The Son of Man',
          artist: 'René Magritte',
          museum: 'Private Collection',
          imageUrl: sonOfMan,
          tags: ['Surrealism', 'Identity', 'Apple'],
        },
        {
          title: 'The Creation of Adam',
          artist: 'Michelangelo',
          museum: 'Sistine Chapel, Vatican City',
          imageUrl: creationOfAdam,
          tags: ['Renaissance', 'Fresco', 'Religion'],
        },
        {
          title: 'Nighthawks',
          artist: 'Edward Hopper',
          museum: 'Art Institute of Chicago',
          imageUrl: nighthawks,
          tags: ['Realism', 'Urban Life', 'Isolation'],
        },
        {
          title: 'The Garden of Earthly Delights',
          artist: 'Hieronymus Bosch',
          museum: 'Museo del Prado, Madrid',
          imageUrl: gardenOfEarthlyDelights,
          tags: ['Northern Renaissance', 'Triptych', 'Moral'],
        },
        {
          title: 'Liberty Leading the People',
          artist: 'Eugène Delacroix',
          museum: 'Louvre Museum, Paris',
          imageUrl: libertyLeadingPeople,
          tags: ['Romanticism', 'Revolution', 'Allegory'],
        }, */
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
