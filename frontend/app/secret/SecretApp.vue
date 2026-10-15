<script setup>
import RetroMonitor from './RetroMonitor.vue'
import ArchiveGallery from './ArchiveGallery.vue'
import Starfield from './Starfield.vue'
import { onMounted, ref, computed, onUnmounted } from 'vue'

const { data, refresh } = await useFetch('/api/history')
const generations = computed(() => data.value?.generations ?? [])
const powerPhase = ref('on')
let powerTimerA = null
let powerTimerB = null
function toggleMachinePower() {
  if (powerPhase.value === 'off') {
    powerPhase.value = 'boot'
    powerTimerA = setTimeout(() => {
      powerPhase.value = 'glitch-on'
      powerTimerB = setTimeout(() => { powerPhase.value = 'on' }, 250)
    }, 2000)
  } else if (powerPhase.value === 'on') {
    powerPhase.value = 'glitch-off'
    powerTimerA = setTimeout(() => { powerPhase.value = 'off' }, 500)
  }
}

const monitorZone = ref(null)
const monitorScale = ref(1)
let monitorResizeObserver = null

function updateMonitorScale() {
  const zone = monitorZone.value
  const computer = zone?.querySelector('.retro-computer')

  if (!zone || !computer) return

  const width = computer.offsetWidth
  const height = computer.offsetHeight

  if (!width || !height) return

  monitorScale.value = Math.min(
    1.2,
    zone.clientWidth * 0.95 / width,
    zone.clientHeight * 0.88 / height
  )
}

// Camera position: 0 = computer, 1 = archive.
const cameraPosition = ref(0)
const targetPosition = ref(0)
let animationFrame = null

// First half approaches the archive; the second travels through it.
const archiveProgress = computed(() =>
  Math.max(0, Math.min(1, (cameraPosition.value - 0.5) * 2))
)

function animateCamera() {
  const difference = targetPosition.value - cameraPosition.value

  if (Math.abs(difference) < 0.0005) {
    cameraPosition.value = targetPosition.value
    animationFrame = null
    return
  }

  cameraPosition.value += difference * 0.075
  animationFrame = requestAnimationFrame(animateCamera)
}

function handleWheel(event) {
  if (event.target.closest('textarea, input, select, button')) return

  if (event.cancelable) event.preventDefault()

  const delta = event.deltaY || event.deltaX

  // Travel quickly enough to reach the archive,
  // then slow down to explore individual memories.
  const sensitivity = targetPosition.value < 0.5 ? 1800 : 72000

  targetPosition.value = Math.max(
    0,
    Math.min(1, targetPosition.value + delta / sensitivity)
  )

  if (animationFrame === null) {
    animationFrame = requestAnimationFrame(animateCamera)
  }
}

const idleCard = ref(null)
const idlePosition = ref({ x: 100, y: 100, angle: 0 })

let idleTimer = null
let idleFrame = null
let idleOriginElement = null
let idleFlying = false
let idleLandedCard = null
let idleX = 100
let idleY = 100
let idleVX = 2.7
let idleVY = 2.1

const idleCardWidth = 200
const idleCardHeight = 275

function idleImageUrl(path) {
  return `http://127.0.0.1:8000/${path}`
}

