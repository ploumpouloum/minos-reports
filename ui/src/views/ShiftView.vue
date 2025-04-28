<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { useRoute, useRouter } from 'vue-router'
import { ref, watch, type Ref } from 'vue'
import { getRouteParam } from '@/utils'
import type { Shift, Station } from '@/types/main'
import ShiftAssignment from '@/components/ShiftAssignment.vue'
import ShiftEmptyAssignment from '@/components/ShiftEmptyAssignment.vue'

const route = useRoute()
const router = useRouter()

const main = useMainStore()

const shift: Ref<Shift | undefined> = ref()
const station: Ref<Station | undefined> = ref()

main.fetchData()

const refreshData = () => {
  if (!main.dataLoaded) {
    return
  }
  shift.value = main.getShift(getRouteParam(route.params.shiftId))
  station.value = main.getStation(shift.value.stationId)
}

refreshData()

watch(
  () => main.dataLoaded,
  () => refreshData()
)

watch(
  () => route.params.shiftId,
  () => refreshData()
)
</script>

<template>
  <v-sheet v-if="main.dataLoaded && shift && station" id="main">
    <h2>{{ station.label }}</h2>
    <h3>
      De
      {{
        new Date(shift.startDateTime).toLocaleTimeString('fr-FR', {
          weekday: 'long',
          hour: '2-digit',
          minute: '2-digit'
        })
      }}
      à
      {{
        new Date(shift.endDateTime).toLocaleTimeString('fr-FR', {
          weekday: 'long',
          hour: '2-digit',
          minute: '2-digit'
        })
      }}
    </h3>
    <v-card
      variant="outlined"
      v-for="assignment in main.getShiftAssignments(shift.id)"
      :key="assignment.volunteerId"
      @click="
        assignment.volunteerId
          ? router.push({
              name: 'volunteer',
              params: { nivol: main.getVolunteer(assignment.volunteerId).nivol }
            })
          : router.push({
              name: 'assignement',
              params: { shiftId: assignment.shiftId, role: assignment.role }
            })
      "
    >
      <ShiftAssignment
        v-if="assignment.volunteerId"
        :role="assignment.role"
        :volunteer-id="assignment.volunteerId"
      />
      <ShiftEmptyAssignment v-else :role="assignment.role" />
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
