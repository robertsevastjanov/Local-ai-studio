<script setup>
const { data, refresh } = await useFetch('/api/history')
const generations = computed(() => data.value?.generations ?? [])
</script>

<template>
  <main class="memory-page">
    <NuxtLink to="/" class="memory-switch" title="Back to Classic">
      ◀ CLASSIC
    </NuxtLink>

    <div class="memory-intro">
      <h1>✦ THE MEMORY MACHINE ✦</h1>
      <p>Local AI Studio — Experimental Interface</p>
      <span>NEURAL ARCHIVE SYSTEM / INITIALIZING...</span>
    </div>
    <RetroMonitor @generated="refresh" />
    <ArchiveGallery :generations="generations" />
  </main>
</template>

<style scoped>
.memory-page {
  min-height: 100vh;
  background:
    radial-gradient(ellipse at 50% 30%, #472476, transparent 65%),
    linear-gradient(135deg, #0b091b, #102344);
  color: #e9d5ff;
}

.memory-switch {
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 100;
  padding: 9px 13px;
  border: 1px solid #b88aff;
  border-radius: 10px;
  color: #f3e8ff;
  background: linear-gradient(180deg, #7440b8, #28154e);
  text-decoration: none;
  box-shadow: inset 0 1px #ffffff66, 0 0 15px #a855f755;
}

.memory-intro {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 15px;
  text-align: center;
  padding: 24px;
}

.memory-intro h1 {
  font-size: clamp(25px, 5vw, 56px);
  letter-spacing: 3px;
  text-shadow: 0 0 30px #a855f7;
}

.memory-intro p {
  color: #c4b5fd;
}

.memory-intro span {
  font-size: 11px;
  letter-spacing: 2px;
  color: #67e8f9;
}
</style>

<style>
/* Memory Machine: compact first screen */
.memory-page .memory-intro {
  min-height: auto;
  padding: 20px 50px 0;
  gap: 5px;
}

.memory-page .memory-intro h1 {
  margin: 0;
  font-size: clamp(20px, 3vw, 34px);
}

.memory-page .memory-intro p,
.memory-page .memory-intro span {
  margin: 0;
  font-size: 10px;
}

.memory-page .retro-computer {
  width: min(1000px, 94vw);
  margin: 15px auto 20px;
}

.memory-page .retro-screen {
  padding: 14px;
}

.memory-page .retro-screen-header {
  margin-bottom: 12px;
}

.memory-page .retro-panel {
  padding: 12px;
}

.memory-page .retro-panel h2 {
  margin-bottom: 10px;
}

.memory-page .retro-panel textarea {
  height: 95px;
}

.memory-page .retro-preview {
  min-height: 190px;
}

.memory-page .retro-status {
  margin-top: 10px;
}

@media (min-width: 701px) and (max-height: 850px) {
  .memory-page .retro-computer {
    zoom: 0.85;
  }
}

@media (min-width: 701px) and (max-height: 700px) {
  .memory-page .retro-computer {
    zoom: 0.72;
  }
}
</style>

<style>
/* Fit Memory Machine to the browser viewport */
.memory-page {
  height: 100dvh;
  min-height: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.memory-page .memory-intro {
  flex-shrink: 0;
  padding-top: 8px;
}

.memory-page .retro-computer {
  flex-shrink: 0;
  width: min(1000px, 94vw);
  margin: 8px auto;
  zoom: min(1, calc((100dvh - 115px) / 670px));
}

@media (max-width: 700px) {
  .memory-page {
    height: auto;
    min-height: 100dvh;
    overflow: visible;
  }

  .memory-page .retro-computer {
    zoom: 1;
  }
}
</style>

<style>
/* Allow scrolling when the virtual archive is added */
.memory-page {
  height: auto;
  min-height: 100dvh;
  overflow: visible;
}

.memory-page .retro-computer {
  max-width: 94vw;
}
</style>

<style>
/* Memory Machine: single-screen desktop */
@media (min-width: 701px) {
  html:has(.memory-page),
  body:has(.memory-page) {
    overflow: hidden;
  }

  .memory-page {
    height: 100dvh;
    min-height: 0;
    overflow: hidden;
    display: grid;
    grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
    grid-template-rows: auto minmax(0, 1fr);
    align-items: center;
    gap: 12px;
    padding: 24px;
  }

  .memory-page .memory-intro {
    grid-column: 1 / -1;
    min-height: 0;
    padding: 0;
  }

  .memory-page .retro-computer {
    width: 100%;
    max-width: 100%;
    margin: 0;
    zoom: 0.65;
  }

  .memory-page .archive-section {
    height: 100% !important;
    min-width: 0;
    min-height: 0;
    overflow: hidden;
  }

  .memory-page .archive-sticky {
    position: relative;
    height: 100%;
    min-height: 0;
  }

  .memory-page .archive-track {
    max-width: 100%;
    overflow-x: auto;
    transform: none !important;
    padding: 20px;
    gap: 22px;
  }

  .memory-page .archive-card {
    flex-basis: 210px;
  }

  .memory-page .archive-image-frame {
    height: 210px;
  }
}
</style>
