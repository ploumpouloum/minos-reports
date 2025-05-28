<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import type { Volunteer } from '@/types/main'
import { type PropType } from 'vue'
import VolunteerDlusVacation from '../components/VolunteerDlusVacation.vue'
import VolunteerLabel from './VolunteerLabel.vue'

const main = useMainStore()

defineProps({
  volunteer: {
    type: Object as PropType<Volunteer>,
    required: true
  }
})
</script>

<template>
  <div v-if="!volunteer">No volunteer set</div>
  <div v-else>
    <div class="volunteer">
      <VolunteerLabel :volunteer="volunteer" />
    </div>
    <table>
      <tr v-for="assignment in main.getVolunteerAssignments(volunteer.id)" :key="assignment.id">
        <VolunteerDlusVacation :shift-id="assignment.shiftId" :role="assignment.role" />
      </tr>
    </table>
  </div>
</template>

<style scoped lang="css">
.volunteer {
  font-weight: bold;
  text-align: center;
}

table {
  margin: 0.5rem auto 1.5rem auto;
  border-spacing: 0;
  border-collapse: collapse;
  width: 100%;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}
</style>
