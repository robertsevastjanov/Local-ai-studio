// Nuxt server API endpoint: GET /api/history
export default defineEventHandler(async () => {

  // Request generation history from Python FastAPI backend.
  const history = await $fetch('http://127.0.0.1:8000/history')

  // Return the received JSON to the Nuxt frontend.
  return history
})