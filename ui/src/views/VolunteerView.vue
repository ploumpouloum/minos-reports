<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { useRoute } from 'vue-router'
import { ref, watch, type Ref } from 'vue'
import { getRouteParam } from '@/utils'
import VolunteerMissions from '../components/VolunteerMissions.vue'
import type { Volunteer } from '@/types/main'

const route = useRoute()

const main = useMainStore()

main.fetchData()

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
  <v-sheet v-if="main.dataLoaded && volunteer" id="main">
    <h2>{{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }})</h2>
    <div v-if="!main.isDlus && !main.isSupervisor">
      Vous ne pouvez voir le détail des affectations de ce volontaire.
    </div>
    <div v-else>
      <VolunteerMissions :volunteer="volunteer" :volunteersClickable="true" />
    </div>
  </v-sheet>
  <v-sheet v-else id="main">Waiting for data ...</v-sheet>
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
