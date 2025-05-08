<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Station, Shift } from '../types/main.ts'
import ManquesShiftDetail from '@/components/ManquesShiftDetail.vue'

const main = useMainStore()

const props = defineProps({
  shiftId: {
    type: String,
    required: true
  },
  showComplet: {
    type: Boolean,
    required: true
  }
})

const shift: Ref<Shift | null> = ref(main.getShift(props.shiftId))
const station: Ref<Station | null> = ref(
  shift.value ? main.getStation(shift.value.stationId) : null
)
const shiftManques = computed(() => {
  return main.getManques(props.shiftId)
})
const shiftTotals = computed(() => {
  return main.getManques(props.shiftId, true)
})
</script>

<template>
  <tr v-if="shift && station">
    <td class="shift">
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
    </td>
    <td v-for="role in main.stationsRoles" :key="role">
      <ManquesShiftDetail :total="shiftTotals[role] || NaN" :manque="shiftManques[role] || NaN" />
    </td>
  </tr>
  <tr v-else>
    Missing data
  </tr>
</template>

<style scoped lang="css">
td {
  text-align: center;
  border: 1px solid black;
}

td.shift {
  text-align: left;
  padding: 0.2rem 0.4rem;
}
</style>
