<script setup lang="ts">
import { useMainStore } from '@/stores/main'

const main = useMainStore()
</script>

<template>
  <v-sheet v-if="main.dataLoaded" id="main">
    <h2>Liste des inscrits{{ main.isDlus ? ' de votre UL' : '' }}</h2>
    <v-card
      variant="outlined"
      v-for="volunteer in main.volunteers.sort((a, b) => a.lastname.localeCompare(b.lastname))"
      :key="volunteer.id"
    >
      {{ volunteer.firstname }} {{ volunteer.lastname }} ({{ volunteer.department }})
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

.v-card {
  padding: 10px;
  margin: 10px 0;
}
</style>
