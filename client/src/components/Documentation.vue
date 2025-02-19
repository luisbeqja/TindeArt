<template>
  <div class="documentation-container text-black" :class="{ 'expanded': isExpanded }">
    <div class="doc-header" @click="toggleExpand">
      <div class="title-wrapper">
        <h2 class="title text-xl font-bold">How TindeArt Works</h2>
      </div>
      <p class="expand-button" :class="{ 'p-0': isExpanded }">
        {{ isExpanded ? '◀' : '▶' }}
      </p>
    </div>

    <div class="doc-content" :class="{ 'show': isExpanded }">
      <p class="text-sm text-gray-600 mb-4">
        TindeArt uses a sophisticated recommendation system that learns your art preferences through your interactions (swipes) and provides personalized art recommendations.
      </p>

      <section class="mb-6">
        <h3 class="text-lg font-semibold mb-2">1. Image Analysis</h3>
        <p class="text-sm text-gray-600 mb-2">
          When an artwork is added to our system, we analyze it using three main feature categories:
        </p>
        <div class="feature-list">
          <div class="feature-item">
            <h4 class="font-medium">Color Features</h4>
            <ul class="list-disc ml-5 text-sm">
              <li>Extracts 5 dominant colors</li>
              <li>Calculates color proportions</li>
              <li>Measures RGB distribution</li>
            </ul>
          </div>
          <div class="feature-item">
            <h4 class="font-medium">Color Distribution</h4>
            <ul class="list-disc ml-5 text-sm">
              <li>RGB channel histograms</li>
              <li>8 bins per channel</li>
              <li>Pattern recognition</li>
            </ul>
          </div>
          <div class="feature-item">
            <h4 class="font-medium">Composition</h4>
            <ul class="list-disc ml-5 text-sm">
              <li>3x3 grid analysis</li>
              <li>Brightness mapping</li>
              <li>Contrast measurement</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="mb-6">
        <h3 class="text-lg font-semibold mb-2">2. Learning Your Preferences</h3>
        <div class="learning-stages">
          <div class="stage">
            <h4 class="font-medium">New Users (Cold Start)</h4>
            <ul class="list-disc ml-5 text-sm">
              <li>Initially uses similarity-based approach</li>
              <li>Recommends artworks with features similar to ones you've liked</li>
              <li>Uses cosine similarity to find artworks with matching characteristics</li>
            </ul>
          </div>
          <div class="stage">
            <h4 class="font-medium">Established Users</h4>
            <ul class="list-disc ml-5 text-sm">
              <li>Activates after 5+ likes/dislikes each</li>
              <li>Uses Random Forest Classifier</li>
              <li>Creates personalized preference profile</li>
              <li>Predicts preferences based on artwork features</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="mb-6">
        <h3 class="text-lg font-semibold mb-2">3. Continuous Learning</h3>
        <ul class="list-disc ml-5 text-sm">
          <li>Updates preference profile with each swipe</li>
          <li>Refines recommendations based on latest interactions</li>
          <li>Adapts to changes in your taste over time</li>
        </ul>
      </section>

      <section class="mb-6">
        <h3 class="text-lg font-semibold mb-2">4. Dataset</h3>
        <p class="text-sm text-gray-600 mb-2">
          The recommendations come from a curated collection of artworks from WikiArt, including various:
        </p>
        <ul class="list-disc ml-5 text-sm">
          <li>Artistic styles</li>
          <li>Genres</li>
          <li>Time periods</li>
          <li>Artists</li>
        </ul>
      </section>

      <div class="privacy-note text-sm text-gray-600 mt-4">
        <strong>Privacy Note:</strong> The system only stores anonymous user IDs and artwork interaction data. No personal information is required or stored.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Documentation',
  data() {
    return {
      isExpanded: false
    }
  },
  methods: {
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    }
  }
}
</script>

<style scoped>
.documentation-container {
  background: white;
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);    
  width: 50px;
  transition: width 0.3s ease-in-out;
  overflow: hidden;
  position: relative;
}

.documentation-container.expanded {
  width: 100%;
}

.doc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  position: relative;
  height: 32px;
}

.title-wrapper {
  position: absolute;
  white-space: nowrap;
  transition: transform 0.3s ease-in-out;
  transform: translateX(-100%);
  opacity: 0;
}

.expanded .title-wrapper {
  transform: translateX(0);
  opacity: 1;
}

.title {
  font-size: 20px;
  font-weight: bold;
}

.expand-button {
  background: none;
  border: none;
  font-size: 20px;
  color: #666;
  cursor: pointer;
  transition: color 0.3s ease;
  margin-left: auto;
}

.expand-button:hover {
  color: #4b9eff;
}

.doc-content {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
  transition: all 0s ease-in-out;
  overflow: scroll;
  height: 78vh;
}

.doc-content.show {
  opacity: 1;
  max-height: 2000px;
  margin-top: 16px;
  transition: all 0.3s ease-in-out;
}

.feature-list, .learning-stages {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 8px;
}

.feature-item, .stage {
  background: rgba(0, 0, 0, 0.02);
  padding: 12px;
  border-radius: 8px;
}

.privacy-note {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding-top: 12px;
}

@media (max-width: 768px) {
  .feature-list, .learning-stages {
    grid-template-columns: 1fr;
  }
}
</style> 