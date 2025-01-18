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

const volunteer: Ref<Volunteer | null> = ref(main.getVolunteer(props.assignment.idVolunteer))
</script>

<template>
  <td class="role">{{ props.assignment.role }}</td>
  <td>{{ volunteer?.firstname }} {{ volunteer?.lastname }}</td>
</template>

<style lang="css">
.role {
  width: 100px;
}
</style>
