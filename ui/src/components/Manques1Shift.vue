<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Station, Shift } from '../types/main.ts'

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
    <td class="manques" v-if="Object.keys(shiftManques).length > 0">
      <span v-for="(count, role, idx) in shiftManques" :key="role"
        >{{ idx ? ', ' : 'Manque ' }}<b>{{ count }}</b> {{ role }}</span
      >
    </td>
    <td class="manques complet" v-else>COMPLET</td>
  </tr>
  <tr v-else>
    Missing data
  </tr>
</template>

<style scoped lang="css">
.manques {
  text-align: end;
  color: red;
}

.complet {
  color: green;
}
</style>
