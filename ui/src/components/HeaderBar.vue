<script setup lang="ts">
import { onMounted } from 'vue'

import { useMainStore } from '@/stores/main'

import logoImage from '@/assets/logo.jpg'

import globeImage from '@/assets/globe.svg'

const main = useMainStore()

</script>

<template>
  <div class="header-bar">
    <div id="logo">
      <router-link to="/">
        <v-img
          id="logo"
          :src="logoImage"
          alt="Logo"
          class="logo"
          height="70"
        />
      </router-link>
    </div>
    <a :href="main.onlinePageUrl" target="_blank" title="View online"
      ><img id="online" :src="globeImage" alt="View online"
    /></a>
  </div>
</template>

<style scoped>
.header-bar {
  padding: 0.25rem;
  display: flex;
  flex-direction: row;
}

#logo {
  flex-grow: 1;
}

a:after {
  content: none;
}

img#online {
  height: 20px;
  padding-right: 10px;
}

@media print {
  .header-bar {
    display: none;
  }
}
</style>
