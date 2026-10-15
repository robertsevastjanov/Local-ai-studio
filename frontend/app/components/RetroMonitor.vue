<script setup>
import { ref } from 'vue'

const API_URL = 'http://127.0.0.1:8000'

const prompt = ref('')
const steps = ref(10)
const seed = ref(42)
const generating = ref(false)
const generationError = ref('')
const latestImage = ref(null)

const emit = defineEmits(['generated'])

function imageUrl(path) {
  return `${API_URL}/${path}`
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
    emit('generated')
  } catch (err) {
    generationError.value =
      err?.data?.message || 'Generation failed. Check the local AI server.'
  } finally {
    generating.value = false
  }
}
</script>

<template>
  <div class="retro-computer">
    <div class="retro-monitor">
      <div class="retro-screen">
        <header class="retro-screen-header">
          <span>✦ LOCAL AI STUDIO</span>
          <span class="retro-online">● SYSTEM ONLINE</span>
        </header>

        <div class="retro-workspace">
          <section class="retro-panel">
            <h2>✧ IMAGE GENERATOR</h2>

            <form @submit.prevent="generateImage">
              <label for="retro-prompt">YOUR PROMPT</label>
              <textarea
                id="retro-prompt"
                v-model="prompt"
                maxlength="1000"
                rows="5"
                placeholder="Describe your creation..."
                :disabled="generating"
              />

              <div class="retro-settings">
                <label>
                  STEPS
                  <input v-model.number="steps" type="number" min="1" max="30" />
                </label>
                <label>
                  SEED
                  <input v-model.number="seed" type="number" min="0" />
                </label>
              </div>

              <button
                class="retro-generate"
                type="submit"
                :disabled="generating || prompt.trim().length < 10"
              >
                {{ generating ? '◌ GENERATING...' : '✦ GENERATE IMAGE' }}
              </button>

              <p v-if="generationError" class="retro-error">
                {{ generationError }}
              </p>
            </form>
          </section>

          <section class="retro-panel">
            <h2>◈ PREVIEW</h2>

            <div class="retro-preview">
              <p v-if="generating">◌ Creating your image...</p>
              <img
                v-else-if="latestImage"
                :src="imageUrl(latestImage.image_path)"
                :alt="latestImage.prompt"
              />
              <p v-else>✧ Your creation appears here</p>
            </div>
          </section>
        </div>

        <footer class="retro-status">
          <span>STABLE DIFFUSION 1.5</span>
          <span>MPS ACCELERATION</span>
        </footer>
      </div>

      <div class="retro-monitor-chin">
        <span>MEMORY MACHINE / MODEL 2005</span>
        <span class="retro-power-light"></span>
      </div>
    </div>

    <div class="retro-stand"></div>
    <div class="retro-base"></div>
  </div>
</template>

<style scoped>
.retro-computer {
  width: min(1100px, 94vw);
  margin: 60px auto 90px;
  filter: drop-shadow(0 30px 45px #0009);
}

.retro-monitor {
  padding: 20px 20px 0;
  border: 3px solid #bca0ef;
  border-radius: 32px 32px 22px 22px;
  background: linear-gradient(145deg, #b89de9, #5b438f 15%, #211c46 55%, #6956a4);
  box-shadow: inset 0 3px 4px #ffffff99, inset 0 -7px 12px #0a0826;
}

.retro-screen {
  position: relative;
  overflow: hidden;
  padding: 25px;
  border: 8px solid #0a0c1c;
  border-radius: 15px;
  color: #eee3ff;
  background: linear-gradient(145deg, #30204c, #13142d 55%, #102e4e);
  box-shadow: inset 0 0 35px #000a, 0 0 18px #b583ff55;
}

.retro-screen::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(180deg, #ffffff0c, transparent 30%, #00000010);
}

.retro-screen-header,
.retro-status {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 11px;
  letter-spacing: 2px;
}

.retro-screen-header {
  margin-bottom: 25px;
  font-weight: 800;
}

.retro-online {
  color: #70f5d5;
}

.retro-workspace {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.retro-panel {
  min-width: 0;
  padding: 20px;
  border: 1px solid #b48bff88;
  border-radius: 15px;
  background: linear-gradient(145deg, #422568, #17132d 65%, #164065);
  box-shadow: inset 0 2px 2px #ffffff33, 0 12px 25px #0005;
}

.retro-panel h2 {
  margin: 0 0 20px;
  font-size: 17px;
  letter-spacing: 1px;
}

.retro-panel label {
  display: block;
  margin-bottom: 8px;
  font-size: 11px;
  letter-spacing: 1px;
}

.retro-panel textarea,
.retro-panel input {
  width: 100%;
  padding: 12px;
  border: 1px solid #9e7ad4;
  border-radius: 8px;
  color: white;
  background: #090d23;
  font: inherit;
}

.retro-panel textarea {
  resize: vertical;
}

.retro-settings {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-top: 15px;
}

.retro-generate {
  width: 100%;
  margin-top: 15px;
  padding: 14px;
  border: 1px solid #e9baff;
  border-radius: 11px;
  color: white;
  font-weight: 800;
  cursor: pointer;
  background: linear-gradient(180deg, #d9a1ff, #a855f7 43%, #6d28d9 52%, #4338ca);
  box-shadow: inset 0 2px 2px #ffffff88, 0 5px 0 #28134d, 0 12px 25px #a855f755;
  transition: transform .2s, filter .2s;
}

.retro-generate:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.04);
  filter: brightness(1.2);
}

.retro-generate:disabled {
  opacity: .5;
  cursor: not-allowed;
}

.retro-preview {
  display: grid;
  place-items: center;
  min-height: 300px;
  border: 1px solid #7551a8;
  border-radius: 10px;
  background: #080b1d;
  text-align: center;
  color: #bca8dc;
}

.retro-preview img {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
}

.retro-status {
  margin-top: 20px;
  color: #a6d9ed;
}

.retro-monitor-chin {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 55px;
  padding: 0 25px;
  color: #d5c1f2;
  font-size: 10px;
  letter-spacing: 2px;
}

.retro-power-light {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  background: #70ffe0;
  box-shadow: 0 0 15px #70ffe0;
}

.retro-stand {
  width: 75px;
  height: 45px;
  margin: auto;
  background: linear-gradient(90deg, #251940, #8d6bbd, #251940);
}

.retro-base {
  width: 240px;
  height: 17px;
  margin: auto;
  border: 1px solid #bca0ef;
  border-radius: 50% 50% 10px 10px;
  background: linear-gradient(#9a7bd1, #241a45);
}

.retro-error {
  color: #ff9aa9;
  font-size: 12px;
}

@media (max-width: 700px) {
  .retro-computer {
    width: 98vw;
  }

  .retro-monitor {
    padding: 9px 9px 0;
  }

  .retro-screen {
    padding: 12px;
  }

  .retro-workspace {
    grid-template-columns: 1fr;
  }

  .retro-panel {
    padding: 14px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .retro-generate {
    transition: none;
  }
}
</style>
