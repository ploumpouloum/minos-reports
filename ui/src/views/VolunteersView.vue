<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { useRouter } from 'vue-router'
import type { Volunteer } from '@/types/main'
import { computed, ref } from 'vue'
import VolunteerArrived from '@/components/VolunteerArrived.vue'
import VolunteerLabel from '../components/VolunteerLabel.vue'

const main = useMainStore()

const sortCriteria = ref('incoming_date')

const sortedVolunteers = computed(() => {
  const sortFn = function (volunteer: Volunteer) {
    if (sortCriteria.value == 'name') {
      return volunteer.lastname + '+' + volunteer.firstname
    } else {
      return volunteer.incoming_date_time?.toISOString() || ''
    }
  }
  return main.volunteers.slice().sort((a, b) => sortFn(a).localeCompare(sortFn(b)))
})

const getHalfDayKey = function (date: Date) {
  if (!date) {
    return ''
  }
  const day = date.toDateString()
  const half = date.getHours() < 12 ? 'AM' : 'PM'
  return `${day}-${half}`
}

const isNewHalf = function (index: number) {
  if (index == 0) {
    return false
  }
  const currentHalf = getHalfDayKey(sortedVolunteers.value[index].incoming_date_time)
  const previousHalf = getHalfDayKey(sortedVolunteers.value[index - 1].incoming_date_time)
  return currentHalf != previousHalf
}

const router = useRouter()
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
    <h2>
      Liste des {{ sortedVolunteers.length }} volontaires{{ main.isDlus ? ' de votre UL' : '' }}
    </h2>
    <p class="screen">
      {{ sortedVolunteers.filter((volunteer) => volunteer.arrived).length }} volontaires déjà
      arrivés sur site
    </p>
    <div class="screen">
      Tri par:
      <v-btn-toggle
        v-model="sortCriteria"
        base-color="grey-lighten-3"
        color="#676767"
        class="ma-2"
        group
        density="compact"
      >
        <v-btn value="name">Nom</v-btn>
        <v-btn value="incoming_date">Arrivée</v-btn>
      </v-btn-toggle>
    </div>
    <table>
      <tr>
        <th>Bénévole</th>
        <th style="width: 7rem">Arrivée</th>
        <th style="width: 7rem">Départ</th>
        <th style="width: 10rem">Emargement</th>
        <th class="screen" style="width: 7rem">Affectations</th>
      </tr>
      <tr
        :class="{ nexthalf: sortCriteria == 'incoming_date' && isNewHalf(index) }"
        class="data"
        v-for="(volunteer, index) in sortedVolunteers"
        :key="volunteer.id"
      >
        <td><VolunteerLabel :volunteer="volunteer" /></td>
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
        <td>
          <div class="fcenter screen">
            <VolunteerArrived :initial-arrived="volunteer.arrived" :nivol="volunteer.nivol || ''" />
          </div>
        </td>
        <td class="screen">
          <div class="fcenter">
            <v-btn
              @click="
                router.push({
                  name: 'volunteer',
                  params: { nivol: volunteer.nivol }
                })
              "
              >Voir</v-btn
            >
          </div>
        </td>
      </tr>
    </table>
  </v-sheet>
</template>

<style scoped>
#main {
  padding: 15px;
  margin: auto;
  text-align: center;
}

.v-card {
  padding: 10px;
  margin: 10px 0;
}

table {
  margin: 1.5rem auto;
  border-spacing: 0;
  border-collapse: collapse;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

td {
  padding: 0.2rem 0.5rem;
  border: 1px solid black;
  max-width: 300px;
  height: 4rem;
}

tr.data:nth-child(odd) {
  background-color: #f2f2f2;
}

@media print {
  .screen {
    display: none !important;
  }
}

.fcenter {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nexthalf {
  border-top: double 5px;
}
</style>
