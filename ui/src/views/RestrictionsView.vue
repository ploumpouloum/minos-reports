<script setup lang="ts">
import { useMainStore } from '@/stores/main'

const main = useMainStore()

main.fetchData()
</script>

<template>
  <v-sheet v-if="!main.dataLoaded" id="main">
    <p>
      Loading data ...
      <v-progress-circular color="primary" indeterminate></v-progress-circular>
    </p>
  </v-sheet>
  <v-sheet v-else id="main">
    <v-card variant="outlined" class="card">
      <h3>Mineurs</h3>
      <p
        v-for="volunteer in main.volunteers
          .filter((volunteer) => volunteer.minor)
          .sort((a, b) => a.lastname.localeCompare(b.lastname))"
        :key="volunteer.id"
      >
        {{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }})
      </p>
      <p v-if="main.volunteers.filter((volunteer) => volunteer.minor).length == 0">Aucun mineur</p>
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
        {{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }})
      </p>
      <p
        v-if="
          main.volunteers.filter((volunteer) => volunteer.mission_restrictions?.includes('BINOME'))
            .length == 0
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
        {{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }})
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
        {{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }})
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
        {{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }}):
        {{ volunteer.food_restrictions?.join(', ') }}
      </p>
      <p v-if="main.volunteers.filter((volunteer) => volunteer.food_restrictions).length == 0">
        Aucune personne avec des restrictions alimentaires
      </p>
    </v-card>
  </v-sheet>
</template>

<style scoped>
#main {
  padding: 15px;
  margin: auto;
  display: flex;
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
