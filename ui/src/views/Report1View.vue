<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import Report1Shift from '../components/Report1Shift.vue'
import AbbreviationSummary from '@/components/AbbreviationSummary.vue'

const main = useMainStore()

main.fetchData()
</script>

<template>
  <AbbreviationSummary />
  <div class="report">
    <template v-for="startDay in main.startDays" :key="startDay.toISOString()">
      <div class="shift" v-for="(shift, index) in main.getShifts(startDay)" :key="shift.id">
        <div class="day" v-if="index == 0">
          {{
            startDay.toLocaleDateString('fr-FR', { weekday: 'long', day: '2-digit', month: 'long' })
          }}
        </div>
        <Report1Shift :shiftId="shift.id" />
      </div>
    </template>
  </div>
</template>

<style scoped lang="css">
.report {
  margin-top: 1rem;
  display: flex;
  flex-flow: column wrap;
  height: calc(100vh - 12rem);
}

.report > * {
  margin-left: 30px;
  margin-right: 30px;
}

.shift {
  width: 350px;
}

.break {
  flex-basis: 100%;
  width: 0;
}

.day {
  background-color: #e40613;
  padding: 0.5rem 0;
  color: white;
  text-align: center;
  margin-bottom: 10px;
}
</style>