function idleDate(value) {
  if (!value) return 'MEMORY RESTORED'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return 'MEMORY RESTORED'
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function stopIdleFlight() {
  if (idleFrame !== null) {
    cancelAnimationFrame(idleFrame)
    idleFrame = null
  }

  idleOriginElement?.classList.remove('archive-card-taken-off')
  idleOriginElement = null
  idleFlying = false
  idleCard.value = null
}

function animateIdleCard() {
  if (!idleCard.value) {
    idleFrame = null
    return
  }

  const maxX = Math.max(0, window.innerWidth - idleCardWidth)
  const maxY = Math.max(0, window.innerHeight - idleCardHeight)

  idleX += idleVX
  idleY += idleVY

  if (idleX <= 0) {
    idleX = 0
    idleVX = Math.abs(idleVX)
  } else if (idleX >= maxX) {
    idleX = maxX
    idleVX = -Math.abs(idleVX)
  }

  if (idleY <= 0) {
    idleY = 0
    idleVY = Math.abs(idleVY)
  } else if (idleY >= maxY) {
    idleY = maxY
    idleVY = -Math.abs(idleVY)
  }

  idlePosition.value = {
    x: idleX,
    y: idleY,
    angle: Math.sin((idleX + idleY) / 180) * 3
  }

  idleFrame = requestAnimationFrame(animateIdleCard)
}

function startIdleFlight() {
  const cards = [...document.querySelectorAll('.archive-card')]
    .map(element => ({
      element,
      rect: element.getBoundingClientRect(),
      id: element.dataset.imageId
    }))
    .filter(({ rect }) =>
      rect.width > 0 &&
      rect.height > 0 &&
      rect.right > 0 &&
      rect.left < window.innerWidth &&
      rect.bottom > 0 &&
      rect.top < window.innerHeight
    )

  if (!cards.length) return

  const origin = cards[Math.floor(Math.random() * cards.length)]
  const chosen = generations.value.find(
    item => String(item.id) === String(origin.id) && item.image_path
  )
  if (!chosen) return

  // Keep previously landed memories where they landed.
  if (idleLandedCard && idleLandedCard !== origin.element) idleLandedCard = null
  idleOriginElement = origin.element
  idleOriginElement.classList.add('archive-card-taken-off')
  idleFlying = true
  idleCard.value = { ...chosen }

  const maxX = Math.max(0, window.innerWidth - idleCardWidth)
  const maxY = Math.max(0, window.innerHeight - idleCardHeight)

  // Start centered over the actual card, then fly freely across the viewport.
  idleX = Math.max(0, Math.min(maxX,
    origin.rect.left + (origin.rect.width - idleCardWidth) / 2))
  idleY = Math.max(0, Math.min(maxY,
    origin.rect.top + (origin.rect.height - idleCardHeight) / 2))

  idleVX = (Math.random() < 0.5 ? -1 : 1) * (2.0 + Math.random() * 0.6)
  idleVY = (Math.random() < 0.5 ? -1 : 1) * (1.7 + Math.random() * 0.6)

  idlePosition.value = { x: idleX, y: idleY, angle: 0 }
  idleFrame = requestAnimationFrame(animateIdleCard)
}

function landIdleCard() {
  if (!idleCard.value || !idleOriginElement || !idleFlying) return
  if (idleFrame !== null) cancelAnimationFrame(idleFrame)
  idleFrame = null
  idleFlying = false

  const element = idleOriginElement
  const rect = element.getBoundingClientRect()
  const oldX = parseFloat(element.style.getPropertyValue('--landed-x')) || 0
  const oldY = parseFloat(element.style.getPropertyValue('--landed-y')) || 0
  const dx = idleX + idleCardWidth / 2 - (rect.left + rect.width / 2)
  const dy = idleY + idleCardHeight / 2 - (rect.top + rect.height / 2)
  element.style.setProperty('--landed-x', `${oldX + dx}px`)
  element.style.setProperty('--landed-y', `${oldY + dy}px`)
  element.classList.remove('archive-card-taken-off')
  idleLandedCard = element
  idleOriginElement = null
  idleCard.value = null
}

function resetIdleTimer() {
  clearTimeout(idleTimer)
  if (idleFlying) landIdleCard()
  idleTimer = setTimeout(startIdleFlight, 30000)
}

onMounted(() => {
  updateMonitorScale()

  monitorResizeObserver = new ResizeObserver(updateMonitorScale)

  if (monitorZone.value) {
    monitorResizeObserver.observe(monitorZone.value)
  }

  const computer = monitorZone.value?.querySelector('.retro-computer')
  if (computer) monitorResizeObserver.observe(computer)

  for (const event of ['mousemove', 'mousedown', 'keydown', 'wheel', 'touchstart', 'pointerdown']) {
    window.addEventListener(event, resetIdleTimer, { passive: true })
  }

  resetIdleTimer()
})

onUnmounted(() => {
  if (animationFrame !== null) cancelAnimationFrame(animationFrame)
  monitorResizeObserver?.disconnect()

  clearTimeout(idleTimer)
  clearTimeout(powerTimerA)
  clearTimeout(powerTimerB)
  stopIdleFlight()

  for (const event of ['mousemove', 'mousedown', 'keydown', 'wheel', 'touchstart', 'pointerdown']) {
    window.removeEventListener(event, resetIdleTimer)
  }
})
</script>

<template>
  <main class="secret-app" :class="{ 'memory-power-off': powerPhase !== 'on' }" @wheel="handleWheel">
    <Starfield :progress="cameraPosition" />
    <div class="secret-content">
    <NuxtLink
      to="/"
      class="secret-back"
      aria-label="Return to Classic"
    >
      ◀ CLASSIC
    </NuxtLink>

    <div
      class="secret-horizontal-scene"
      :style="{ transform: `translateX(${-Math.min(cameraPosition * 2, 1) * 50}%)` }"
    >

      <svg class="secret-cable-extension" viewBox="0 0 2000 1000" preserveAspectRatio="none" aria-hidden="true">
        <defs>
          <linearGradient id="wire-purple-v2" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#f3c5ff"/><stop offset=".25" stop-color="#8543b3"/><stop offset="1" stop-color="#100b2b"/></linearGradient>
          <linearGradient id="wire-blue-v2" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#b3f6ff"/><stop offset=".3" stop-color="#347bc1"/><stop offset="1" stop-color="#09142e"/></linearGradient>
        </defs>
        <path d="M740 430 C810 480 870 525 990 465 S1150 380 1310 470 S1600 550 2000 445" stroke="#070716" stroke-width="12"/>
        <path d="M740 430 C810 480 870 525 990 465 S1150 380 1310 470 S1600 550 2000 445" stroke="url(#wire-purple-v2)" stroke-width="7"/>
        <path d="M740 468 C830 515 880 540 1010 495 S1180 450 1350 535 S1720 490 2000 545" stroke="#060915" stroke-width="11"/>
        <path d="M740 468 C830 515 880 540 1010 495 S1180 450 1350 535 S1720 490 2000 545" stroke="url(#wire-blue-v2)" stroke-width="6"/>
        <path d="M740 503 C850 530 920 600 1040 530 S1270 545 1430 600 S1740 555 2000 630" stroke="#080713" stroke-width="9"/>
        <path d="M740 503 C850 530 920 600 1040 530 S1270 545 1430 600 S1740 555 2000 630" stroke="url(#wire-purple-v2)" stroke-width="5"/>
      </svg>
      <section ref="monitorZone" class="secret-monitor-zone" :style="{ '--monitor-scale': monitorScale }">
        <div class="secret-desk" aria-hidden="true"><div class="secret-desk-top"></div><div class="secret-desk-front"></div><div class="secret-desk-leg secret-desk-leg-left"></div><div class="secret-desk-leg secret-desk-leg-right"></div></div>
        <RetroMonitor :power-phase="powerPhase" @toggle-power="toggleMachinePower" @generated="refresh" />
      </section>

      <section class="secret-archive-zone">
        <ArchiveGallery :generations="generations" :scroll-progress="archiveProgress" />
      </section>
    </div>
    <div
      v-if="idleCard"
      class="idle-memory-card"
      :style="{
        left: `${idlePosition.x}px`,
        top: `${idlePosition.y}px`,
        transform: `rotate(${idlePosition.angle}deg)`
      }"
      aria-hidden="true"
    >
      <img :src="idleImageUrl(idleCard.image_path)" alt="" />
      <div class="idle-memory-info">
        <span>✦ MEMORY IN MOTION</span>
        <strong>{{ idleCard.prompt }}</strong>
        <small>{{ idleDate(idleCard.created_at) }}</small>
      </div>
    </div>
    </div>
  </main>
