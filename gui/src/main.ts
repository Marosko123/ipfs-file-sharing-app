import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useIpfs } from '@/composables/useIpfs'

import App from './App.vue'
import router from './router'

const ipfs = useIpfs()
const app = createApp(App)

app.provide('ipfs', ipfs)

app.use(createPinia())
app.use(router)

app.mount('#app')
