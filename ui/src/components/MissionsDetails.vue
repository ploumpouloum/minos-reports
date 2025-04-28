<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import type { Volunteer } from '@/types/main'
import { type ComputedRef, computed } from 'vue'
import VolunteerShift from '@/components/VolunteerShift.vue'

const main = useMainStore()

main.fetchData()

const volunteer: ComputedRef<Volunteer | undefined> = computed(() =>
  main.myVolunteerId ? main.getVolunteer(main.myVolunteerId) : undefined
)
</script>

<template>
  <p>Bienvenue à la MaxiRace 2025 à Annecy !</p>
  <p v-if="main.isLoading">Loading data ...</p>
  <p v-else-if="!volunteer">Il semble que tu n'es pas (encore ?) inscrit.e à la MaxiRace.</p>
  <div v-else>
    <h3>Ton planning actuel:</h3>
    <ul id="activities">
      <li>
        Arrive
        {{
          new Date(volunteer.incoming_date_time).toLocaleTimeString('fr-FR', {
            weekday: 'long',
            day: '2-digit',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit'
          })
        }}
      </li>
      <li
        v-for="assignment in main.getVolunteerAssignments(volunteer.id)"
        :key="assignment.shiftId"
      >
        <VolunteerShift
          :role="assignment.role"
          :shift-id="assignment.shiftId"
          :volunteer-id="volunteer.id"
        />
      </li>
      <li>
        Repart
        {{
          new Date(volunteer.outgoing_date_time).toLocaleTimeString('fr-FR', {
            weekday: 'long',
            day: '2-digit',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit'
          })
        }}
      </li>
    </ul>
  </div>
</template>

<style scoped lang="css">
p {
  padding: 1rem 0 2rem;
}
#activities li {
  margin-left: 2rem;
}
</style>
