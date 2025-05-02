import type { UseIpfsReturn } from './useIpfs'

export interface PerfResult {
  size: string
  add: number   // ms
  get: number   // ms
}

/** byte sizes you want to test */
const TEST_SIZES = [
  { label: '10 KB', bytes: 10 * 1024 },
  { label: '100 KB', bytes: 100 * 1024 },
  { label: '1 MB', bytes: 1024 * 1024 },
  { label: '5 MB', bytes: 5 * 1024 * 1024 }
]

/**
 * Runs add/get for various blob sizes and measures timings.
 * Logs timings to the console and returns them to the UI.
 */
export async function runPerfTest(ipfs: UseIpfsReturn): Promise<PerfResult[]> {
  const results: PerfResult[] = []

  for (const { label, bytes } of TEST_SIZES) {
    /* -------- create a random Uint8Array of the target size -------- */
    const randomData = crypto.getRandomValues(new Uint8Array(bytes))
    const file = new File([randomData], `perf-${bytes}.bin`, {
      type: 'application/octet-stream'
    })

    /* ---------------------- ADD (upload) timing -------------------- */
    const t0 = performance.now()
    const cid = await ipfs.addFile(file)
    const t1 = performance.now()

    /* --------------------- GET (download) timing ------------------- */
    await ipfs.getFile(cid)
    const t2 = performance.now()

    const addMs = t1 - t0
    const getMs = t2 - t1

    /* console output for quick inspection */
    // eslint-disable-next-line no-console
    console.log(
      `[PerfTest] ${label}  ➜  add: ${addMs.toFixed(2)} ms  |  get: ${getMs.toFixed(2)} ms`
    )

    results.push({ size: label, add: addMs, get: getMs })
  }

  return results
}
