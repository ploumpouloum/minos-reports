<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import ManquesShift from '@/components/ManquesShift.vue'
import { ref } from 'vue'
import ManquesShiftTotal from '@/components/ManquesShiftTotal.vue'

const main = useMainStore()

main.fetchData()

const showComplet = ref(false)
</script>

<template>
  <div v-if="!main.dataLoaded" class="report">
    <p>
      Loading data ...
      <v-progress-circular color="primary" indeterminate></v-progress-circular>
    </p>
  </div>
  <div v-else class="report">
    <div
      v-for="startDay in main.startDays.filter(
        (startDay) => main.getShiftsWithManques(startDay, showComplet).length > 0
      )"
      :key="startDay.toISOString()"
    >
      <div class="day">
        <b></b>
      </div>
      <table cellspacing="0">
        <thead>
          <tr>
            <th class="noborder">
              {{
                startDay.toLocaleDateString('fr-FR', {
                  weekday: 'long',
                  day: '2-digit',
                  month: 'long'
                })
              }}
            </th>
            <ManquesShiftTotal :day="startDay" :showComplet="showComplet" />
          </tr>
        </thead>
        <tbody>
          <ManquesShift
            v-for="shift in main.getShiftsWithManques(startDay, showComplet)"
            :key="shift.id"
            :shiftId="shift.id"
            :showComplet="showComplet"
          />
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
input {
  margin-right: 6px;
  margin-bottom: 12px;
}
.report {
  margin-left: 30px;
  margin-right: 30px;
}

.day {
  background-color: #e40613;
  color: white;
  text-align: center;
  margin-bottom: 10px;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

table {
  margin-bottom: 10px;
  width: 100%;
  border-collapse: collapse;
}

th.noborder {
  border: none;
  background-color: transparent;
  width: auto;
  color: black;
  text-align: right;
  padding: 0 1rem;
}

.help {
  margin: 0.8rem 3rem;
  font-size: 0.9rem;
  line-height: 1rem;
}
</style>
