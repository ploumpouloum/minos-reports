<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import Report1Assignement from './Report1Assignement.vue'
import type { Station } from '../types/main.ts'

const main = useMainStore()

const props = defineProps({
  stationId: {
    type: String,
    required: true
  }
})

const station: Ref<Station | null> = ref(main.getStation(props.stationId))
</script>

<template>
  <table v-if="station">
    <thead>
      <tr>
        <th colspan="2">
          {{ station.label }} de
          {{
            station.startDateTime.toLocaleTimeString('fr-FR', {
              hour: '2-digit',
              minute: '2-digit'
            })
          }}
          à
          {{
            station.endDateTime.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
          }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="assignment in main.getStationAssignments(station.id)"
        :key="assignment.idVolunteer + assignment.idStation"
      >
        <Report1Assignement :assignment="assignment" />
      </tr>
    </tbody>
  </table>
  <div v-else>Station not found</div>
</template>

<style lang="css">
table {
  margin-bottom: 10px;
  width: 100%;
}
</style>
