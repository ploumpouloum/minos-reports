<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { ref } from 'vue'
import axios from 'axios'

const main = useMainStore()

const snackbarShown = ref(false)
const snackbarText = ref('')

const volontairesFileInput = ref()
const affectationFileInput = ref()

const updateData = () => {
  if (!volontairesFileInput.value) {
    snackbarText.value = 'Le fichier des volontaires est obligatoire'
    snackbarShown.value = true
    return
  }
  if (!affectationFileInput.value) {
    snackbarText.value = 'Le fichier des affectations est obligatoire'
    snackbarShown.value = true
    return
  }
  snackbarText.value = 'Import en cours'
  snackbarShown.value = true
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
    .then(
      () => {
        snackbarText.value = 'Import terminé'
        snackbarShown.value = true
      },
      (error) => {
        console.error(error)
        snackbarText.value = 'Une erreur est survenue'
        snackbarShown.value = true
      }
    )
}
</script>

<template>
  <v-sheet id="main">
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
      <v-btn @click="updateData" variant="outlined">Importer</v-btn>
    </v-card>
  </v-sheet>
  <v-snackbar v-model="snackbarShown" timeout="1000">
    {{ snackbarText }}
  </v-snackbar>
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
