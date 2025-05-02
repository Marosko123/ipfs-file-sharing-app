<template>
  <div class="uploader-container">
    <!-- Global Status / Errors -->
    <div v-if="ipfsError" class="alert error">
      ❌ IPFS init failed: {{ ipfsError.message }}
    </div>
    <div v-else-if="!ready" class="alert status">
      🔄 Connecting to IPFS…
    </div>

    <!-- Tabs -->
    <div v-else>
      <nav class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="currentTab = tab"
          :class="{ active: currentTab === tab }"
          class="tab-button"
        >{{ tab }}</button>
      </nav>

      <section class="tab-content">
        <!-- Network Tab -->
        <div v-if="currentTab === 'Network'">
          <div class="card">
            <div class="status-header">
              <span class="status-badge">🟢</span>
              <span>You: <strong>{{ peerId }}</strong></span>
              <span>Peers: <strong>{{ peerCount }}</strong></span>
            </div>
            <details class="peers-panel">
              <summary>View Connected Peers</summary>
              <table class="peers-table">
                <thead>
                  <tr><th>#</th><th>Peer ID</th></tr>
                </thead>
                <tbody>
                  <tr v-for="(id, i) in peers" :key="id">
                    <td>{{ i + 1 }}</td><td>{{ id }}</td>
                  </tr>
                  <tr v-if="peers.length === 0">
                    <td colspan="2" class="no-peers">No peers connected</td>
                  </tr>
                </tbody>
              </table>
            </details>
          </div>
        </div>

        <!-- Uploader Tab -->
        <div v-if="currentTab === 'Uploader'">
          <div class="card">
            <h2>IPFS File Uploader & Retriever</h2>

            <div class="upload-box">
              <label class="file-input-wrapper">
                <input ref="fileInput" type="file" @change="selectFile" />
                <span v-if="selectedFile">{{ selectedFile.name }}</span>
                <span v-else>📁 Choose a file</span>
              </label>
              <button
                @click="uploadFile"
                :disabled="!selectedFile || loading"
                class="btn upload-btn"
              >
                {{ loading ? 'Uploading…' : 'Upload' }}
              </button>
            </div>

            <div v-if="fileHash" class="result-box">
              <p>
                <strong>Uploaded CID:</strong>
                <span class="mono">{{ fileHash }}</span>
              </p>
              <button @click="copyToClipboard" class="btn copy-btn">
                Copy Hash
              </button>
            </div>
            <p v-if="lastUploadTime !== null" class="timing">
              Last upload: {{ lastUploadTime.toFixed(2) }} ms
            </p>

            <div class="download-box">
              <label class="download-input-wrapper">
                <input
                  type="text"
                  v-model="retrieveHash"
                  placeholder="📥 Enter CID to retrieve"
                  :disabled="loading"
                />
              </label>
              <button
                @click="retrieveFile"
                :disabled="!retrieveHash || loading"
                class="btn download-btn"
              >
                {{ loading ? 'Downloading…' : 'Download' }}
              </button>
            </div>
            <p v-if="lastDownloadTime !== null" class="timing">
              Last download: {{ lastDownloadTime.toFixed(2) }} ms
            </p>

            <p
              v-if="message"
              :class="['message', error ? 'error-message' : 'status-message']"
            >
              {{ message }}
            </p>
          </div>
        </div>

        <!-- Performance Tab -->
        <div v-if="currentTab === 'Performance'">
          <div class="card">
            <details open>
              <summary>Performance Log ({{ perfRecords.length }} entries)</summary>
              <table class="perf-table">
                <thead>
                  <tr>
                    <th>#</th><th>Time</th><th>Op</th>
                    <th>Size (bytes)</th><th>Duration (ms)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(rec, idx) in perfRecords" :key="idx">
                    <td>{{ idx + 1 }}</td>
                    <td>{{ rec.ts }}</td>
                    <td class="capitalize">{{ rec.op }}</td>
                    <td class="mono">{{ rec.size }}</td>
                    <td class="mono">{{ rec.time.toFixed(2) }}</td>
                  </tr>
                </tbody>
              </table>
              <button @click="downloadCSV" class="btn download-csv">
                Download CSV
              </button>
            </details>
          </div>
        </div>

        <!-- History Tab -->
        <div v-if="currentTab === 'History'">
          <div class="card">
            <IPFSHistory ref="historyComponent" />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue'
import type { UseIpfsReturn } from '@/composables/useIpfs'
import IPFSHistory from './IPFSHistory.vue'

interface PerfRecord {
  ts: string
  op: 'upload' | 'download'
  size: number
  time: number
}

const ipfs = inject<UseIpfsReturn>('ipfs')!
const {
  ready, error: ipfsError,
  peerId, peers, peerCount,
  addFile, getFile, pinFile
} = ipfs

// Tabs in desired order
const tabs = ['Network', 'Uploader', 'Performance', 'History']
const currentTab = ref('Network')

// State
const fileInput      = ref<HTMLInputElement|null>(null)
const selectedFile   = ref<File|null>(null)
const fileHash       = ref('')
const retrieveHash   = ref('')
const message        = ref('')
const error          = ref(false)
const loading        = ref(false)
const lastUploadTime = ref<number|null>(null)
const lastDownloadTime = ref<number|null>(null)
const perfRecords    = ref<PerfRecord[]>([])

function recordPerf(op: 'upload'|'download', size: number, time: number) {
  perfRecords.value.push({
    ts: new Date().toLocaleTimeString(),
    op, size, time
  })
}

