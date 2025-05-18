<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Station, Shift } from '../types/main.ts'
import { stationsRolesMaps } from '@/constants'

const main = useMainStore()

const props = defineProps({
  shiftId: {
    type: String,
    required: true
  },
  role: {
    type: String,
    required: true
  }
})

const shift: Ref<Shift | null> = ref(main.getShift(props.shiftId))
const station: Ref<Station | null> = ref(
  shift.value ? main.getStation(shift.value.stationId) : null
)

const localeTime = (date: Date) =>
  date.toLocaleTimeString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
</script>

<template>
  <template v-if="shift && station">
    <td>{{ stationsRolesMaps[role] }}</td>
    <td>{{ station.label }}</td>
    <td>{{ localeTime(shift.meetDateTime) }}</td>
    <td>{{ localeTime(shift.endDateTime) }}</td>
  </template>

  <template v-else><td colspan="4">Shift or station not found</td> </template>
</template>

<style lang="css" scoped>
td {
  padding: 0.2rem 0.5rem;
  border: 1px solid black;
}
</style>
