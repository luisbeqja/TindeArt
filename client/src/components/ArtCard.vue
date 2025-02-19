<template>
  <div class="art-card-container">
    <div
      class="art-card"
      :style="{ transform: `translateX(${offset}px) rotate(${rotation}deg)` }"
    >
      <div class="art-image-container">
        <img :src="imgUrl" :alt="artwork.title" class="art-image" />
        <div class="art-info">
          <h2>{{ artist }}</h2>
          <p>{{ gener }}</p>
        </div>
      </div>
      <div class="action-buttons">
        <button class="action-button dislike" @click="handleDislike" :disabled="isLoading">
          <span class="icon">✕</span>
        </button>
        <button class="action-button info" @click="handleInfo" :disabled="isLoading">
          <span class="icon">i</span>
        </button>
        <button class="action-button like" @click="handleLike" :disabled="isLoading">
          <span class="icon">♥</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import dataset from './dataset.json';

export default {
  name: 'ArtCard',
  props: {
    artwork: {
      type: Object,
      required: true,
      default: () => ({
        title: '',
        artist: '',
        museum: '',
        imageUrl: '',
      }),
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      offset: 0,
      rotation: 0,
      isDragging: false,
      startX: 0,
    };
  },
  methods: {
    handleLike() {
      this.animateSwipe(1);
      this.$emit('like', this.artwork);
    },
    handleDislike() {
      this.animateSwipe(-1);
      this.$emit('dislike', this.artwork);
    },
    handleInfo() {
      this.$emit('info', this.artwork);
    },
    animateSwipe(direction) {
      this.offset = direction * 600;
      this.rotation = direction * 20;
      setTimeout(() => {
        this.offset = 0;
        this.rotation = 0;
      }, 300);
    },
  },
  computed: {
    gener() {
      return dataset?.features?.genre?.names[Number(this.artwork.genre)]
    },
    artist() {
      return dataset?.features?.artist?.names[Number(this.artwork.genre)]
    },
    imgUrl() {
      return `/wikiart_images/${this.artwork.filename}`
    }
  }
};
</script>

<style scoped>
.art-card-container {
  width: 100%;
  margin: 0 ;
  position: relative;
  max-width: 400px;
  z-index: 20;
}

.art-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.art-image-container {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 200%; /* Adjust this value to match your desired aspect ratio */
}

.art-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.art-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
}

.art-info h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
}

.art-info p {
  margin: 4px 0;
  font-size: 16px;
}

.action-buttons {
  display: flex;
  justify-content: space-around;
  padding: 16px;
  background: white;
}

.action-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.action-button:hover {
  transform: scale(1.1);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.action-button:disabled:hover {
  transform: none;
}

.action-button.dislike {
  background: #ff4b4b;
  color: white;
}

.action-button.info {
  background: #4b9eff;
  color: white;
}

.action-button.like {
  background: #4bff4b;
  color: white;
}

.icon {
  font-size: 24px;
}
</style>
