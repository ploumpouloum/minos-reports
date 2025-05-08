<script setup lang="ts">
import { computed } from 'vue'
import { useMainStore } from '@/stores/main'
import ManquesShiftDetail from '@/components/ManquesShiftDetail.vue'
import { stationsRolesMaps } from '@/constants'

const main = useMainStore()

const props = defineProps({
  day: {
    type: Date,
    required: true
  },
  showComplet: {
    type: Boolean,
    required: true
  }
})

const manques = computed(() => {
  return main.getTotalManques(props.day, props.showComplet)
})
const manquesTotals = computed(() => {
  return main.getTotalManques(props.day, props.showComplet, true)
})
</script>

<template>
  <th v-for="role in main.stationsRoles" :key="role">
    {{ stationsRolesMaps[role] }}
    <br />
    <ManquesShiftDetail :total="manquesTotals[role] || NaN" :manque="manques[role] || NaN" />
  </th>
</template>

<style scoped lang="css">
th {
  border: 1px solid black;
  background-color: #717171;
  color: white;
  width: 5%;
  line-height: 1.4rem;
}
</style>