</template>

<style scoped>
.secret-app {
  min-height: 100dvh;
  color: #e9d5ff;
  background:
    radial-gradient(ellipse at 40% 30%, #493078, transparent 65%),
    linear-gradient(135deg, #0b091b, #102344);
}

.secret-content {
  position: relative;
  z-index: 1;
}


.secret-app {
  height: 100dvh;
  min-height: 0;
  overflow: hidden;
}

.secret-content {
  height: 100%;
}

.secret-horizontal-scene {
  display: flex;
  width: 200vw;
  height: 100%;
  will-change: transform;
}

.secret-monitor-zone,
.secret-archive-zone {
  flex: 0 0 100vw;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* Glossy three-dimensional desk behind the monitor. */
.secret-monitor-zone { position: relative; perspective: 1100px; }
.secret-desk { position: absolute; width: min(95vw, 1120px); height: 24%; bottom: 4%; left: 50%; transform: translateX(-50%); pointer-events: none; filter: drop-shadow(0 25px 30px #000b); }
.secret-desk-top { position: absolute; inset: 0 0 43%; border-radius: 12px; background: linear-gradient(155deg,#9b79c4 0%,#4c326c 18%,#171329 55%,#42315b 100%); border: 2px solid #bda0df; transform: perspective(650px) rotateX(64deg); box-shadow: inset 0 3px 5px #ffffff70, 0 14px 30px #000a; }
.secret-desk-front { position: absolute; top: 44%; width: 100%; height: 24%; border-radius: 2px 2px 9px 9px; background: linear-gradient(#6c5088,#261a3d 45%,#120d24); border-bottom: 3px solid #090714; box-shadow: inset 0 2px 2px #d9b4ff66; }
.secret-desk-leg { position: absolute; top: 65%; width: 8%; height: 35%; background: linear-gradient(90deg,#100d20,#58406e 35%,#1b142e 80%); }
.secret-desk-leg-left { left: 5%; transform: skewX(6deg); }
.secret-desk-leg-right { right: 5%; transform: skewX(-6deg); }
.secret-monitor-zone :deep(.retro-computer) {
  width: 1000px;
  flex-shrink: 0;
  margin: 0;
  zoom: 1;
  scale: var(--monitor-scale, 1);
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 24px 15px #000b) drop-shadow(12px 8px 12px #130d32);
}

.secret-archive-zone :deep(.archive-section) {
  width: 100%;
  height: 100% !important;
  background: transparent;
}

.secret-archive-zone :deep(.archive-sticky) {
  height: 100%;
}

.secret-back {
  position: fixed;
  top: 12px;
  left: 12px;
  z-index: 1000;
  padding: 8px 12px;
  border: 1px solid #b88aff;
  border-radius: 10px;
  color: #f3e8ff;
  background: linear-gradient(180deg, #7440b8, #28154e);
  text-decoration: none;
}

/* Idle screensaver: a real memory card bouncing through the scene. */
.idle-memory-card {
  position: fixed;
  z-index: 800;
  box-sizing: border-box;
  width: 200px;
  height: 275px;
  padding: 8px;
  border: 2px solid #d9b5ff;
  border-radius: 15px;
  background: linear-gradient(145deg, #b89de9, #34265e 35%, #10152e 80%, #8762ba);
  box-shadow:
    inset 0 2px 4px #ffffffbb,
    inset 0 -5px 10px #07091c,
    0 7px 0 #30204d,
    0 15px 30px #000c,
    0 0 25px #a855f799;
  pointer-events: none;
  overflow: hidden;
  will-change: left, top, transform;
}

.idle-memory-card img {
  display: block;
  width: 100%;
  height: 155px;
  object-fit: cover;
  border: 4px solid #11152d;
  border-radius: 8px;
  box-shadow: 0 4px 10px #0009;
}

.idle-memory-info {
  display: flex;
  flex-direction: column;
  gap: 7px;
  padding: 10px 4px 5px;
  color: #f3e8ff;
}

.idle-memory-info span {
  color: #67e8f9;
  font-size: 9px;
  letter-spacing: 1.5px;
}

.idle-memory-info strong {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  font-size: 12px;
  line-height: 1.4;
}

.idle-memory-info small {
  color: #c4b5fd;
  font-size: 10px;
}

@media (prefers-reduced-motion: reduce) {
  .idle-memory-card {
    transition: none;
  }
}
/* The separate CSS desk is replaced by the integrated illustrated chassis. */
.secret-monitor-zone .secret-desk {display:none !important;}
.secret-monitor-zone :deep(.retro-computer) {width:min(1400px,99vw);filter:none;}

/* SECRET_CABLE_EXTENSION_V2: behind cards, aligned to artwork ports */
.secret-horizontal-scene { position: relative; isolation: isolate; }
.secret-cable-extension {
  position: absolute; inset: 0; width: 100%; height: 100%;
  pointer-events: none; fill: none; z-index: 0;
  stroke-linecap: round; filter: drop-shadow(0 3px 4px #000c);
}
.secret-monitor-zone, .secret-archive-zone { position: relative; z-index: 1; }
.secret-archive-zone :deep(.archive-backbone-cables) { display: none !important; }

/* Keep memory cards in space, but black out their content while the machine is off. */
.memory-power-off .secret-archive-zone :deep(.archive-image-frame) { background: #000 !important; }
.memory-power-off .secret-archive-zone :deep(.archive-image-frame img),
.memory-power-off .secret-archive-zone :deep(.archive-card-info) { visibility: hidden !important; }
.memory-power-off .idle-memory-card img,
.memory-power-off .idle-memory-info { visibility: hidden !important; }
/* CONSISTENT_FIX_V1: the artwork's bottom is always below the viewport.
   Transform origin keeps the legs below the frame even at unusual aspect ratios. */
.secret-monitor-zone :deep(.retro-computer) {
  position:absolute !important;
  left:50% !important;
  bottom:-10dvh !important;
  margin:0 !important;
  transform:translateX(-50%) !important;
  transform-origin:center bottom !important;
  scale:calc(var(--monitor-scale,1) * 1.12) !important;
  translate:none !important;
}
/* Hide the old disconnected artificial paths, no foreground cable overlays. */
.secret-cable-extension {opacity:0 !important;pointer-events:none !important;}
.secret-archive-zone :deep(.archive-backbone-cables) {display:none !important;}
.secret-archive-zone :deep(.archive-card:hover),
.secret-archive-zone :deep(.archive-card:focus-within) {z-index:99999 !important;}


/* PANORAMA_ALIGNMENT_V2: only one physical panorama, carried by the monitor element. */
.secret-horizontal-scene {position:relative !important; isolation:isolate; overflow:visible !important;}
.secret-horizontal-scene::before {content:none !important;display:none !important;background:none !important;}
.secret-monitor-zone {position:relative !important; overflow:visible !important; display:block !important; perspective:none !important; z-index:1 !important;}
.secret-monitor-zone :deep(.retro-computer) {position:absolute !important;left:0 !important;top:0 !important;width:170vw !important;height:auto !important;margin:0 !important;max-width:none !important;scale:1 !important;translate:none !important;transform:none !important;zoom:1 !important;filter:none !important;z-index:1 !important;pointer-events:none !important;}
.secret-monitor-zone :deep(.retro-screen),.secret-monitor-zone :deep(.retro-screen *),.secret-monitor-zone :deep(.memory-power-switch) {pointer-events:auto !important;}
.secret-archive-zone {position:relative !important;z-index:2 !important;background:transparent !important;}
.secret-cable-extension,.secret-archive-zone :deep(.archive-backbone-cables) {display:none !important;opacity:0 !important;}
.secret-archive-zone :deep(.archive-card:hover),.secret-archive-zone :deep(.archive-card:focus-within) {transform:translateY(-5px) scale(1.045) !important;z-index:99999 !important;}


/* CENTER_POWER_V1: center the actual monitor on the first viewport.
   Keep art and HTML overlay in the SAME translated element. */
.secret-monitor-zone :deep(.retro-computer) {
  left:6.3vw !important;
  pointer-events:auto !important;
}
.secret-monitor-zone :deep(.machine-visual) {pointer-events:auto !important;}
.secret-monitor-zone :deep(.memory-power-switch) {pointer-events:auto !important;z-index:999 !important;}


/* SOFT_PANORAMA_EDGE_V1 */
/* Archive section should not paint a second rectangular sky over the shared starfield. */
.secret-archive-zone {background:transparent !important;}
.secret-archive-zone :deep(.archive-section),
.secret-archive-zone :deep(.archive-sticky),
.secret-archive-zone :deep(.archive-track) {background:transparent !important;}

</style>