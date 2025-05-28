<script setup lang="ts">
import { ref } from 'vue'
import type { Ref, PropType } from 'vue'
import { useMainStore } from '@/stores/main'
import type { Assignment, Volunteer } from '@/types/main'
import { stationsRolesMaps } from '@/constants'
import VolunteerLabel from './VolunteerLabel.vue'

const main = useMainStore()

const props = defineProps({
  assignment: {
    type: Object as PropType<Assignment>,
    required: true
  },
  volunteerClickable: {
    type: Boolean,
    required: false
  },
  currentVolunteer: {
    type: Object as PropType<Volunteer>,
    required: false
  }
})

const volunteer: Ref<Volunteer | null> = ref(
  props.assignment.volunteerId ? main.getVolunteer(props.assignment.volunteerId) : null
)
</script>

<template>
  <td class="role">{{ stationsRolesMaps[props.assignment.role] }}</td>
  <td colspan="3" :class="{ current: currentVolunteer && currentVolunteer == volunteer }">
    <router-link v-if="volunteer && volunteerClickable" :to="`/volunteer/${volunteer.nivol}`">
      <VolunteerLabel :volunteer="volunteer" />
    </router-link>
    <span v-else-if="volunteer && !volunteerClickable">
      <VolunteerLabel :volunteer="volunteer" />
    </span>
    <template v-else>Non affecté</template>
  </td>
</template>

<style lang="css" scoped>
td {
  border: 1px #717171 solid;
}

.current {
  font-weight: bold;
}
</style>
