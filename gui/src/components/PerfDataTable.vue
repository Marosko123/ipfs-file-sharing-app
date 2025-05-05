<!-- src/components/PerfDataTable.vue -->
<template>
  <div class="perf-table-wrapper">
    <!-- Toolbar Filters: only Op + Min/Max size -->
    <div class="table-controls">
      <label>
        Op:
        <select v-model="opFilter">
          <option value="">All</option>
          <option value="upload">Upload</option>
          <option value="download">Download</option>
        </select>
      </label>

      <label>
        Min Size (MB):
        <input
          type="number"
          v-model.number="minSize"
          placeholder="e.g. 0.1"
          min="0"
          step="0.1"
        />
      </label>

      <label>
        Max Size (MB):
        <input
          type="number"
          v-model.number="maxSize"
          placeholder="e.g. 5"
          min="0"
          step="0.1"
        />
      </label>
    </div>

    <div class="table-container">
      <table class="perf-table">
        <thead>
          <tr>
            <th @click="sortBy('ts')">
              Time <span v-if="sortKey==='ts'">{{ sortAsc ? '↑' : '↓' }}</span>
            </th>
            <th @click="sortBy('op')" class="capitalize">
              Op <span v-if="sortKey==='op'">{{ sortAsc ? '↑' : '↓' }}</span>
            </th>
            <th @click="sortBy('size')">
              Size (MB) <span v-if="sortKey==='size'">{{ sortAsc ? '↑' : '↓' }}</span>
            </th>
            <th @click="sortBy('time')">
              Duration <span v-if="sortKey==='time'">{{ sortAsc ? '↑' : '↓' }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, i) in filteredSorted" :key="i">
            <td>{{ r.ts }}</td>
            <td class="capitalize">{{ r.op }}</td>
            <td class="mono">{{ formatSizeMB(r.size) }}</td>
            <td class="mono">{{ r.time.toFixed(2) }}</td>
          </tr>
          <tr v-if="filteredSorted.length === 0">
            <td colspan="4" class="no-data">No matching records</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface PerfRecord {
  ts: string
  op: 'upload' | 'download'
  size: number
  time: number
}

const props = defineProps<{ records: PerfRecord[] }>()
const emit  = defineEmits<{ (e: 'filtered', data: PerfRecord[]): void }>()

// filters (in MB)
const opFilter   = ref<'upload'|'download'|''>('')
const minSize    = ref<number|null>(null)
const maxSize    = ref<number|null>(null)

// sorting
const sortKey = ref<keyof PerfRecord>('ts')
const sortAsc = ref(true)
function sortBy(key: keyof PerfRecord) {
  if (sortKey.value === key) sortAsc.value = !sortAsc.value
  else {
    sortKey.value = key
    sortAsc.value = true
  }
}

// filter + sort
const filteredSorted = computed(() => {
  const minB = minSize.value != null ? minSize.value * 1024 * 1024 : 0
  const maxB = maxSize.value != null ? maxSize.value * 1024 * 1024 : Infinity

  return props.records
    .filter(r => {
      if (opFilter.value && r.op !== opFilter.value) return false
      if (r.size < minB || r.size > maxB) return false
      return true
    })
    .sort((a,b) => {
      const av = a[sortKey.value], bv = b[sortKey.value]
      if (typeof av==='string' && typeof bv==='string') {
        return sortAsc.value ? av.localeCompare(bv) : bv.localeCompare(av)
      }
      if (typeof av==='number' && typeof bv==='number') {
        return sortAsc.value ? av-bv : bv-av
      }
      return 0
    })
})

// emit filtered subset
watch(filteredSorted, v => emit('filtered', v), { immediate: true })

// helper
function formatSizeMB(bytes: number) {
  return (bytes / (1024*1024)).toFixed(2) + ' MB'
}
</script>

<style scoped>
.perf-table-wrapper { display:flex; flex-direction:column; gap:.75rem; }
.table-controls {
  display:flex; flex-wrap:wrap; gap:.75rem; align-items:center;
}
.table-controls label { display:flex; align-items:center; gap:.25rem; }
.table-controls input, .table-controls select {
  padding:.3rem .5rem; font-size:.9rem;
  border:1px solid var(--text-secondary); border-radius:4px;
}

.table-container {
  max-height:300px; overflow-y:auto;
  border:1px solid #ddd; border-radius:4px;
}
.perf-table { width:100%; border-collapse:collapse; }
.perf-table th, .perf-table td {
  padding:.5rem; border-bottom:1px solid #eee; text-align:left;
}
.perf-table th {
  position:sticky; top:0; background:var(--surface);
  cursor:pointer; user-select:none;
}
.no-data { text-align:center; padding:1rem; color:var(--text-secondary); }
.mono { font-family:monospace; }
.capitalize { text-transform:capitalize; }
</style>
