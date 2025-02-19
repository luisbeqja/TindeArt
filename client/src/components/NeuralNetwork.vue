<template>
  <div class="neural-network" :class="{ 'is-learning': isLearning }">
    <div class="layers-container">
      <svg class="connections" width="100%" height="100%">
        <g
          v-for="(fromLayer, layerIndex) in ['output', 'hidden2', 'hidden1']"
          :key="layerIndex"
        >
          <path
            v-for="(_, fromIndex) in getLayerSize(fromLayer)"
            :key="fromIndex"
            :class="{
              active:
                isLearning && activeNeurons[fromLayer].includes(fromIndex + 1),
            }"
            :d="getConnectionPaths(fromLayer, fromIndex)"
            class="connection-line"
          />
        </g>
      </svg>

      <!-- Output Layer (top) -->
      <div class="layer output-layer">
        <div
          v-for="i in 2"
          :key="'output-' + i"
          class="neuron"
          :class="{ active: isLearning && activeNeurons.output.includes(i) }"
        ></div>
      </div>

      <!-- Hidden Layer 2 -->
      <div class="layer hidden-layer">
        <div
          v-for="i in 4"
          :key="'hidden2-' + i"
          class="neuron"
          :class="{ active: isLearning && activeNeurons.hidden2.includes(i) }"
        ></div>
      </div>

      <!-- Hidden Layer 1 -->
      <div class="layer hidden-layer">
        <div
          v-for="i in 6"
          :key="'hidden1-' + i"
          class="neuron"
          :class="{ active: isLearning && activeNeurons.hidden1.includes(i) }"
        ></div>
      </div>

      <!-- Input Layer (bottom) -->
      <div class="layer input-layer">
        <div
          v-for="i in 8"
          :key="'input-' + i"
          class="neuron"
          :class="{ active: isLearning && activeNeurons.input.includes(i) }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NeuralNetwork',
  props: {
    isLearning: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      activeNeurons: {
        input: [],
        hidden1: [],
        hidden2: [],
        output: [],
      },
      animationInterval: null,
      layerSizes: {
        output: 2,
        hidden2: 4,
        hidden1: 6,
        input: 8,
      },
    };
  },
  methods: {
    getLayerSize(layer) {
      return Array(this.layerSizes[layer]).fill(0);
    },
    getPreviousLayer(layer) {
      const layers = ['output', 'hidden2', 'hidden1', 'input'];
      const currentIndex = layers.indexOf(layer);
      return layers[currentIndex + 1];
    },
    getConnectionPaths(fromLayer, fromIndex) {
      const prevLayer = this.getPreviousLayer(fromLayer);
      if (!prevLayer) return '';

      const paths = [];
      const prevLayerSize = this.layerSizes[prevLayer];

      for (let toIndex = 0; toIndex < prevLayerSize; toIndex++) {
        const x1 =
          (fromLayer === 'output'
            ? 25
            : fromLayer === 'hidden2'
            ? 41.6
            : 58.3) + '%';
        const x2 =
          (fromLayer === 'output'
            ? 41.6
            : fromLayer === 'hidden2'
            ? 58.3
            : 75) + '%';
        const y1 =
          ((fromIndex + 1) * 100) / (this.layerSizes[fromLayer] + 1) + '%';
        const y2 =
          ((toIndex + 1) * 100) / (this.layerSizes[prevLayer] + 1) + '%';

        paths.push(`M ${x1} ${y1} C ${x2} ${y1}, ${x1} ${y2}, ${x2} ${y2}`);
      }

      return paths.join(' ');
    },
    startAnimation() {
      this.animationInterval = setInterval(() => {
        this.activeNeurons.output = this.getRandomNeurons(2, 1);
        this.activeNeurons.hidden2 = this.getRandomNeurons(4, 2);
        this.activeNeurons.hidden1 = this.getRandomNeurons(6, 3);
        this.activeNeurons.input = this.getRandomNeurons(8, 4);
      }, 500);
    },
    stopAnimation() {
      clearInterval(this.animationInterval);
      this.activeNeurons = {
        input: [],
        hidden1: [],
        hidden2: [],
        output: [],
      };
    },
    getRandomNeurons(total, count) {
      const neurons = [];
      while (neurons.length < count) {
        const n = Math.floor(Math.random() * total) + 1;
        if (!neurons.includes(n)) {
          neurons.push(n);
        }
      }
      return neurons;
    },
  },
  watch: {
    isLearning(newVal) {
      if (newVal) {
        this.startAnimation();
      } else {
        this.stopAnimation();
      }
    },
  },
  beforeUnmount() {
    this.stopAnimation();
  },
};
</script>

<style scoped>
.neural-network {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  padding: 15px;
  position: relative;
  z-index: 10;
}

.layers-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  max-width: 400px;
  height: 100%;
  position: relative;
  margin: 0 auto;
  padding: 20px 0;
}

.layer-labels {
  position: absolute;
  right: 10px;
  top: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 0;
  font-size: 12px;
  color: #666;
}

.connections {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.connection-line {
  fill: none;
  stroke: #ddd;
  stroke-width: 1;
  opacity: 0.3;
  transition: all 0.3s ease;
}

.connection-line.active {
  stroke: #4b9eff;
  stroke-width: 2;
  opacity: 0.6;
}

.layer {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 12px;
  z-index: 1;
  position: relative;
}

.neuron {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ddd;
  transition: all 0.3s ease;
  position: relative;
}

.neuron.active {
  background: #4b9eff;
  box-shadow: 0 0 10px #4b9eff;
}

.neuron.active::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(75, 158, 255, 0.3);
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.is-learning .connection-line.active {
  animation: flow 1s infinite;
}

@keyframes flow {
  0% {
    stroke-dasharray: 5;
    stroke-dashoffset: 0;
  }
  100% {
    stroke-dasharray: 5;
    stroke-dashoffset: -10;
  }
}
</style>
