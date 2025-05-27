<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { useRoute } from 'vue-router'
import { ref, watch, type Ref } from 'vue'
import { getRouteParam } from '@/utils'
import VolunteerMissions from '../components/VolunteerMissions.vue'
import type { Volunteer } from '@/types/main'

const route = useRoute()

const main = useMainStore()

const volunteer: Ref<Volunteer | undefined> = ref()

const refreshData = () => {
  if (!main.dataLoaded) {
    return
  }
  volunteer.value = main.getVolunteerByNivol(getRouteParam(route.params.nivol))
}

refreshData()

watch(
  () => main.dataLoaded,
  () => refreshData()
)

watch(
  () => route.params.nivol,
  () => refreshData()
)
</script>

<template>
  <v-sheet v-if="!main.dataLoaded" id="main">
    <p>
      Loading data ...
      <v-progress-circular color="primary" indeterminate></v-progress-circular>
    </p>
  </v-sheet>
  <v-sheet v-else-if="!main.isSupervisor" id="main">Cet écran est réservé aux superviseurs</v-sheet>
  <v-sheet v-else-if="main.dataLoaded && volunteer" id="main">
    <h2>{{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }})</h2>
    <div>
      <VolunteerMissions :volunteer="volunteer" :volunteersClickable="true" />
    </div>
  </v-sheet>
  <v-sheet v-else id="main">Insufficient data found</v-sheet>
</template>

<style scoped>
#main {
  max-width: 800px;
  padding: 15px;
  margin: auto;
}

h3 {
  margin-bottom: 15px;
}
.v-card {
  padding: 10px;
  margin: 10px 0;
}
</style>
