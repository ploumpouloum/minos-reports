<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import Report1Assignement from './Report1Assignement.vue'
import type { Station, Shift } from '../types/main.ts'

const main = useMainStore()

const props = defineProps({
  shiftId: {
    type: String,
    required: true
  }
})

const shift: Ref<Shift | null> = ref(main.getShift(props.shiftId))
const station: Ref<Station | null> = ref(
  shift.value ? main.getStation(shift.value.stationId) : null
)
</script>

<template>
  <table v-if="shift && station">
    <thead>
      <tr>
        <th colspan="2">
          {{ station.label }} de
          {{
            new Date(shift.startDateTime).toLocaleTimeString('fr-FR', {
              hour: '2-digit',
              minute: '2-digit'
            })
          }}
          à
          {{
            new Date(shift.endDateTime).toLocaleTimeString('fr-FR', {
              hour: '2-digit',
              minute: '2-digit'
            })
          }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="assignment in main.getShiftAssignments(shift.id)"
        :key="assignment.volunteerId + assignment.shiftId"
      >
        <Report1Assignement :assignment="assignment" />
      </tr>
    </tbody>
  </table>
  <div v-else>Shift or station not found</div>
</template>

<style lang="css">
table {
  margin-bottom: 10px;
  width: 100%;
}
</style>
