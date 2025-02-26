<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { useRoute, useRouter } from 'vue-router'
import { ref, watch, type Ref } from 'vue'
import { getRouteParam } from '@/utils'
import VolunteerShift from '@/components/VolunteerShift.vue'
import type { Volunteer } from '@/types/main'

const route = useRoute()
const router = useRouter()

const main = useMainStore()

const volunteer: Ref<Volunteer | undefined> = ref()

const refreshData = () => {
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
    <h2>{{ $route.params.nivol }} - {{ volunteer.firstname }} {{ volunteer.lastname }}</h2>
    <v-card
      variant="outlined"
      v-for="assignment in main.getVolunteerAssignments(volunteer.id)"
      :key="assignment.shiftId"
      @click="router.push({ name: 'shift', params: { shiftId: assignment.shiftId } })"
    >
      <VolunteerShift :role="assignment.role" :shift-id="assignment.shiftId" />
    </v-card>
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