function selectFile(e: Event) {
  selectedFile.value = (e.target as HTMLInputElement).files?.[0] ?? null
  message.value = ''
  error.value = false
}

async function uploadFile() {
  if (!selectedFile.value) return
  loading.value = true; message.value = 'Uploading…'; error.value = false
  try {
    const file = selectedFile.value!
    const t0 = performance.now()
    const cid = await addFile(file)
    const ms = performance.now() - t0

    lastUploadTime.value = ms
    recordPerf('upload', file.size, ms)
    fileHash.value = cid

    if (pinFile) await pinFile(cid)
    navigator.clipboard.writeText(cid)
    message.value = `✅ Uploaded & pinned: ${cid}`

    selectedFile.value = null
    fileInput.value!.value = ''
  } catch (e:any) {
    console.error(e)
    message.value = '❌ Upload failed'
    error.value = true
  } finally {
    loading.value = false
  }
}

async function retrieveFile() {
  if (!retrieveHash.value) return
  loading.value = true; message.value = 'Downloading…'; error.value = false
  try {
    const t0 = performance.now()
    const blob = await getFile(retrieveHash.value)
    const ms = performance.now() - t0

    lastDownloadTime.value = ms
    recordPerf('download', blob.size, ms)

    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = retrieveHash.value
    a.click()

    message.value = '✅ Downloaded!'
    retrieveHash.value = ''
  } catch (e:any) {
    console.error(e)
    message.value = '❌ Download failed'
    error.value = true
  } finally {
    loading.value = false
  }
}

function copyToClipboard() {
  if (!fileHash.value) return
  navigator.clipboard.writeText(fileHash.value)
  message.value = '✅ Hash copied!'
}

function downloadCSV() {
  const header = ['Timestamp','Op','Size','Time']
  const rows = perfRecords.value.map(r =>
    [r.ts, r.op, r.size, r.time.toFixed(2)].join(',')
  )
  const csv = [header.join(','), ...rows].join('\r\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = `perf_${Date.now()}.csv`
  a.click()
}
</script>

<style scoped>
.uploader-container {
  max-width: 900px;
  margin: 2rem auto;
  font-family: sans-serif;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Alerts */
.alert { padding: 0.75rem 1rem; border-radius: 6px; font-weight: bold; }
.alert.status { background: var(--background-muted); color: var(--text-secondary); }
.alert.error  { background: #ffe5e5;                   color: var(--error); }

/* Tabs */
.tabs { display: flex; gap: 0.5rem; }
.tab-button {
  flex: 1;
  padding: 0.75rem;
  background: var(--surface);
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-weight: bold;
  transition: border-color 0.2s;
}
.tab-button.active { border-color: var(--primary); }
.tab-button:hover { background: var(--background-muted); }

/* Card base */
.card {
  background: var(--surface);
  padding: 1.25rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Network */
.status-header {
  display: flex; align-items: center; gap: 1rem;
  font-size: 0.95rem; margin-bottom: 0.5rem;
}
.status-badge { font-size: 1.2rem; }
.peers-panel summary {
  cursor: pointer; font-weight: bold;
  padding: 0.5rem; background: var(--background-muted);
  border-radius: 4px;
}
.peers-table, .perf-table {
  width: 100%; border-collapse: collapse; margin-top: 0.5rem;
}
.peers-table th, .peers-table td,
.perf-table th, .perf-table td {
  border: 1px solid #ddd; padding: 0.5rem;
}
.peers-table th, .perf-table th {
  background: var(--surface);
  text-transform: uppercase;
  font-size: 0.85rem;
}
.no-peers {
  text-align: center; color: var(--text-secondary);
  font-style: italic;
}

/* Uploader */
.upload-box, .download-box {
  display: flex; align-items: center;
  gap: 1rem; margin-top: 1rem;
}
.file-input-wrapper,
.download-input-wrapper {
  flex: 1; padding: 0.75rem;
  border: 2px dashed var(--primary);
  border-radius: 6px;
  display: flex; align-items: center;
  color: var(--text-secondary);
}
.download-input-wrapper input {
  flex: 1; border: none;
  background: transparent;
  color: var(--text-primary);
  outline: none; font-size: 1rem;
}
.btn {
  padding: 0.6rem 1.2rem;
  border: none; border-radius: 6px;
  cursor: pointer; font-weight: bold;
  transition: filter 0.2s;
}
.upload-btn { background: var(--primary);      color: var(--surface); }
.download-btn { background: var(--primary-dark); color: var(--surface); }
.copy-btn     { background: var(--secondary);    color: var(--surface); }
.download-csv { background: var(--accent);       color: var(--surface); }
.btn:disabled { background: var(--text-secondary); cursor: not-allowed; }
.btn:hover:not(:disabled) { filter: brightness(1.1); }
.result-box {
  margin-top: 1rem;
  padding: 0.75rem;
  background: var(--background-muted);
  border-left: 4px solid var(--primary);
  display: flex; justify-content: space-between;
}
.mono     { font-family: monospace; }
.timing   { font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.5rem; }
.message  { margin-top: 1rem; font-size: 1rem; }
.status-message { color: var(--text-secondary); }
.error-message  { color: var(--error); }

/* Performance */
.perf-log summary {
  cursor: pointer; font-weight: bold;
  padding: 0.5rem; background: var(--background-muted);
  border-radius: 4px;
}
</style>
