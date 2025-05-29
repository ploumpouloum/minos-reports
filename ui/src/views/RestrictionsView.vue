<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import VolunteerLabel from '../components/VolunteerLabel.vue'

const main = useMainStore()
</script>

<template>
  <v-sheet v-if="!main.dataLoaded" id="main">
    <p>
      Loading data ...
      <v-progress-circular color="primary" indeterminate></v-progress-circular>
    </p>
  </v-sheet>
  <v-sheet v-else-if="!main.isSupervisor" id="main">Cet écran est réservé aux superviseurs</v-sheet>
  <v-sheet v-else id="main">
    <div class="line">
      <v-card variant="outlined" class="card">
        <h3>Mineurs</h3>
        <p
          v-for="volunteer in main.volunteers
            .filter((volunteer) => volunteer.minor)
            .sort((a, b) => a.lastname.localeCompare(b.lastname))"
          :key="volunteer.id"
        >
          <VolunteerLabel :volunteer="volunteer" />
        </p>
        <p v-if="main.volunteers.filter((volunteer) => volunteer.minor).length == 0">
          Aucun mineur
        </p>
      </v-card>
      <v-card variant="outlined" class="card">
        <h3>Attention ne veut pas</h3>
        <h4>Binome</h4>
        <p
          v-for="volunteer in main.volunteers
            .filter((volunteer) => volunteer.mission_restrictions?.includes('BINOME'))
            .sort((a, b) => a.lastname.localeCompare(b.lastname))"
          :key="volunteer.id"
        >
          <VolunteerLabel :volunteer="volunteer" />
        </p>
        <p
          v-if="
            main.volunteers.filter((volunteer) =>
              volunteer.mission_restrictions?.includes('BINOME')
            ).length == 0
          "
        >
          Aucune personne avec des restrictions de missions BINOME
        </p>
        <h4>VPS</h4>
        <p
          v-for="volunteer in main.volunteers
            .filter((volunteer) => volunteer.mission_restrictions?.includes('VPS'))
            .sort((a, b) => a.lastname.localeCompare(b.lastname))"
          :key="volunteer.id"
        >
          <VolunteerLabel :volunteer="volunteer" />
        </p>
        <p
          v-if="
            main.volunteers.filter((volunteer) => volunteer.mission_restrictions?.includes('VPS'))
              .length == 0
          "
        >
          Aucune personne avec des restrictions de missions VPS
        </p>
        <h4>Montagne</h4>
        <p
          v-for="volunteer in main.volunteers
            .filter((volunteer) => volunteer.mission_restrictions?.includes('MONTAGNE'))
            .sort((a, b) => a.lastname.localeCompare(b.lastname))"
          :key="volunteer.id"
        >
          <VolunteerLabel :volunteer="volunteer" />
        </p>
        <p
          v-if="
            main.volunteers.filter((volunteer) =>
              volunteer.mission_restrictions?.includes('MONTAGNE')
            ).length == 0
          "
        >
          Aucune personne avec des restrictions de missions MONTAGNE
        </p>
      </v-card>
      <v-card variant="outlined" class="card">
        <h3>Restrictions alimentaires</h3>
        <p
          v-for="volunteer in main.volunteers
            .filter((volunteer) => volunteer.food_restrictions)
            .sort((a, b) => a.lastname.localeCompare(b.lastname))"
          :key="volunteer.id"
        >
          <VolunteerLabel :volunteer="volunteer" />:
          {{ volunteer.food_restrictions?.join(', ') }}
        </p>
        <p v-if="main.volunteers.filter((volunteer) => volunteer.food_restrictions).length == 0">
          Aucune personne avec des restrictions alimentaires
        </p>
      </v-card>
    </div>
    <div class="line">
      <v-card variant="outlined" class="card">
        <h3>Informations complémentaires</h3>
        <table>
          <tr
            v-for="assignment in main.assignments
              .filter((assignment) => assignment.comments)
              .sort(function (a, b) {
                return (
                  new Date(main.getShift(a.shiftId).startDateTime).getTime() -
                  new Date(main.getShift(b.shiftId).startDateTime).getTime()
                )
              })"
            :key="assignment.id"
          >
            <td>{{ main.getStation(main.getShift(assignment.shiftId).stationId).label }}</td>
            <td>
              {{
                main.getShift(assignment.shiftId).startDateTime.toLocaleTimeString('fr-FR', {
                  day: '2-digit',
                  month: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit'
                })
              }}
              à
              {{
                main.getShift(assignment.shiftId).endDateTime.toLocaleTimeString('fr-FR', {
                  hour: '2-digit',
                  minute: '2-digit'
                })
              }}
            </td>
            <td>
              <VolunteerLabel
                v-if="assignment.volunteerId"
                :volunteer="main.getVolunteer(assignment.volunteerId)"
              />
            </td>
            <td>{{ assignment.role }}</td>
            <td>{{ assignment.comments }}</td>
          </tr>
        </table>
        <p v-if="main.assignments.filter((assignment) => assignment.comments).length == 0">
          Aucune information complémentaire
        </p>
      </v-card>
    </div>
  </v-sheet>
</template>

<style scoped>
#main {
  padding: 15px;
  margin: auto;
}

.line {
  padding-bottom: 1rem;
  display: flex;
}

@media screen and (max-width: 1024px) {
  .line {
    padding-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
}

table {
  border-spacing: 0;
  border-collapse: collapse;
}

td {
  padding: 0.2rem 0.5rem;
  border: 1px solid black;
}

h3 {
  margin-bottom: 15px;
}

.card {
  padding: 10px;
  margin: 0 10px;
  flex-grow: 1;
}

h4 {
  margin-top: 10px;
}

p {
  font-size: 0.9rem;
}
</style>
