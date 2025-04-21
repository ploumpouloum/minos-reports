<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { useRouter } from 'vue-router'

const router = useRouter()

const main = useMainStore()

main.fetchData().then(() => {
  if (main.isSupervisor) {
    router.push({
      name: 'restrictions'
    })
  }
  if (main.isDlus) {
    router.push({
      name: 'volunteers'
    })
  }
})
</script>

<template>
  <v-sheet id="main">
    <v-card variant="outlined">
      <p>Bienvenue à la MaxiRace 2025 à Annecy !</p>
      <p>
        Il semble que tu n'es pas (encore ?) inscrit.e à la MaxiRace, et si tu es DLUS, personne de
        ton UL ne s'est encore inscrit avec ton mail comme validateur.
      </p>
    </v-card>
  </v-sheet>
</template>

<style scoped lang="css">
#main {
  max-width: 800px;
  padding: 15px;
  margin: auto;
}
.v-card {
  min-height: 200px;
  padding: 10px;
  margin: 10px 0;
}
p {
  padding: 1rem 0 2rem;
}
</style>
