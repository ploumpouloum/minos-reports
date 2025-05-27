<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { ref, watch } from 'vue'
import axios from 'axios'

const main = useMainStore()

const props = defineProps({
  label: {
    type: String,
    required: true
  },
  initialKind: {
    type: String,
    required: false
  }
})

const kind = ref(props.initialKind)

watch(
  () => kind.value,
  () => setStationKind()
)

const setStationKind = function () {
  main.isUpdating = true
  main.snackbarText = 'Modification en cours'
  main.snackbarShown = true
  axios
    .post(main.config.backend_api + '/station_kind/', { label: props.label, kind: kind.value })
    .then(
      () => {
        main.isUpdating = false
        main.snackbarText = 'Modification enregistrée'
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
  {{ props.label }}
  <v-btn-toggle v-model="kind" base-color="grey-lighten-3" class="ma-2" group>
    <v-btn color="#1565C0" value="VPS">VPS</v-btn>
    <v-btn color="#2E7D32" value="Poste Fixe">Poste Fixe</v-btn>
    <v-btn color="#990000" value="Logistique">Logistique</v-btn>
  </v-btn-toggle>
</template>

<style lang="css" scoped>
li {
  list-style-type: none;
}
</style>
