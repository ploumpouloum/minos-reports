<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import Report1Shift from '../components/Report1Shift.vue'

const main = useMainStore()

main.fetchData()
</script>

<template>
  <div class="report">
    <template v-for="startDay in main.startDays" :key="startDay">
      <div class="shift" v-for="(shift, index) in main.getShifts(startDay)" :key="shift.id">
        <div class="day" v-if="index == 0">
          {{ new Date(startDay).toLocaleDateString('fr-FR', { day: '2-digit', month: 'long' }) }}
        </div>
        <Report1Shift :shiftId="shift.id" />
      </div>
    </template>
  </div>
</template>

<style scoped lang="css">
.report {
  display: flex;
  flex-flow: column wrap;
  height: calc(100vh - 80px);
}

.report > * {
  margin-left: 30px;
  margin-right: 30px;
}

.shift {
  width: 300px;
}

.break {
  flex-basis: 100%;
  width: 0;
}

.day {
  background-color: #e40613;
  color: white;
  text-align: center;
  margin-bottom: 10px;
}
</style>
