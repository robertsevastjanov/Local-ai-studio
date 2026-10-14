<script setup>
// Load generation history from our Nuxt API endpoint.
const { data, pending, error } = await useFetch('/api/history')
// Handle images that cannot be loaded (e.g. HTTP 404).
// Store IDs of images that failed to load.
const failedImages = ref([])

// Mark an image as unavailable when loading fails.
function handleImageError(id) {
  console.log('IMAGE ERROR HANDLER CALLED:', id)

  if (!failedImages.value.includes(id)) {
    failedImages.value.push(id)
  }
}
</script>

<template>
  <main>
    <NuxtRouteAnnouncer />

    <h1>Local AI Studio</h1>
    <p>AI Image Generation & QA Automation Project</p>

    <h2>Generation Gallery</h2>

    <!-- Show a message while the API request is running. -->
    <p v-if="pending">Loading generation history...</p>

    <!-- Show an error if the API request fails. -->
    <p v-else-if="error">Failed to load generation history.</p>

    <!-- Show data when the request succeeds. -->
    <div v-else-if="data">
      <p>Images generated: {{ data.count }}</p>

      <!-- Render one entry for each generation. -->
      <div
        v-for="generation in data.generations"
        :key="generation.id"
      >
        <h3>{{ generation.prompt }}</h3>
        <ClientOnly>
          <p v-if="failedImages.includes(generation.id)">
            Image unavailable
          </p>

          <img
            v-else
            :src="'http://127.0.0.1:8000/' + generation.image_path"
            :alt="generation.prompt"
            width="256"
            height="256"
            @error="handleImageError(generation.id)"
          />
        </ClientOnly>

        <p>Steps: {{ generation.steps }}</p>
        <p>Seed: {{ generation.seed }}</p>
        <p>Created: {{ generation.created_at }}</p>

        <hr />
      </div>
    </div>
  </main>
</template>