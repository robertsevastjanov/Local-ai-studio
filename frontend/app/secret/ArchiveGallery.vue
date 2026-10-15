<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const props = defineProps({
  generations: {
    type: Array,
    default: () => []
  },
  scrollProgress: {
    type: Number,
    default: null
  }
})

const API_URL = 'http://127.0.0.1:8000'
const section = ref(null)
const track = ref(null)
const offset = ref(0)
const maxOffset = ref(0)
const selectedImage = ref(null)
const glitchId = ref(null)
let glitchTimer = null
let glitchClearTimer = null

function scheduleGlitch() {
  clearTimeout(glitchTimer)
  glitchTimer = setTimeout(() => {
    const visible = [...(track.value?.querySelectorAll('.archive-card') ?? [])]
      .filter(element => {
        const rect = element.getBoundingClientRect()
        return rect.width > 0 && rect.height > 0 &&
          rect.left < window.innerWidth && rect.right > 0 &&
          rect.top < window.innerHeight && rect.bottom > 0 &&
          !element.classList.contains('archive-card-taken-off')
      })
    if (visible.length) {
      const element = visible[Math.floor(Math.random() * visible.length)]
      glitchId.value = element.dataset.imageId
      clearTimeout(glitchClearTimer)
      glitchClearTimer = setTimeout(() => { glitchId.value = null }, 1000)
    }
    scheduleGlitch()
  }, 60000)
}

const images = computed(() => props.generations.slice(0, 500))

function imageUrl(path) {
  return `${API_URL}/${path}`
}

function formatDate(value) {
  if (!value) return 'Date unavailable'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return 'Date unavailable'
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
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

// External camera control takes priority over vertical page scrolling.
const effectiveOffset = computed(() => {
  if (props.scrollProgress === null) return offset.value

  const progress = Math.max(0, Math.min(1, props.scrollProgress))
  return progress * maxOffset.value
})

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
  scheduleGlitch()
})

onUnmounted(() => {
  resizeObserver?.disconnect()
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', updateScroll)
  clearTimeout(glitchTimer)
  clearTimeout(glitchClearTimer)
})

// SECRET_SCENE_RETRY_V1: irregular columns, original card styling untouched.
const memoryStacks = [2,2,3,2,2,2,4,2,3,2,2]
function memoryPlacement(index) {
  let col=0, remaining=index
  while (remaining >= memoryStacks[col % memoryStacks.length]) {
    remaining -= memoryStacks[col % memoryStacks.length]; col++
  }
  const n=memoryStacks[col % memoryStacks.length]
  const span=12/n
  return { gridColumn: String(col+1), gridRow: `${remaining*span+1} / span ${span}` }
}

// MEMORY_CONSTELLATIONS_V2: gently stagger each memory, preserving its card design.
const constellationOffsets = [
  [-12,-34],[19,42],[8,35],[-20,-25],[15,-56],[-14,18],
  [22,49],[-12,-36],[15,13],[-22,38],[13,-24],[-9,51],
  [21,-12],[-18,-42],[8,29],[-10,9],[22,-52],[-16,43],
  [10,-31],[-24,16],[17,48],[-7,-18],[24,-41],[-15,31]
]
function constellationStyle(index) {
  const [x,y] = constellationOffsets[index % constellationOffsets.length]
  return { marginLeft: `${x}px`, marginTop: `${y}px`, '--constellation-x': `${x}px` }
}
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
        :style="{ transform: `translate3d(${-effectiveOffset}px, 0, 0)` }"
      >
        <svg class="archive-backbone-cables" viewBox="0 0 1000 400" preserveAspectRatio="none" aria-hidden="true">
          <defs>
            <linearGradient id="secret-cable-violet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ead4ff"/><stop offset=".4" stop-color="#7c3dbd"/><stop offset="1" stop-color="#170c37"/></linearGradient>
            <linearGradient id="secret-cable-cyan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b7ffff"/><stop offset=".45" stop-color="#218cba"/><stop offset="1" stop-color="#091d41"/></linearGradient>
          </defs>
          <path d="M0 210 C95 240 125 130 240 175 S420 300 535 215 S770 115 1000 205" stroke="url(#secret-cable-violet)" stroke-width="7"/>
          <path d="M0 225 C100 260 170 175 275 235 S440 125 585 190 S820 290 1000 170" stroke="url(#secret-cable-cyan)" stroke-width="5"/>
          <path d="M0 235 C115 205 155 315 300 265 S500 310 655 235 S850 185 1000 255" stroke="#ad83cf" stroke-width="3"/>
        </svg>
        <article
          v-for="(image, index) in images"
          :key="image.id"
          class="archive-card"
          :class="{ 'archive-card-glitch': String(glitchId) === String(image.id) }"
          :data-image-id="image.id"
          :style="{ ...memoryPlacement(index), ...constellationStyle(index), '--tilt': `${index % 2 ? 2 : -2}deg` }"
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
            <span class="archive-date">{{ formatDate(image.created_at) }}</span>
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
    <div class="archive-modal-caption">
      <strong>{{ selectedImage.prompt }}</strong>
      <span>{{ formatDate(selectedImage.created_at) }}</span>
    </div>
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
  display: none;
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
  position: relative;
  display: grid;
  grid-auto-flow: column;
  grid-template-rows: repeat(2, minmax(0, 1fr));
  grid-auto-columns: 250px;
  align-items: center;
  align-content: center;
  gap: 22px 8px;
  width: max-content;
  height: calc(100dvh - 220px);
  min-height: 0;
  padding: 12px 8vw;
  will-change: transform;
}

