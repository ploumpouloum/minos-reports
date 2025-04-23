<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import VolunteerShift from '@/components/VolunteerShift.vue'

const main = useMainStore()
</script>

<template>
  <v-sheet v-if="main.dataLoaded" id="main">
    <div v-if="!main.isDlus">Cet écran est réservé aux DLUS</div>
    <div v-else>
      <h2>Liste des inscrits rattachés à toi en tant que DLUS</h2>
      <v-card
        variant="outlined"
        v-for="volunteer in main.volunteers.sort((a, b) => a.lastname.localeCompare(b.lastname))"
        :key="volunteer.id"
      >
        <p>{{ volunteer.firstname }} {{ volunteer.lastname }} ({{ volunteer.department }})</p>
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
      </v-card>
    </div>
  </v-sheet>
  <v-sheet v-else id="main">Waiting for data ...</v-sheet>
</template>

<style scoped>
#main {
  max-width: 800px;
  padding: 15px;
  margin: auto;
}

.v-card {
  padding: 10px;
  margin: 10px 0;
}

#activities li {
  margin-left: 2rem;
}
</style>
