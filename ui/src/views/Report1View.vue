<script setup lang="ts">
import { watch, ref, nextTick } from 'vue'

import { useMainStore } from '@/stores/main'
import { useRoute } from 'vue-router'
import Report1Station from '../components/Report1Station.vue'

const main = useMainStore()

const route = useRoute()

main.fetchData()
</script>

<template>
  <div class="report">
    <template v-for="startDay in main.startDays">
      <div v-for="(station, index) in main.getStations(startDay)">
        <div class="day" v-if="index==0">
          {{ new Date(startDay).toLocaleDateString('fr-FR', { day: '2-digit', month: 'long' }) }}
        </div>
        <Report1Station :stationId="station.id" />
      </div>
      
    </template>
  </div>
</template>

<style lang="css">
.report {
  display: flex;
  flex-flow: column wrap;
  height: calc(100vh - 80px);
}

.report>* {
  margin-left: 30px;
  margin-right: 30px;
}

.break {
  flex-basis: 100%;
  width: 0;
}

.day {
  background-color: #E40613;
  color: white;
  text-align: center;
  margin-bottom: 10px;
}


</style>
