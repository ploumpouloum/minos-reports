import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
//import axios from 'axios'
import { createVuetify } from 'vuetify'
//import type { Config } from '@/types/config'

async function loadVuetify() {
  const primaryColor = '#000000'
  const secondaryColor = '#FFFFFF'

  // Load secondary colors from config.json
  /*
  try {
    const response = await axios.get('./content/config.json')
    if (response.status === axios.HttpStatusCode.Ok) {
      const config: Config = response.data
      secondaryColor = config.secondaryColor || secondaryColor
    } else {
      console.error('Failed to fetch config.json')
    }
  } catch (error) {
    console.error('Error loading config:', error)
  }
  */
  const uiTheme = {
    colors: {
      background: secondaryColor,
      surface: secondaryColor,
      primary: primaryColor
    }
  }

  return createVuetify({
    theme: {
      defaultTheme: 'uiTheme',
      variations: {
        colors: ['background', 'primary'],
        lighten: 2,
        darken: 2
      },
      themes: {
        uiTheme
      }
    }
  })
}

export default loadVuetify
