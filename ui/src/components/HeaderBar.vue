<script setup lang="ts">
import logoImage from '@/assets/logo.jpg'
</script>

<template>
  <div class="header-bar">
    <div id="logo">
      <router-link to="/">
        <v-img id="logo" :src="logoImage" alt="Logo" class="logo" height="70" />
      </router-link>
    </div>
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
