<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Volunteer } from '../types/main.ts'

const main = useMainStore()

const props = defineProps({
  role: {
    type: String,
    required: true
  },
  volunteerId: {
    type: String,
    required: false
  },
  skipVolunteerId: {
    type: String,
    required: false
  }
})

const volunteer: Ref<Volunteer | null> = ref(
  props.volunteerId ? main.getVolunteer(props.volunteerId) : null
)
</script>

<template>
  <template v-if="!volunteerId || volunteerId != skipVolunteerId">
    <span v-if="volunteer"
      >{{ volunteer.firstname }} {{ volunteer.lastname }} ({{ volunteer.department }},
      {{ props.role }})</span
    >
    <span v-else>{{ props.role }}</span>
    <span>, </span>
  </template>
</template>

<style lang="css" scoped>
#activities {
  margin-left: 1rem;
}

span:last-child {
  display: none;
}
</style>
