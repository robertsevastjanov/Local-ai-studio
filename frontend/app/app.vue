<script setup>
import { computed, ref } from 'vue'

const API_URL = 'http://127.0.0.1:8000'

const prompt = ref('')
const steps = ref(10)
const seed = ref(42)

const generating = ref(false)
const generationError = ref('')
const latestImage = ref(null)
const selectedImage = ref(null)
const failedImages = ref([])

// Load generation history from our Nuxt API endpoint.
const { data, pending, error, refresh } = await useFetch('/api/history')
// Handle images that cannot be loaded (e.g. HTTP 404).
// Store IDs of images that failed to load.
const generations = computed(() => data.value?.generations ?? [])

function imageUrl(path) {
  return `${API_URL}/${path}`
}

// Mark an image as unavailable when loading fails.
function handleImageError(id) {
  console.log('IMAGE ERROR HANDLER CALLED:', id)

  if (!failedImages.value.includes(id)) {
    failedImages.value.push(id)
  }
}

async function generateImage() {
  if (generating.value || prompt.value.trim().length < 10) return

  generating.value = true
  generationError.value = ''
  latestImage.value = null

  try {
    const result = await $fetch('/api/generate', {
      method: 'POST',
      body: {
        prompt: prompt.value.trim(),
        steps: Number(steps.value),
        seed: Number(seed.value)
      }
    })

    latestImage.value = result
    await refresh()
  } catch (err) {
    generationError.value =
      err?.data?.message || 'Generation failed. Please check the local AI server.'
  } finally {
    generating.value = false
  }
}
</script>

<template>
  <div class="studio">
    <NuxtRouteAnnouncer />

    <header class="topbar">
      <div class="brand">
        <span class="brand-icon">✦</span>
        <span>LOCAL AI STUDIO</span>
      </div>
      <span class="local-label">● LOCAL GENERATION</span>
    </header>

    <main class="container">
      <section class="hero">
        <div class="eyebrow">YOUR PRIVATE CREATIVE WORKSPACE</div>
        <h1>Create without limits<span class="accent">.</span></h1>
        <p>
          Generate images using AI running locally on your computer.
          Your prompts and images stay on your device.
        </p>
      </section>

      <section class="workspace">
        <div class="panel generator-panel">
          <div class="section-heading">
            <span class="section-icon">✧</span>
            <h2>Image Generator</h2>
          </div>

          <form @submit.prevent="generateImage">
            <label for="prompt">YOUR PROMPT</label>

            <textarea
              id="prompt"
              v-model="prompt"
              maxlength="1000"
              placeholder="Describe the image you want to create..."
              rows="6"
              :disabled="generating"
            />

            <div class="prompt-footer">
              <span>Minimum 10 characters</span>
              <span>{{ prompt.length }} / 1000</span>
            </div>

            <div class="settings">
              <div class="setting">
                <label for="steps">STEPS</label>
                <input
                  id="steps"
                  v-model.number="steps"
                  type="number"
                  min="1"
                  max="30"
                  :disabled="generating"
                />
              </div>

              <div class="setting">
                <label for="seed">SEED</label>
                <input
                  id="seed"
                  v-model.number="seed"
                  type="number"
                  min="0"
                  :disabled="generating"
                />
              </div>
            </div>

            <button
              class="generate-button"
              type="submit"
              :disabled="generating || prompt.trim().length < 10"
            >
              <span v-if="generating" class="spinner"></span>
              <span v-else>✦</span>
              {{ generating ? 'Generating...' : 'Generate Image' }}
            </button>

            <p v-if="generationError" class="error-message">
              {{ generationError }}
            </p>
          </form>
        </div>

        <div class="panel preview-panel">
          <div class="section-heading">
            <span class="section-icon">◈</span>
            <h2>Preview</h2>
          </div>

          <div class="preview-area">
            <div v-if="generating" class="preview-placeholder">
              <div class="large-spinner"></div>
              <h3>Creating your image</h3>
              <p>Stable Diffusion is working locally...</p>
            </div>

            <img
              v-else-if="latestImage"
              :src="imageUrl(latestImage.image_path)"
              :alt="latestImage.prompt"
              class="preview-image"
              @click="selectedImage = latestImage"
            />

            <div v-else class="preview-placeholder">
              <div class="placeholder-symbol">✧</div>
              <h3>Your creation appears here</h3>
              <p>Enter a prompt and start generating.</p>
            </div>
          </div>
        </div>
      </section>

      <section class="gallery-section">
        <div class="gallery-heading">
          <div>
            <div class="eyebrow">YOUR CREATIONS</div>
            <h2>Generation Gallery</h2>
          </div>
          <span v-if="data" class="image-counter">
            Images generated: {{ data.count }}
          </span>
        </div>

        <p class="storage-notice">
          Only your latest 500 generated images will be displayed in the gallery.
          All images are saved locally in the
          <code>images/</code> folder and are never automatically deleted.
          Older images remain available there.
        </p>

        <p v-if="pending">Loading generation history...</p>
        <p v-else-if="error" class="error-message">
          Failed to load generation history.
        </p>

        <div v-else class="gallery-grid">
          <article
            v-for="generation in generations"
            :key="generation.id"
            class="image-card"
          >
            <div class="image-container">
              <ClientOnly>
                <div
                  v-if="failedImages.includes(generation.id)"
                  class="unavailable"
                >
                  Image unavailable
                </div>

                <img
                  v-else
                  :src="imageUrl(generation.image_path)"
                  :alt="generation.prompt"
                  loading="lazy"
                  @error="handleImageError(generation.id)"
                  @click="selectedImage = generation"
                />
              </ClientOnly>
            </div>

            <div class="card-content">
              <h3 :title="generation.prompt">
                {{ generation.prompt }}
              </h3>
              <div class="card-meta">
                <span>{{ generation.steps }} steps</span>
                <span>Seed {{ generation.seed }}</span>
              </div>
            </div>
          </article>
        </div>
      </section>
    </main>

    <div
      v-if="selectedImage"
      class="modal-overlay"
      @click.self="selectedImage = null"
    >
      <div class="modal">
        <button
          class="close-button"
          aria-label="Close image"
          @click="selectedImage = null"
        >
          ×
        </button>

        <img
          :src="imageUrl(selectedImage.image_path)"
          :alt="selectedImage.prompt"
        />

        <div class="modal-info">
          <h3>{{ selectedImage.prompt }}</h3>
          <p>
            Steps: {{ selectedImage.steps }}
            · Seed: {{ selectedImage.seed }}
          </p>
          <p v-if="selectedImage.created_at">
            {{ selectedImage.created_at }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

