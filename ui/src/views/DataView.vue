<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { ref } from 'vue'
import axios from 'axios'
import StationsKind from '@/components/StationsKind.vue'

const main = useMainStore()

const volontairesFileInput = ref()
const affectationFileInput = ref()

const updateData = () => {
  if (!volontairesFileInput.value) {
    main.snackbarText = 'Le fichier des volontaires est obligatoire'
    main.snackbarShown = true
    return
  }
  if (!affectationFileInput.value) {
    main.snackbarText = 'Le fichier des affectations est obligatoire'
    main.snackbarShown = true
    return
  }
  main.snackbarText = 'Import en cours'
  main.snackbarShown = true
  main.isUpdating = true
  axios
    .delete(main.config.backend_api + '/data')
    .then(() => {
      const formData = new FormData()
      formData.append('file', volontairesFileInput.value)
      return axios.post(main.config.backend_api + '/uploadvolontaires/', formData)
    })
    .then(() => {
      const formData = new FormData()
      formData.append('file', affectationFileInput.value)
      return axios.post(main.config.backend_api + '/uploadaffectation/', formData)
    })
    .then(() => main.fetchData(true))
    .then(
      () => {
        main.isUpdating = false
        main.snackbarText = 'Import terminé'
        main.snackbarShown = true
      },
      (error) => {
        main.isUpdating = false
        console.error(error)
        main.snackbarText = 'Une erreur est survenue'
        main.snackbarShown = true
      }
    )
}
</script>

<template>
  <v-sheet v-if="!main.dataLoaded" id="main">
    <p>
      Loading data ...
      <v-progress-circular color="primary" indeterminate></v-progress-circular>
    </p>
  </v-sheet>
  <v-sheet v-else id="main">
    <v-card variant="outlined">
      <h3>Fichier MINOS des volontaires</h3>
      <v-file-input
        label="File input"
        variant="outlined"
        v-model="volontairesFileInput"
      ></v-file-input>
      <h3>Fichier MINOS des affectations</h3>
      <v-file-input
        label="File input"
        variant="outlined"
        v-model="affectationFileInput"
      ></v-file-input>
      <v-btn :disabled="main.isUpdating" @click="updateData" variant="outlined">Importer</v-btn>
    </v-card>
    <v-card variant="outlined">
      <h3>Types des postes</h3>
      <StationsKind />
    </v-card>
  </v-sheet>
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
</style>
