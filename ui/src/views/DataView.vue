<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { ref } from 'vue'
import axios from 'axios'

const main = useMainStore()

const snackbarShown = ref(false)
const snackbarText = ref('')

const volontairesFileInput = ref()
// const affectationFileInput = ref()

const deleteAllData = () => {
  main.deleteAllData().then(
    () => {
      snackbarText.value = 'Data deleted'
      snackbarShown.value = true
    },
    (error) => {
      console.error(error)
      snackbarText.value = 'Error occured'
      snackbarShown.value = true
    }
  )
}

const uploadVolontaires = () => {
  const formData = new FormData()
  formData.append('file', volontairesFileInput.value)
  axios.post(main.config.backend_api + '/uploadvolontaires/', formData).then(
    () => {
      snackbarText.value = 'Data loaded'
      snackbarShown.value = true
    },
    (error) => {
      console.error(error)
      snackbarText.value = 'Error occured'
      snackbarShown.value = true
    }
  )
}

// const uploadAffectation = () => {
//   const formData = new FormData()
//   formData.append('file', affectationFileInput.value)
//   axios.post(main.config.backend_api + '/uploadaffectation/', formData)
// }
</script>

<template>
  <v-sheet id="main">
    <v-card variant="outlined">
      <h3>Effacer toutes les données</h3>
      <v-btn @click="deleteAllData" variant="outlined">Tout effacer</v-btn>
    </v-card>
    <v-card variant="outlined">
      <h3>Importer les volontaires</h3>
      <v-file-input
        label="File input"
        variant="outlined"
        v-model="volontairesFileInput"
      ></v-file-input>
      <v-btn @click="uploadVolontaires" variant="outlined">Importer</v-btn>
    </v-card>
    <!--
    <v-card variant="outlined">
      <h3>Importer les affectations</h3>
      <v-file-input
        label="File input"
        variant="outlined"
        v-model="affectationFileInput"
      ></v-file-input>
      <v-btn @click="uploadAffectation" variant="outlined">Importer</v-btn>
    </v-card>
    -->
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
