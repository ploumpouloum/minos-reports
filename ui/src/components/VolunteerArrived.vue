<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { ref, watch } from 'vue'
import axios from 'axios'

const main = useMainStore()

const props = defineProps({
  nivol: {
    type: String,
    required: true
  },
  initialArrived: {
    type: Boolean,
    required: false
  }
})

const arrived = ref(props.initialArrived)

watch(
  () => arrived.value,
  () => setVolunteerArrived()
)

const setVolunteerArrived = function () {
  main.isUpdating = true
  main.snackbarText = 'Modification en cours'
  main.snackbarShown = true
  const volunteer = main.getVolunteerByNivol(props.nivol)
  volunteer.arrived = arrived.value
  axios
    .post(main.config.backend_api + '/volunteer_status/', {
      nivol: props.nivol,
      arrived: arrived.value
    })
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
  <v-switch v-model="arrived" color="green-lighten-1" label="Arrivé(e)" hide-details></v-switch>
</template>
