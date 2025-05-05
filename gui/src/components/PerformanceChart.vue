<template>
  <div class="chart-container">
    <!-- pass your computed chartData into `data` and chartOptions into `options` -->
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

// register Chart.js
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
)

interface PerfRecord {
  ts: string
  op: 'upload' | 'download'
  size: number
  time: number
}
const props = defineProps<{ records: PerfRecord[] }>()

// derive sorted, unique size labels
const labels = computed<string[]>(() =>
  Array.from(new Set(props.records.map(r => r.size.toString())))
    .sort((a, b) => Number(a) - Number(b))
)

function datasetFor(op: 'upload'|'download', color: string) {
  return {
    label: op,
    data: labels.value.map(lbl => {
      const rec = props.records.find(r => r.size.toString() === lbl && r.op === op)
      return rec ? rec.time : NaN
    }),
    fill: false,
    borderColor: color,
    tension: 0.2
  }
}

const chartData = computed(() => ({
  // unwrap the ref to a plain array so Chart.js sees it properly :contentReference[oaicite:1]{index=1}
  labels: labels.value,
  datasets: [
    datasetFor('upload',   'rgb(54,162,235)'),
    datasetFor('download', 'rgb(255,99,132)')
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' as const },
    title:  { display: true, text: 'IPFS Performance by File Size' }
  },
  scales: {
    x: { title: { display: true, text: 'Size (bytes)' } },
    y: { title: { display: true, text: 'Time (ms)' } }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 300px;
  margin-top: 1rem;
}
</style>
