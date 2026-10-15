<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const props = defineProps({
  generations: {
    type: Array,
    default: () => []
  }
})

const API_URL = 'http://127.0.0.1:8000'
const section = ref(null)
const track = ref(null)
const offset = ref(0)
const maxOffset = ref(0)
const selectedImage = ref(null)

const images = computed(() => props.generations.slice(0, 500))

function imageUrl(path) {
  return `${API_URL}/${path}`
}

function updateScroll() {
  if (!section.value || !track.value) return

  const viewportWidth = section.value.clientWidth
  const contentWidth = track.value.scrollWidth

  maxOffset.value = Math.max(0, contentWidth - viewportWidth)

  const scrollDistance = Math.max(
    0,
    section.value.offsetHeight - window.innerHeight
  )

  const progress = scrollDistance > 0
    ? Math.min(1, Math.max(0,
        (window.scrollY + window.innerHeight -
         section.value.getBoundingClientRect().bottom -
         window.scrollY + scrollDistance) / scrollDistance
      ))
    : 0

  offset.value = progress * maxOffset.value
}

function handleScroll() {
  if (!section.value) return

  const rect = section.value.getBoundingClientRect()
  const distance = section.value.offsetHeight - window.innerHeight

  const progress = distance > 0
    ? Math.min(1, Math.max(0, -rect.top / distance))
    : 0

  offset.value = progress * maxOffset.value
}

let resizeObserver

onMounted(() => {
  resizeObserver = new ResizeObserver(() => {
    updateScroll()
    handleScroll()
  })

  if (track.value) resizeObserver.observe(track.value)

  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', updateScroll)

  updateScroll()
  handleScroll()
})

onUnmounted(() => {
  resizeObserver?.disconnect()
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', updateScroll)
})
</script>

<template>
  <section
    ref="section"
    class="archive-section"
    :style="{
      height: images.length
        ? `calc(100dvh + ${maxOffset}px)`
        : '100dvh'
    }"
  >
    <div class="archive-sticky">
      <header class="archive-header">
        <div>
          <span class="archive-eyebrow">NEURAL MEMORY STORAGE</span>
          <h2>THE VIRTUAL ARCHIVE</h2>
        </div>
        <span class="archive-count">{{ images.length }} MEMORIES</span>
      </header>

      <div v-if="!images.length" class="archive-empty">
        NO MEMORIES FOUND — GENERATE YOUR FIRST IMAGE
      </div>

      <div
        v-else
        ref="track"
        class="archive-track"
        :style="{ transform: `translate3d(${-offset}px, 0, 0)` }"
      >
        <article
          v-for="(image, index) in images"
          :key="image.id"
          class="archive-card"
          :style="{ '--tilt': `${index % 2 ? 2 : -2}deg` }"
          @click="selectedImage = image"
        >
          <div class="archive-image-frame">
            <img
              :src="imageUrl(image.image_path)"
              :alt="image.prompt"
              loading="lazy"
            />
          </div>
          <div class="archive-card-info">
            <span>MEMORY_{{ String(index + 1).padStart(4, '0') }}</span>
            <p>{{ image.prompt }}</p>
          </div>
        </article>
      </div>

      <div class="archive-hint">↓ SCROLL TO TRAVEL THROUGH MEMORIES →</div>
    </div>
  </section>

  <div
    v-if="selectedImage"
    class="archive-modal"
    role="dialog"
    aria-modal="true"
    @click.self="selectedImage = null"
  >
    <button
      class="archive-close"
      aria-label="Close preview"
      @click="selectedImage = null"
    >✕</button>
    <img
      :src="imageUrl(selectedImage.image_path)"
      :alt="selectedImage.prompt"
    />
  </div>
</template>

<style scoped>
.archive-section {
  position: relative;
  background:
    radial-gradient(ellipse at center, #38205d 0%, transparent 65%),
    linear-gradient(120deg, #090a1c, #101d37);
}

.archive-sticky {
  position: sticky;
  top: 0;
  height: 100dvh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.archive-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 6vw;
  color: #e9d5ff;
}

.archive-eyebrow,
.archive-count,
.archive-hint {
  color: #67e8f9;
  font-size: 11px;
  letter-spacing: 3px;
}

.archive-header h2 {
  margin: 8px 0 0;
  font-size: clamp(24px, 4vw, 48px);
  text-shadow: 0 0 25px #a855f7;
}

.archive-track {
  display: flex;
  align-items: center;
  gap: 55px;
  width: max-content;
  padding: 40px 8vw;
  will-change: transform;
}

.archive-card {
  flex: 0 0 280px;
  padding: 12px;
  border: 2px solid #d5b4fa;
  border-radius: 20px;
  background: linear-gradient(135deg, #c8a7ee, #4a3678 20%, #161a3b 75%, #8266b2);
  box-shadow:
    inset 0 2px 3px #ffffffaa,
    0 20px 35px #0009,
    0 0 25px #a855f744;
  transform: perspective(900px) rotateY(var(--tilt));
  transition: transform .3s, box-shadow .3s;
  cursor: pointer;
}

.archive-card:hover {
  transform: perspective(900px) rotateY(0deg) translateY(-15px) scale(1.05);
  box-shadow: 0 30px 50px #000a, 0 0 35px #c084fc99;
}

.archive-image-frame {
  height: 280px;
  overflow: hidden;
  border: 5px solid #11152d;
  border-radius: 12px;
  background: #080b1c;
}

.archive-image-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.archive-card-info {
  padding: 14px 5px 5px;
  color: #e9d5ff;
}

.archive-card-info span {
  color: #67e8f9;
  font-size: 10px;
  letter-spacing: 2px;
}

.archive-card-info p {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  font-size: 12px;
  line-height: 1.5;
}

.archive-hint {
  padding: 20px;
  text-align: center;
}

.archive-empty {
  padding: 40px;
  color: #c4b5fd;
  text-align: center;
}

.archive-modal {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: grid;
  place-items: center;
  padding: 50px;
  background: #03040cef;
}

.archive-modal img {
  max-width: 90vw;
  max-height: 85vh;
  object-fit: contain;
}

.archive-close {
  position: absolute;
  top: 25px;
  right: 30px;
  border: 0;
  color: white;
  background: transparent;
  font-size: 30px;
  cursor: pointer;
}

@media (max-width: 700px) {
  .archive-card {
    flex-basis: 220px;
  }

  .archive-image-frame {
    height: 220px;
  }

  .archive-header {
    padding: 20px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .archive-card {
    transition: none;
  }
}
</style>
