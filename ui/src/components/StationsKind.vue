<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import StationKind from './StationKind.vue'

const main = useMainStore()
</script>

<template>
  <ul>
    <li
      v-for="station in main.stations.sort((a, b) => a.label.localeCompare(b.label))"
      :key="station.id"
    >
      <StationKind :label="station.label" :initial-kind="station.kind" />
    </li>
  </ul>
</template>

<style lang="css" scoped>
li {
  list-style-type: none;
}
</style>
