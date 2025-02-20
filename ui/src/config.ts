import axios from 'axios'
import { inject } from 'vue'
import type { PiniaPluginContext } from 'pinia'
import constants from './constants'

export type Config = {
  backend_api: string
}

async function loadConfig() {
  return (await axios.get<Config>('./config.json')).data
}

declare module 'pinia' {
  export interface PiniaCustomProperties {
    config: Config
  }
}

export function configPlugin({ store }: PiniaPluginContext) {
  const config = inject<Config>(constants.config)
  if (config) {
    store.config = config
  }
}

export default loadConfig
