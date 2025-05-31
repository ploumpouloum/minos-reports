<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import VacationsShift from '../components/VacationsShift.vue'

const main = useMainStore()

const getDayId = function (date: Date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `day-${year}-${month}-${day}`
}
</script>

<template>
  <div v-if="!main.dataLoaded" id="main">
    <p>
      Loading data ...
      <v-progress-circular color="primary" indeterminate></v-progress-circular>
    </p>
  </div>
  <v-sheet v-else-if="!main.isSupervisor" id="main">Cet écran est réservé aux superviseurs</v-sheet>
  <div v-else>
    <div
      :id="getDayId(startDay)"
      class="day-block"
      v-for="startDay in main.startDays.filter(
        (date) => getDayId(date).localeCompare(getDayId(new Date())) >= 0
      )"
      :key="startDay.toISOString()"
    >
      <div class="day">
        {{
          startDay.toLocaleDateString('fr-FR', { weekday: 'long', day: '2-digit', month: 'long' })
        }}
      </div>
      <div class="shifts">
        <div class="shift" v-for="shift in main.getShifts(startDay)" :key="shift.id">
          <VacationsShift :volunteersClickable="true" :shiftId="shift.id" />
        </div>
      </div>
    </div>
    <hr />
    <h3>Journées passées</h3>
    <div
      :id="getDayId(startDay)"
      class="day-block"
      v-for="startDay in main.startDays.filter(
        (date) => getDayId(date).localeCompare(getDayId(new Date())) < 0
      )"
      :key="startDay.toISOString()"
    >
      <div class="day">
        {{
          startDay.toLocaleDateString('fr-FR', { weekday: 'long', day: '2-digit', month: 'long' })
        }}
      </div>
      <div class="shifts">
        <div class="shift" v-for="shift in main.getShifts(startDay)" :key="shift.id">
          <VacationsShift :volunteersClickable="true" :shiftId="shift.id" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="css">
.shifts {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1rem;
  margin: 1rem;
}

@media (min-width: 640px) {
  .shifts {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (min-width: 1024px) {
  .shifts {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (min-width: 1440px) {
  .shifts {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
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

hr {
  color: red;
  margin-bottom: 1rem;
}

h3 {
  text-align: center;
  padding-bottom: 1rem;
}
</style>
