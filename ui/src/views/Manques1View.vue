<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import Manques1Shift from '../components/Manques1Shift.vue'
import { ref } from 'vue'

const main = useMainStore()

main.fetchData()

const showComplet = ref(true)
</script>

<template>
  <div class="report">
    <input type="checkbox" id="checkbox" v-model="showComplet" />
    <label for="checkbox">Afficher les postes complets</label>
    <div
      v-for="startDay in main.startDays.filter(
        (startDay) => main.getShiftsWithManques(startDay, showComplet).length > 0
      )"
      :key="startDay.toISOString()"
    >
      <div class="day">
        <b>{{
          new Date(startDay).toLocaleDateString('fr-FR', {
            weekday: 'long',
            day: '2-digit',
            month: 'long'
          })
        }}</b>

        <div v-if="Object.keys(main.getTotalManques(startDay, showComplet)).length > 0">
          <b>{{ main.getShifts(startDay).length }}</b> postes, dont
          <b>{{ main.getShiftsWithManques(startDay, false).length }}</b> non complets ;
          <span
            v-for="(count, role, idx) in main.getTotalManques(startDay, showComplet)"
            :key="role"
            >{{ idx ? ', ' : 'manque ' }}<b>{{ count }}</b> {{ role }}</span
          >
        </div>
        <div v-else>
          <div>
            <b>{{ main.getShifts(startDay).length }}</b> postes, tous complets
          </div>
        </div>
      </div>
      <table cellspacing="0">
        <tbody>
          <Manques1Shift
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
}
</style>
