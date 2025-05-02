// src/composables/useIpfs.ts
import { ref, computed, onBeforeUnmount, type Ref } from 'vue'
import { createHelia, type Helia, type HeliaInit } from 'helia'
import { webTransport } from '@libp2p/webtransport'
import { importer } from 'ipfs-unixfs-importer'
import { exporter } from 'ipfs-unixfs-exporter'
import { CID } from 'multiformats/cid'
import { Web3Storage } from 'web3.storage'
import { verifiedFetch } from '@helia/verified-fetch'
import type { Blockstore } from 'interface-blockstore'

export interface UseIpfsReturn {
  helia: Ref<Helia | null>
  ready: Ref<boolean>
  error: Ref<Error | null>
  peerId: Ref<string | null>
  peers: Ref<string[]>
  peerCount: Ref<number>
  addFile: (file: File) => Promise<string>
  getFile: (cid: string) => Promise<Blob>
  pinFile: (cid: string) => Promise<void>
  verifiedFetch: (cid: string, opts?: any) => Promise<Response>
}

export function useIpfs(
  opts?: { libp2p?: HeliaInit['libp2p'] }
): UseIpfsReturn {
  const helia = ref<Helia | null>(null)
  const store = ref<Blockstore | null>(null)
  const ready = ref(false)
  const error = ref<Error | null>(null)
  const peerId = ref<string | null>(null)
  const peers = ref<string[]>([])
  const peerCount = computed(() => peers.value.length)
  let peerTimer: number

  // refresh peer list every 3s
  function updatePeers() {
    if (!helia.value) return
    peers.value = helia.value.libp2p
      .getConnections()
      .map(c => c.remotePeer.toString())
  }

  ; (async () => {
    try {
      // only WebTransport, no WebSockets, no bootstrap
      const transport = webTransport()

      const node = await createHelia({
        // remove all default listen addresses
        addresses: { listen: [] },

        // override libp2p core: only our chosen transport + no bootstrap
        libp2p: (prev): HeliaInit['libp2p'] => ({
          ...prev,
          transports: [transport],
          peerDiscovery: [],
          // ensure any other default listenAddrs don’t break
          addresses: { listen: [] },
          transportManager: {
            faultTolerance: 'NO_FATAL'
          }
        })
      })

      helia.value = node
      store.value = node.blockstore
      peerId.value = node.libp2p.peerId.toString()

      // initial peers + polling
      updatePeers()
      peerTimer = window.setInterval(updatePeers, 3000)

      ready.value = true
      console.log('[Helia] ready; peerId=', peerId.value)
    } catch (e: any) {
      error.value = e instanceof Error ? e : new Error(String(e))
      console.error('[Helia] init failed', e)
    }
  })()

  onBeforeUnmount(() => {
    clearInterval(peerTimer)
  })

  async function addFile(file: File): Promise<string> {
    if (!store.value) throw new Error('IPFS node not ready')
    const buf = new Uint8Array(await file.arrayBuffer())
    const t0 = performance.now()
    let lastCid: CID | null = null

    for await (const entry of importer(
      [{ path: file.name, content: buf }],
      store.value,
      { wrapWithDirectory: false }
    )) {
      lastCid = entry.cid
    }
    if (!lastCid) throw new Error('addFile: no CID')
    const t1 = performance.now()
    console.log(`[addFile] ${file.name} → ${lastCid} in ${(t1 - t0).toFixed(2)} ms`)
    return lastCid.toString()
  }

  async function getFile(cidStr: string): Promise<Blob> {
    if (!store.value) throw new Error('IPFS node not ready')
    const cid = CID.parse(cidStr)
    const t0 = performance.now()

    const entry = await exporter(cid, store.value)
    if (entry.type !== 'file') {
      throw new Error('getFile: CID did not resolve to a file')
    }

    // entry.content() must be called to get async iterator
    const chunks: Uint8Array[] = []
    for await (const chunk of entry.content()) {
      chunks.push(chunk)
    }

    const blob = new Blob(chunks)
    const t1 = performance.now()
    console.log(`[getFile] ${cidStr} in ${(t1 - t0).toFixed(2)} ms`)
    return blob
  }

  async function pinFile(cidStr: string): Promise<void> {
    const token = import.meta.env.VITE_WEB3_API_TOKEN
    if (!token) {
      console.warn('[pinFile] no Web3.Storage token; skipping')
      return
    }
    try {
      await new Web3Storage({ token }).pin(cidStr)
      console.log('[pinFile] pinned', cidStr)
    } catch (e) {
      console.error('[pinFile] error', e)
    }
  }

  function vf(cid: string, opts?: any): Promise<Response> {
    if (!helia.value) throw new Error('IPFS node not ready')
    return verifiedFetch(cid, { helia: helia.value, ...opts })
  }

  return {
    helia,
    ready,
    error,
    peerId,
    peers,
    peerCount,
    addFile,
    getFile,
    pinFile,
    verifiedFetch: vf
  }
}
