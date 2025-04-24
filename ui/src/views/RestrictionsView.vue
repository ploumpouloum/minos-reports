<script setup lang="ts">
import { useMainStore } from '@/stores/main'

const main = useMainStore()

main.fetchData()
</script>

<template>
  <v-sheet v-if="main.dataLoaded" id="main">
    <v-card variant="outlined">
      <h3>Mineurs</h3>
      <p
        v-for="volunteer in main.volunteers
          .filter((volunteer) => volunteer.minor)
          .sort((a, b) => (a.lastname < b.lastname ? -1 : a.lastname == b.lastname ? 0 : 1))"
        :key="volunteer.id"
      >
        {{ volunteer.firstname }} {{ volunteer.lastname }} ({{ volunteer.department }})
      </p>
      <p v-if="main.volunteers.filter((volunteer) => volunteer.minor).length == 0">Aucun mineur</p>
    </v-card>
    <v-card variant="outlined">
      <h3>Attention ne veut pas</h3>
      <h4>Binome</h4>
      <p
        v-for="volunteer in main.volunteers
          .filter((volunteer) => volunteer.mission_restrictions?.includes('BINOME'))
          .sort((a, b) => (a.lastname < b.lastname ? -1 : a.lastname == b.lastname ? 0 : 1))"
        :key="volunteer.id"
      >
        {{ volunteer.firstname }} {{ volunteer.lastname }} ({{ volunteer.department }})
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
          .sort((a, b) => (a.lastname < b.lastname ? -1 : a.lastname == b.lastname ? 0 : 1))"
        :key="volunteer.id"
      >
        {{ volunteer.firstname }} {{ volunteer.lastname }} ({{ volunteer.department }})
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
          .sort((a, b) => (a.lastname < b.lastname ? -1 : a.lastname == b.lastname ? 0 : 1))"
        :key="volunteer.id"
      >
        {{ volunteer.firstname }} {{ volunteer.lastname }} ({{ volunteer.department }})
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
    <v-card variant="outlined">
      <h3>Restrictions alimentaires</h3>
      <p
        v-for="volunteer in main.volunteers
          .filter((volunteer) => volunteer.food_restrictions)
          .sort((a, b) => (a.lastname < b.lastname ? -1 : a.lastname == b.lastname ? 0 : 1))"
        :key="volunteer.id"
      >
        {{ volunteer.firstname }} {{ volunteer.lastname }} ({{ volunteer.department }}):
        {{ volunteer.food_restrictions?.join(', ') }}
      </p>
      <p v-if="main.volunteers.filter((volunteer) => volunteer.food_restrictions).length == 0">
        Aucune personne avec des restrictions alimentaires
      </p>
    </v-card>
  </v-sheet>
  <v-sheet v-else id="main">Waiting for data ...</v-sheet>
</template>

<style scoped>
#main {
  max-width: 800px;
  padding: 15px;
  margin: auto;
}

h3 {
  margin-bottom: 15px;
}
.v-card {
  padding: 10px;
  margin: 10px 0;
}

h4 {
  margin-top: 10px;
}
</style>