.archive-card {
  position: relative;
  width: 100%;
  align-self: center;
  padding: 10px;
  border: 2px solid #d9b5ff;
  border-radius: 20px;
  background:
    linear-gradient(145deg, #d7bbff 0%, #7756a9 9%, #27234e 35%, #11152e 72%, #9870cf 100%);
  box-shadow:
    inset 0 3px 4px #ffffffaa,
    inset 0 -8px 15px #09091e99,
    0 5px 0 #39235f,
    0 12px 24px #0009,
    0 0 20px #a855f755;
  transform: perspective(1000px) rotateY(var(--tilt)) translateZ(0);
  transform-style: preserve-3d;
  transition:
    transform .35s cubic-bezier(.2,.8,.2,1),
    box-shadow .35s,
    border-color .35s;
  cursor: pointer;
  animation: memory-float 5s ease-in-out infinite;
  isolation: isolate;
  left: var(--landed-x, 0px);
  top: var(--landed-y, 0px);
}

.archive-card:nth-child(2n + 1) {
  grid-row: 1;
  scale: .88;
  animation-delay: -1.7s;
}

.archive-card:nth-child(2n) {
  grid-row: 2;
  scale: 1;
  animation-delay: -3.1s;
}

@keyframes memory-float {
  0%, 100% { translate: 0 0; }
  50% { translate: 0 -10px; }
}


/* Three long, shaded cables behind every image; move with the track. */
.archive-backbone-cables {
  position: absolute;
  width: calc(100% + 90vw);
  height: 100%;
  left: -90vw;
  top: 0;
  overflow: visible;
  pointer-events: none;
  fill: none;
  stroke-linecap: round;
  filter: drop-shadow(0 4px 3px #000b) drop-shadow(0 0 3px #ba80ff66);
  z-index: 0;
}
.archive-card { z-index: 1; }

.archive-image-frame,
.archive-card-info {
  position: relative;
  z-index: 1;
}

.archive-card-taken-off {
  visibility: hidden !important;
  opacity: 0 !important;
}

/* Brief analog signal interference. */
.archive-card-glitch {
  animation:
    memory-glitch .12s steps(2, end) 8,
    memory-float 5s ease-in-out infinite !important;
  border-color: #67e8f9 !important;
  filter: saturate(2) contrast(1.25);
}

.archive-card-glitch .archive-image-frame {
  position: relative;
}

.archive-card-glitch .archive-image-frame img {
  animation: image-glitch .16s steps(2, end) 6;
}

@keyframes memory-glitch {
  0% { translate: 0 0; }
  25% { translate: -4px 1px; }
  50% { translate: 3px -1px; }
  75% { translate: -2px 2px; }
  100% { translate: 0 0; }
}

@keyframes image-glitch {
  0% { filter: hue-rotate(0deg); transform: translateX(0); }
  25% { filter: hue-rotate(90deg) saturate(2); transform: translateX(-3px); }
  50% { filter: invert(.15); transform: translateX(3px); }
  100% { filter: none; transform: translateX(0); }
}

.archive-card:hover,
.archive-card:focus-within {
  z-index: 100;
  transform: perspective(1000px) rotateY(0deg) translateY(-12px) translateZ(45px) scale(1.06);
  border-color: #f1ddff;
  box-shadow:
    inset 0 3px 5px #ffffffcc,
    0 8px 0 #39235f,
    0 30px 55px #000c,
    0 0 22px #c084fc,
    0 0 55px #8b5cf688;
}

.archive-date {
  display: block;
  max-height: 0;
  margin-top: 0;
  overflow: hidden;
  opacity: 0;
  color: #a5f3fc;
  font-size: 11px;
  transition: opacity .2s, max-height .2s, margin-top .2s;
}

.archive-card:hover .archive-date,
.archive-card:focus-within .archive-date {
  max-height: 32px;
  margin-top: 9px;
  opacity: 1;
}

.archive-image-frame {
  height: 170px;
  overflow: hidden;
  border: 5px solid #11152d;
  border-radius: 12px;
  background: #080b1c;
  box-shadow:
    inset 0 0 0 1px #bda0f755,
    0 4px 0 #08091a,
    0 8px 18px #0008;
  transform: translateZ(12px);
}

.archive-card:nth-child(4n) .archive-image-frame {
  height: 190px;
}

.archive-card:nth-child(5n) .archive-image-frame {
  height: 145px;
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
  display: none;
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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 32px;
  background: #03040cf2;
  backdrop-filter: blur(18px);
}

.archive-modal img {
  display: block;
  width: auto !important;
  height: auto !important;
  max-width: calc(100vw - 64px);
  max-height: calc(100dvh - 64px);
  object-fit: contain;
  object-position: center;
  border-radius: 8px;
}


.archive-modal-caption {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: min(800px, 90vw);
  color: #f3e8ff;
  text-align: center;
  text-shadow: 0 0 16px #a855f766;
}

.archive-modal-caption strong {
  font-size: 15px;
  overflow-wrap: anywhere;
}

.archive-modal-caption span {
  color: #67e8f9;
  font-size: 12px;
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
    height: 160px;
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
/* CONSISTENT_FIX_V1: original card appearance, irregular grouping only. */
.archive-track {
  grid-template-rows:repeat(12,minmax(0,1fr));
  grid-auto-columns:250px;
  column-gap:32px;
  row-gap:0;
  height:calc(100dvh - 150px);
  overflow:visible;
}
.archive-card:nth-child(n) {grid-row:auto;}
.archive-card {align-self:center;overflow:visible;}
.archive-card:hover,.archive-card:focus-within {
  position:relative;z-index:999999 !important;
  scale:1 !important;
  transform:perspective(1000px) rotateY(0deg) translateY(-12px) translateZ(45px) scale(1.06) !important;
}
.archive-backbone-cables {display:none !important;}

/* SOFT_PANORAMA_EDGE_V1 */
.archive-section,.archive-sticky,.archive-track {background:transparent !important;}

</style>