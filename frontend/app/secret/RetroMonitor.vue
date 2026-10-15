<script setup>
import { ref } from 'vue'
const props = defineProps({ powerPhase: { type: String, default: 'on' } })

const API_URL = 'http://127.0.0.1:8000'

const prompt = ref('')
const steps = ref(10)
const seed = ref(42)
const generating = ref(false)
const generationError = ref('')
const latestImage = ref(null)

const emit = defineEmits(['generated', 'toggle-power'])

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
    <div class="machine-visual" :class="'machine-phase-' + powerPhase">
      <i class="painted-led-cover monitor-upper" aria-hidden="true"></i>
      <i class="painted-led-cover monitor-lower" aria-hidden="true"></i>
      <i class="painted-led-cover computer-led" aria-hidden="true"></i>
      <button type="button" class="memory-power-switch" :class="'power-' + powerPhase" :aria-label="powerPhase === 'off' ? 'Turn computer on' : 'Turn computer off'" :disabled="powerPhase !== 'on' && powerPhase !== 'off'" @click="emit('toggle-power')"></button>
      <div v-if="powerPhase !== 'on'" class="memory-power-overlay" :class="'phase-' + powerPhase" aria-live="polite">
        <div v-if="powerPhase === 'boot'" class="memory-boot-spinner"></div>
        <span v-if="powerPhase === 'boot'">MEMORY MACHINE / BOOTING...</span>
      </div>
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

@media (prefers-reduced-motion: reduce) {
  .retro-generate {
    transition: none;
  }
}

