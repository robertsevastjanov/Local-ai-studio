<script setup>
import { computed } from 'vue'

const props = defineProps({
  progress: { type: Number, default: 0 }
})

// Deterministic positions prevent visual jumps during rendering.
const stars = computed(() =>
  Array.from({ length: 85 }, (_, i) => ({
    id: i,
    x: (i * 73.79 + 17) % 100,
    y: (i * 41.37 + 29) % 100,
    size: i % 9 === 0 ? 3 : i % 3 === 0 ? 2 : 1,
    delay: `${(i * 0.37) % 6}s`,
    duration: `${2 + (i % 5)}s`
  }))
)
</script>

<template>
  <div class="starfield" aria-hidden="true">
    <span
      v-for="star in stars"
      :key="star.id"
      class="star"
      :style="{
        left: `${((star.x - props.progress * 100) % 100 + 100) % 100}%`,
        top: `${star.y}%`,
        width: `${star.size}px`,
        height: `${star.size}px`,
        animationDelay: star.delay,
        animationDuration: star.duration
      }"
    />
  </div>
</template>

<style scoped>
.starfield {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background:
    radial-gradient(ellipse at 35% 45%, #2a1a53 0%, transparent 55%),
    radial-gradient(ellipse at 80% 20%, #112f53 0%, transparent 50%),
    #070916;
}

.star {
  position: absolute;
  border-radius: 50%;
  background: white;
  box-shadow: 0 0 5px #ffffffaa;
  animation: twinkle ease-in-out infinite alternate;
}

@keyframes twinkle {
  0% {
    opacity: .12;
    transform: scale(.7);
  }

  100% {
    opacity: 1;
    transform: scale(1.5);
  }
}

@media (prefers-reduced-motion: reduce) {
  .star {
    animation: none;
    opacity: .65;
  }
}
</style>
