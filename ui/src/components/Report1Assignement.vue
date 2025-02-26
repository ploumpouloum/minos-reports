<script setup lang="ts">
import { ref } from 'vue'
import type { Ref, PropType } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Assignment, Volunteer } from '@/types/main'

const main = useMainStore()

const props = defineProps({
  assignment: {
    type: Object as PropType<Assignment>,
    required: true
  }
})

const volunteer: Ref<Volunteer | null> = ref(main.getVolunteer(props.assignment.volunteerId))
</script>

<template>
  <td class="role">{{ props.assignment.role }}</td>
  <td>
    <router-link :to="`/mission/${volunteer?.nivol} `">
      {{ volunteer?.firstname }} {{ volunteer?.lastname }}
    </router-link>
  </td>
</template>

<style lang="css">
.role {
  width: 100px;
}
</style>
