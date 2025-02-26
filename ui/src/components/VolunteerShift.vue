<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Station, Shift } from '../types/main.ts'

const main = useMainStore()

const props = defineProps({
  role: {
    type: String,
    required: true
  },
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
  <div v-if="shift && station">
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
    :
    {{ role }}
    à
    {{ station.label }}
  </div>
  <div v-else>Shift or station not found</div>
</template>

<style lang="css" scoped>
div {
  margin: 10px 0;
}
</style>
