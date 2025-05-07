<script setup lang="ts">
import { ref } from 'vue'
import type { Ref, PropType } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Assignment, Volunteer } from '@/types/main'
import { stationsRolesMaps } from '@/constants'

const main = useMainStore()

const props = defineProps({
  assignment: {
    type: Object as PropType<Assignment>,
    required: true
  }
})

const volunteer: Ref<Volunteer | null> = ref(
  props.assignment.volunteerId ? main.getVolunteer(props.assignment.volunteerId) : null
)
</script>

<template>
  <td class="role">{{ stationsRolesMaps[props.assignment.role] }}</td>
  <td colspan="3">
    <router-link v-if="volunteer" :to="`/volunteer/${volunteer.nivol}`">
      {{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }})
    </router-link>
    <template v-else>Non affecté</template>
  </td>
</template>

<style lang="css" scoped>
td {
  border: 1px #717171 solid;
}
</style>
