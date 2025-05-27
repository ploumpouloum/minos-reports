<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { useRouter } from 'vue-router'

const router = useRouter()

const main = useMainStore()

main.fetchData().then(() => {
  if (main.isSupervisor) {
    router.push({
      name: 'restrictions'
    })
  } else if (main.isDlus) {
    router.push({
      name: 'volunteers-dlus'
    })
  } else {
    router.push({
      name: 'missions'
    })
  }
})
</script>

<template>
  <div id="main">
    <div v-if="main.isLoading">
      Loading data ...
      <v-progress-circular color="primary" indeterminate></v-progress-circular>
    </div>
    <div v-else-if="!main.dataLoaded">Error loading data</div>
    <div v-else>Data loaded. Please wait few secs for UI to refresh.</div>
  </div>
</template>

<style lang="css" scoped>
#main {
  max-width: 800px;
  padding: 15px;
  margin: auto;
}
</style>
