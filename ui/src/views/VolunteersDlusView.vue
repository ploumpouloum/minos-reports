<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { computed, ref } from 'vue'
import { stationsRolesOrder, stationsRolesMaps } from '@/constants'
import VolunteerDlus from '../components/VolunteerDlus.vue'

const main = useMainStore()

const selectedDlus = ref()

const displayDetails = ref(false)

const toggleDisplayDetails = function () {
  displayDetails.value = !displayDetails.value
}

const existingDlus = computed(() => [
  ...new Set(
    main.volunteers.map((volunteer) => volunteer.dlus_email).sort((a, b) => a.localeCompare(b))
  )
])

const selectedVolunteers = computed(() =>
  main.volunteers
    .filter((volunteer) => main.isDlus || volunteer.dlus_email == selectedDlus.value)
    .sort((a, b) => a.lastname.localeCompare(b.lastname))
)
</script>

<template>
  <v-sheet v-if="!main.dataLoaded" id="main">
    <p>
      Loading data ...
      <v-progress-circular color="primary" indeterminate></v-progress-circular>
    </p>
  </v-sheet>
  <v-sheet v-else id="main">
    <div v-if="!main.isDlus && !main.isSupervisor">Cet écran est réservé aux DLUS</div>
    <div v-else>
      <div v-if="main.isSupervisor" id="dlus-select">
        Cet écran est normalement réservé aux DLUS
        <v-combobox
          :items="existingDlus"
          v-model="selectedDlus"
          density="comfortable"
          clearable
          label="Voir la vue en tant que"
        />
      </div>
      <template v-if="selectedVolunteers.length">
        <h2>Liste des volontaires inscrits et validés par la Maxi-Race</h2>
        <table v-if="!displayDetails">
          <tr>
            <th>Bénévole</th>
            <th>Role</th>
            <th>Arrivée</th>
            <th>Départ</th>
          </tr>
          <tr class="data" v-for="volunteer in selectedVolunteers" :key="volunteer.id">
            <td>{{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }})</td>
            <td class="roles">
              {{
                volunteer.roles
                  ?.map((role) => stationsRolesMaps[role])
                  .sort(function (a, b) {
                    return stationsRolesOrder.indexOf(a) - stationsRolesOrder.indexOf(b)
                  })
                  .join(', ')
              }}
            </td>
            <td class="arrives">
              {{
                new Date(volunteer.incoming_date_time).toLocaleTimeString('fr-FR', {
                  day: '2-digit',
                  month: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit'
                })
              }}
            </td>
            <td class="departs">
              {{
                new Date(volunteer.outgoing_date_time).toLocaleTimeString('fr-FR', {
                  day: '2-digit',
                  month: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit'
                })
              }}
            </td>
          </tr>
        </table>

        <template v-if="displayDetails">
          <template v-for="volunteer in selectedVolunteers" :key="volunteer.id">
            <VolunteerDlus :volunteer="volunteer" />
          </template>
        </template>

        <div id="zoom">
          <v-btn @click="toggleDisplayDetails"
            >Voir {{ displayDetails ? 'résumé' : 'détails' }}
          </v-btn>
        </div>
      </template>
    </div>
  </v-sheet>
</template>

<style scoped>
#main {
  padding: 15px 0;
  margin: auto;
  width: min(800px, calc(100vw - 30px));
}

h2 {
  text-align: center;
}

#dlus-select {
  max-width: 400px;
  margin: auto;
  text-align: center;
}

table {
  margin: 1.5rem auto;
  border-spacing: 0;
  border-collapse: collapse;
  width: 100%;
}

td {
  padding: 0.2rem 0.5rem;
  border: 1px solid black;
}

tr.data:nth-child(odd) {
  background-color: #f2f2f2;
}

td.arrives,
td.departs {
  width: 7rem;
}

#zoom .v-btn {
  margin: 2rem auto;
}

@media print {
  #zoom {
    display: none;
  }
}
</style>
