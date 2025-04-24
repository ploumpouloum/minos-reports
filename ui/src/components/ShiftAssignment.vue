<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Volunteer } from '../types/main.ts'

const main = useMainStore()

const props = defineProps({
  volunteerId: {
    type: String,
    required: true
  },
  role: {
    type: String,
    required: true
  }
})

const volunteer: Ref<Volunteer | null> = ref(
  props.volunteerId ? main.getVolunteer(props.volunteerId) : null
)
</script>

<template>
  <div v-if="main.dataLoaded && volunteer">
    {{ props.role }} {{ volunteer.firstname }} {{ volunteer.lastname }} ({{ volunteer.department }})
  </div>
  <div v-else>Volunteer not found</div>
</template>

<style lang="css" scoped>
div {
  margin: 10px 0;
}
</style>
