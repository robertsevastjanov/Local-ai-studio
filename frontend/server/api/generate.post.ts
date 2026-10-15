// Nuxt server API endpoint: POST /api/generate
export default defineEventHandler(async (event) => {
  // Read generation settings sent from the Nuxt interface.
  const body = await readBody(event)

  // Forward the request to the local FastAPI backend.
  const result = await $fetch('http://127.0.0.1:8000/generate', {
    method: 'POST',
    body: {
      prompt: body.prompt,
      steps: body.steps,
      seed: body.seed
    }
  })

  // Return the generated image information to Nuxt.
  return result
})
