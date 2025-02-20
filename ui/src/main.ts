import './assets/main.css'

import { createApp } from 'vue'
import constants from './constants'

import App from './App.vue'
import router from './router'
import loadVuetify from './plugins/vuetify'

import ResizeObserver from 'resize-observer-polyfill'

if (typeof window.ResizeObserver === 'undefined') {
  console.debug('Polyfilling ResizeObserver')
  window.ResizeObserver = ResizeObserver
}

// Pinia
import { createPinia } from 'pinia'
const pinia = createPinia()

// config
import loadConfig, { configPlugin } from './config'

Promise.all([loadConfig(), loadVuetify()])
  .then(([config, vuetify]) => {
    const app = createApp(App)
    app.use(pinia)
    app.use(vuetify)

    // provide config app-wide
    app.provide(constants.config, config)

    // inject plugins into store
    pinia.use(configPlugin)

    app.use(router)
    app.mount('#app')
  })
  .catch((error) => {
    console.error('Error initializing app:', error)
  })
