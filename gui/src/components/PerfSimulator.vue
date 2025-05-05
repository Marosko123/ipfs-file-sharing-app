<!-- src/components/PerfSimulator.vue -->
<template>
  <div class="perf-simulator card">
    <h2>Simulator Test</h2>

    <button
      class="btn upload-btn"
      :disabled="!ready || running"
      @click="runSimulation"
    >
      {{ running ? 'Running…' : 'Run Simulation' }}
    </button>

    <p v-if="!ready" class="status">🔄 Waiting for IPFS…</p>
    <p v-if="error" class="alert error">❌ {{ error }}</p>

    <table v-if="results.length" class="sim-table">
      <thead>
        <tr>
          <th>Size</th>
          <th>Add Time (ms)</th>
          <th>Get Time (ms)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in results" :key="r.size">
          <td>{{ r.size }}</td>
          <td class="mono">{{ r.addTime.toFixed(2) }}</td>
          <td class="mono">{{ r.getTime.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue'
import type { UseIpfsReturn } from '@/composables/useIpfs'

interface SimulationResult {
  size: string
  addTime: number
  getTime: number
}

// inject the existing IPFS composable from main.ts
const ipfs = inject<UseIpfsReturn>('ipfs')
if (!ipfs) throw new Error('IPFS not provided')
const { ready, addFile, getFile } = ipfs

// define the sizes to test
const TEST_SIZES = [
  { label: '10 KB', bytes: 10 * 1024 },
  { label: '100 KB', bytes: 100 * 1024 },
  { label: '1 MB', bytes: 1024 * 1024 },
  { label: '5 MB', bytes: 5 * 1024 * 1024 }
]

const running = ref(false)
const results = ref<SimulationResult[]>([])
const error = ref<string>('')

async function runSimulation() {
  if (!ready.value) {
    error.value = 'IPFS node not ready'
    return
  }
  running.value = true
  error.value = ''
  results.value = []

  for (const { label, bytes } of TEST_SIZES) {
    try {
      // generate random data
      const data = crypto.getRandomValues(new Uint8Array(bytes))
      const file = new File([data], `sim-${bytes}.bin`)

      // measure addFile
      const t0 = performance.now()
      const cid = await addFile(file)
      const t1 = performance.now()

      // measure getFile
      const blob = await getFile(cid)
      const t2 = performance.now()

      results.value.push({
        size: label,
        addTime: t1 - t0,
        getTime: t2 - t1
      })
    } catch (e: any) {
      error.value = `Error testing ${label}: ${e.message}`
      break
    }
  }

  running.value = false
}
</script>

<style scoped>
.perf-simulator {
  max-width: 600px;
  margin: 1.5rem auto;
  text-align: center;
}
.sim-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.sim-table th,
.sim-table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
}
.sim-table th {
  background: var(--surface);
  text-transform: uppercase;
  font-size: 0.85rem;
}
.mono {
  font-family: monospace;
}
.btn {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: filter 0.2s;
  margin-top: 0.5rem;
}
.upload-btn {
  background: var(--primary);
  color: var(--surface);
}
.btn:disabled {
  background: var(--text-secondary);
  cursor: not-allowed;
}
.btn:hover:not(:disabled) {
  filter: brightness(1.1);
}
.status {
  margin-top: 1rem;
  color: var(--text-secondary);
}
.alert.error {
  margin-top: 1rem;
  color: var(--error);
}
</style>
