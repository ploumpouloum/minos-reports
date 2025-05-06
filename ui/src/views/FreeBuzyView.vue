<script setup lang="ts">
import FreeBuzyDay from '@/components/FreeBuzyDay.vue'
import { useMainStore } from '@/stores/main'

const main = useMainStore()

main.fetchData()
</script>

<template>
  <v-sheet id="main">
    <v-card variant="outlined" v-for="day in main.startDays" :key="day.toISOString()">
      <FreeBuzyDay :day="day" />
    </v-card>
  </v-sheet>
</template>

<style scoped>
#main {
  display: flex;
  flex-direction: column;
  margin: 0 15px;
}

.v-card {
  margin-bottom: 15px;
}
</style>
