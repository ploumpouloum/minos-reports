<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Station, Shift } from '../types/main.ts'
import VolunteerShiftMate from '@/components/VolunteerShiftMate.vue'

const main = useMainStore()

const props = defineProps({
  role: {
    type: String,
    required: true
  },
  shiftId: {
    type: String,
    required: true
  },
  volunteerId: {
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
    {{
      new Date(shift.startDateTime).toLocaleTimeString('fr-FR', {
        weekday: 'long',
        day: 'numeric',
        month: 'short',
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
    :
    <ul id="activities">
      <li>{{ role }} à {{ station.label }}</li>
      <li>
        avec
        <VolunteerShiftMate
          v-for="assignment in main.getShiftAssignments(shift.id)"
          :key="assignment.id"
          :volunteer-id="assignment.volunteerId"
          :role="assignment.role"
          :skip-volunteer-id="volunteerId"
        />
      </li>
    </ul>
  </div>
  <div v-else>Shift or station not found</div>
</template>

<style lang="css" scoped>
#activities {
  margin-left: 1rem;
}
</style>