/* The working Vue UI sits inside one illustrated computer-and-desk chassis. */
.machine-visual { position:relative; width:100%; aspect-ratio:1703/923; background:url('/secret/memory-machine.png') center / 100% 100% no-repeat; filter:drop-shadow(0 24px 30px #0008); }
.machine-visual .retro-monitor { position:absolute; left:22.8%; top:12.7%; width:49%; height:49%; padding:0; border:0; border-radius:0; background:transparent; box-shadow:none; }
.machine-visual .retro-screen { box-sizing:border-box; height:100%; padding:2.2%; overflow:hidden; border:0; border-radius:7px; background:linear-gradient(130deg,#211634,#0b1025 60%,#0b2441); box-shadow:inset 0 0 14px #0008; }
.machine-visual .retro-monitor-chin,.machine-visual .retro-stand,.machine-visual .retro-base {display:none;}
.machine-visual .retro-screen-header,.machine-visual .retro-status {font-size:clamp(5px,.7vw,10px); letter-spacing:1px;}
.machine-visual .retro-screen-header {margin-bottom:2%;}
.machine-visual .retro-workspace {height:78%;gap:2%;}
.machine-visual .retro-panel {padding:4%;border-radius:8px;min-height:0;overflow:hidden;}
.machine-visual .retro-panel h2 {font-size:clamp(8px,1vw,15px);margin:0 0 4%;}
.machine-visual .retro-panel label {font-size:clamp(6px,.65vw,10px);margin-bottom:2px;}
.machine-visual .retro-panel textarea {box-sizing:border-box;height:clamp(35px,8vw,115px);padding:3%;font-size:clamp(8px,.9vw,13px);resize:none;}
.machine-visual .retro-panel input {box-sizing:border-box;padding:3%;font-size:clamp(8px,.85vw,12px);}
.machine-visual .retro-settings {gap:4%;margin-top:3%;}
.machine-visual .retro-generate {margin-top:5%;padding:3%;font-size:clamp(8px,.9vw,13px);}
.machine-visual .retro-preview {min-height:0;height:78%;font-size:clamp(8px,.9vw,13px);}
.machine-visual .retro-preview img {max-height:100%;}
.machine-visual .retro-status {margin-top:2%;}
.machine-visual .retro-error {font-size:9px;margin:2px 0;}


/* SECRET_SCREEN_FIX_V2 — fully usable responsive screen inside the chassis */
.machine-visual .retro-monitor {
  left: 22.6%; top: 12.5%; width: 49.2%; height: 49.4%;
  display: block; overflow: visible;
}
.machine-visual .retro-screen {
  display: flex; flex-direction: column;
  width: 100%; height: 100%; padding: 2.1%;
  background: linear-gradient(130deg,#251736,#0b1025 60%,#0b2441);
}
.machine-visual .retro-screen-header { flex: 0 0 auto; margin-bottom: 1.8%; }
.machine-visual .retro-workspace {
  flex: 1 1 auto; height: auto; min-height: 0;
  display: grid; grid-template-columns: 1fr 1fr; gap: 2%;
}
.machine-visual .retro-panel {
  display: flex; flex-direction: column;
  box-sizing: border-box; height: 100%; min-height: 0;
  padding: 3.1%; overflow: hidden;
}
.machine-visual .retro-panel form {
  display: flex; flex-direction: column;
  min-height: 0; flex: 1 1 auto;
}
.machine-visual .retro-panel h2 { flex: 0 0 auto; margin: 0 0 2.5%; font-size: clamp(8px, .9vw, 14px); }
.machine-visual .retro-panel label { flex: 0 0 auto; margin-bottom: 1%; font-size: clamp(6px,.55vw,9px); }
.machine-visual .retro-panel textarea {
  flex: 1 1 auto; min-height: 25px; height: auto; max-height: none;
  box-sizing: border-box; padding: 2.5%;
  font-size: clamp(8px,.72vw,12px); resize: none;
}
.machine-visual .retro-settings {
  flex: 0 0 auto; margin-top: 2%; gap: 3%;
  grid-template-columns: repeat(2,minmax(0,1fr));
}
.machine-visual .retro-settings label { min-width: 0; }
.machine-visual .retro-settings input {
  width: 100%; height: clamp(17px,1.8vw,27px); padding: 1px 5px;
  font-size: clamp(8px,.65vw,11px);
}
.machine-visual .retro-generate {
  flex: 0 0 auto; width: 100%; margin-top: 2.5%;
  padding: clamp(3px,.5vw,8px) 2px;
  font-size: clamp(8px,.7vw,12px);
}
.machine-visual .retro-preview { flex: 1 1 auto; height: auto; min-height: 0; }
.machine-visual .retro-status { flex: 0 0 auto; margin-top: 1.5%; }


/* Blend the artwork into the surrounding starfield. */
.machine-visual {
  -webkit-mask-image: linear-gradient(
    to right,
    black 0%,
    black 68%,
    rgba(0,0,0,.96) 78%,
    rgba(0,0,0,.65) 89%,
    transparent 100%
  );
  mask-image: linear-gradient(
    to right,
    black 0%,
    black 68%,
    rgba(0,0,0,.96) 78%,
    rgba(0,0,0,.65) 89%,
    transparent 100%
  );
}

/* Hit area over the physical green LED, inside the unified artwork. */
.memory-power-switch {
  position: absolute; z-index: 80; left: 82.3%; top: 76%; width: 5%; height: 7%;
  border: 0; border-radius: 50%; cursor: pointer; background: transparent;
}
.memory-power-switch:focus-visible { outline: 2px solid #66ffe6; outline-offset: 2px; }
.memory-power-switch:disabled { cursor: wait; }
.memory-power-overlay {
  position: absolute; z-index: 40; left: 22.8%; top: 12.7%; width: 49%; height: 49%;
  background: #000; border-radius: 7px; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 14px; color: #8fffee;
  font: 600 clamp(8px,1vw,13px) monospace; letter-spacing: 2px; pointer-events: none;
}
.memory-power-overlay.phase-glitch-off, .memory-power-overlay.phase-glitch-on {
  animation: memory-screen-glitch .08s steps(2) infinite;
  background: repeating-linear-gradient(0deg,#02030b 0 4px,#bb65ff 5px 6px,#071e29 7px 10px);
}
.memory-boot-spinner {
  width: 34px; height: 34px; border: 3px solid #203e46;
  border-top-color: #6affdf; border-radius: 50%; animation: memory-boot-spin .7s linear infinite;
}
@keyframes memory-boot-spin { to { transform: rotate(360deg); } }
@keyframes memory-screen-glitch { 0% { filter: hue-rotate(0); transform: translateX(0); } 50% { filter: hue-rotate(120deg); transform: translateX(3px); } }

/* CONSISTENT_FIX_V1: The button covers the *painted* lower bezel LED.
   All positions are percentages of the single artwork, not the viewport. */
.machine-visual .memory-power-switch,
.machine-visual .memory-power-switch.power-on,
.machine-visual .memory-power-switch.power-off,
.machine-visual .memory-power-switch.power-boot,
.machine-visual .memory-power-switch.power-glitch-off,
.machine-visual .memory-power-switch.power-glitch-on {
  left: 70.7% !important; top: 64.4% !important;
  width: 3.4% !important; height: 4.6% !important;
  padding: 0 !important; border: 0 !important;
  background: transparent !important; box-shadow: none !important;
  z-index: 999 !important; pointer-events: auto !important;
}
.machine-visual .memory-power-switch::after {
  content: ''; position:absolute; left: 44%; top: 43%;
  width: 17%; height: 16%; border-radius: 50%;
  background: #51ffe1; box-shadow: 0 0 3px #51ffe1;
}
.machine-visual .memory-power-switch.power-off::after,
.machine-visual .memory-power-switch.power-glitch-off::after {
  background: #ff394d; box-shadow: 0 0 4px #ff394d;
}
.machine-visual .memory-power-switch.power-boot::after {
  background: #56dfff; box-shadow: 0 0 5px #56dfff;
  animation: memory-led-pulse .6s ease-in-out infinite alternate;
}
@keyframes memory-led-pulse { from {opacity:.35} to {opacity:1} }
/* Unlike masking the whole machine, only the PNG fades into the starfield.
   This avoids the vertical rectangular seam and preserves clickable controls. */
.machine-visual {
  background: none !important;
  -webkit-mask-image: none !important; mask-image: none !important;
}
.machine-visual::before {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:url('/secret/memory-machine.png') center / 100% 100% no-repeat;
  -webkit-mask-image:linear-gradient(to right,black 0%,black 66%,rgba(0,0,0,.95) 76%,rgba(0,0,0,.50) 88%,transparent 100%);
  mask-image:linear-gradient(to right,black 0%,black 66%,rgba(0,0,0,.95) 76%,rgba(0,0,0,.50) 88%,transparent 100%);
}
/* Painted indicator masks; they follow the same artwork scaling. */
.machine-visual:not(.machine-phase-on) .painted-led-cover {
  display:block;
}
.painted-led-cover {display:none; position:absolute; z-index:45; pointer-events:none; border-radius:50%;}
.painted-led-cover.monitor-upper {
  left:72.0%;top:64.1%;width:.65%;height:.75%;background:#1b2440;
}
.painted-led-cover.monitor-lower {
  left:72.2%;top:66.6%;width:.65%;height:.8%;background:#1b2440;
}
.painted-led-cover.computer-led {
  left:79.1%;top:79%;width:1%;height:1.1%;background:#15182a;
}
/* Keep the active LED above the masks. */
.machine-visual .memory-power-switch { z-index:999 !important; }


/* PANORAMA_ALIGNMENT_V2: art and controls use the same intrinsic 2048x682 coordinates. */
.retro-computer { position:relative !important; width:170vw !important; height:auto !important; margin:0 !important; max-width:none !important; filter:none !important; scale:1 !important; translate:none !important; transform:none !important; zoom:1 !important; }
.machine-visual { position:relative !important; display:block !important; width:100% !important; height:auto !important; aspect-ratio:2048 / 682 !important; background:url('/secret/memory-machine-panorama-fixed.png') left top / 100% 100% no-repeat !important; mask:none !important; -webkit-mask:none !important; filter:none !important; }
.machine-visual .retro-monitor { position:absolute !important; left:13.15% !important; top:20.5% !important; width:25.35% !important; height:42.1% !important; margin:0 !important; padding:0 !important; border:0 !important; background:transparent !important; box-shadow:none !important; transform:none !important; }
.machine-visual .retro-screen { box-sizing:border-box !important; width:100% !important; height:100% !important; padding:2.1% !important; overflow:hidden !important; border:0 !important; border-radius:6px !important; }
.machine-visual .memory-power-overlay { position:absolute !important; left:13.15% !important; top:20.5% !important; width:25.35% !important; height:42.1% !important; }
.machine-visual .retro-screen-header,.machine-visual .retro-status {font-size:clamp(6px,.57vw,10px) !important;}
.machine-visual .retro-panel h2 {font-size:clamp(8px,.72vw,13px) !important;}
.machine-visual .retro-panel textarea {font-size:clamp(8px,.7vw,12px) !important;}
.machine-visual .retro-panel input {font-size:clamp(8px,.7vw,12px) !important;}
.machine-visual .retro-generate {font-size:clamp(8px,.72vw,12px) !important;}
/* The new artwork has no colored indicator. Do not draw another one. */
.machine-visual .memory-power-switch,.machine-visual .memory-power-switch.power-on,.machine-visual .memory-power-switch.power-off,.machine-visual .memory-power-switch.power-boot,.machine-visual .memory-power-switch.power-glitch-on,.machine-visual .memory-power-switch.power-glitch-off {left:44.5% !important;top:80.5% !important;width:2.2% !important;height:5% !important;background:transparent !important;box-shadow:none !important;border:0 !important;}
.machine-visual .memory-power-switch::after,.machine-visual .memory-power-switch::before {display:none !important;content:none !important;}
.machine-visual:not(.machine-phase-on)::after,.machine-visual:not(.machine-phase-on)::before {display:none !important;content:none !important;}


/* CENTER_POWER_V1 */
/* One invisible hit target on the physical unlit power switch. */
.machine-visual {pointer-events:auto !important;}
.machine-visual .memory-power-switch,
.machine-visual .memory-power-switch.power-on,
.machine-visual .memory-power-switch.power-off,
.machine-visual .memory-power-switch.power-boot,
.machine-visual .memory-power-switch.power-glitch-on,
.machine-visual .memory-power-switch.power-glitch-off {
  position:absolute !important;
  left:44.4% !important; top:80.5% !important;
  width:2.4% !important; height:5.8% !important;
  z-index:999 !important; pointer-events:auto !important;
  display:block !important; visibility:visible !important;
  opacity:1 !important; cursor:pointer !important;
  border:0 !important; background:transparent !important; box-shadow:none !important;
}
.machine-visual .memory-power-switch::before,
.machine-visual .memory-power-switch::after {display:none !important;content:none !important;}
.machine-visual .memory-power-overlay {
  z-index:80 !important; pointer-events:none !important;
  left:13.15% !important; top:20.5% !important;
  width:25.35% !important; height:42.1% !important;
}
.machine-visual .retro-monitor {z-index:5 !important;pointer-events:auto !important;}


/* SOFT_PANORAMA_EDGE_V1 */
/* Fade ONLY the far right of the panoramic artwork. Screen and power hitbox are left of the fade. */
.machine-visual {
  -webkit-mask-image: linear-gradient(to right, #000 0%, #000 69%, rgba(0,0,0,.95) 76%, rgba(0,0,0,.62) 88%, transparent 100%) !important;
  mask-image: linear-gradient(to right, #000 0%, #000 69%, rgba(0,0,0,.95) 76%, rgba(0,0,0,.62) 88%, transparent 100%) !important;
}

</style>