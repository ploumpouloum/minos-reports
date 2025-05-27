<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import type { Volunteer } from '@/types/main'
import { type Ref, ref, watch } from 'vue'
import VolunteerMissions from '../components/VolunteerMissions.vue'

const main = useMainStore()

main.fetchData()

const volunteer: Ref<Volunteer | undefined> = ref()

const refreshData = () => {
  if (!main.dataLoaded) {
    return
  }
  volunteer.value = main.myVolunteerId ? main.getVolunteer(main.myVolunteerId) : undefined
}

refreshData()

watch(
  () => main.dataLoaded,
  () => refreshData()
)

watch(
  () => main.myVolunteerId,
  () => refreshData()
)
</script>

<template>
  <v-sheet id="main">
    <v-card variant="outlined">
      <p>Bienvenue à la MaxiRace 2025 à Annecy !</p>
    </v-card>
    <p v-if="!main.dataLoaded">
      Loading data ...
      <v-progress-circular color="primary" indeterminate></v-progress-circular>
    </p>
    <p v-else-if="!volunteer">Il semble que tu n'es pas (encore ?) inscrit.e à la MaxiRace.</p>
    <div class="planning" v-else>
      <h3>Ton planning actuel</h3>
      <VolunteerMissions :volunteer="volunteer" />
    </div>
  </v-sheet>
</template>

<style scoped lang="css">
#main {
  max-width: 800px;
  padding: 15px;
  margin: auto;
}

.v-card {
  padding: 10px;
  margin: 10px 0;
}

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
