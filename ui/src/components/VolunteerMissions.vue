<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import type { Volunteer } from '@/types/main'
import { type PropType } from 'vue'
import VacationsShift from '../components/VacationsShift.vue'

const main = useMainStore()

defineProps({
  volunteer: {
    type: Object as PropType<Volunteer>,
    required: true
  },
  volunteersClickable: {
    type: Boolean,
    required: false
  }
})
</script>

<template>
  <div v-if="!volunteer">No volunteer set</div>
  <div v-else>
    <div class="arrival">
      Arrivée le
      {{
        new Date(volunteer.incoming_date_time).toLocaleTimeString('fr-FR', {
          weekday: 'long',
          day: '2-digit',
          month: 'short',
          hour: '2-digit',
          minute: '2-digit'
        })
      }}
    </div>
    <div
      class="day-block"
      v-for="startDay in main.getVolunteerAssignmentsDays(volunteer.id)"
      :key="startDay.toISOString()"
    >
      <div class="day">
        {{
          startDay.toLocaleDateString('fr-FR', { weekday: 'long', day: '2-digit', month: 'long' })
        }}
      </div>
      <div class="shifts">
        <div
          class="shift"
          v-for="assignment in main.getVolunteerAssignmentsByDay(volunteer.id, startDay)"
          :key="assignment.shiftId"
        >
          <VacationsShift
            :shiftId="assignment.shiftId"
            :current-volunteer="volunteer"
            :volunteers-clickable="volunteersClickable"
          />
        </div>
      </div>
    </div>
    <div class="departure">
      Départ le
      {{
        new Date(volunteer.outgoing_date_time).toLocaleTimeString('fr-FR', {
          weekday: 'long',
          day: '2-digit',
          month: 'short',
          hour: '2-digit',
          minute: '2-digit'
        })
      }}
    </div>
  </div>
</template>

<style scoped lang="css">
.shifts {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1rem;
  margin: 1rem;
}

@media (min-width: 1440px) {
  .shifts {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.day {
  background-color: #e40613;
  padding: 0.5rem 0;
  color: white;
  text-align: center;
  margin-bottom: 10px;
}

.arrival,
.departure {
  text-align: center;
  padding: 1rem 0;
}

h3 {
  text-align: center;
  margin-top: 1.5rem;
}
</style>
