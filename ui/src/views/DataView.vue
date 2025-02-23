<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { ref } from 'vue'
import axios from 'axios'

const main = useMainStore()

const affectationFileInput = ref()

const uploadAffectation = () => {
  const formData = new FormData()
  formData.append('file', affectationFileInput.value)
  axios.post(main.config.backend_api + '/uploadaffectation/', formData)
}
</script>

<template>
  <v-sheet id="main">
    <v-card variant="outlined">
      <h3>Effacer toutes les données</h3>
      <v-btn @click="main.deleteAllData()" variant="outlined">Tout effacer</v-btn>
    </v-card>
    <v-card variant="outlined">
      <h3>Importer les affectations</h3>
      <v-file-input
        label="File input"
        variant="outlined"
        v-model="affectationFileInput"
      ></v-file-input>
      <!--<input type="file" ref="affectationFileInput" />-->
      <v-btn @click="uploadAffectation" variant="outlined">Importer</v-btn>
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
