<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useMainStore } from '@/stores/main'
import VacationsAssignement from './VacationsAssignement.vue'
import type { Station, Shift } from '../types/main.ts'
import { addMinutes } from '@/utils.ts'

const main = useMainStore()

const props = defineProps({
  shiftId: {
    type: String,
    required: true
  }
})

const shift: Ref<Shift | null> = ref(main.getShift(props.shiftId))
const station: Ref<Station | null> = ref(
  shift.value ? main.getStation(shift.value.stationId) : null
)

const localeHour = (date: Date) =>
  date.toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit'
  })
</script>

<template>
  <div v-if="shift && station">
    <table cellspacing="0">
      <tbody>
        <tr
          class="station"
          :class="{
            'vps-station': station.kind == 'VPS',
            'poste-fixe-station': station.kind == 'Poste Fixe',
            'logistique-station': station.kind == 'Logistique'
          }"
        >
          <td colspan="4">{{ station.label }}</td>
        </tr>
        <tr class="hours-titles">
          <td>RDV CGMS</td>
          <td>DEPART CGMS</td>
          <td>DEBUT POSTE</td>
          <td>FIN POSTE</td>
        </tr>
        <tr>
          <td>{{ localeHour(shift.meetDateTime) }}</td>
          <td>{{ localeHour(addMinutes(shift.meetDateTime, 30)) }}</td>
          <td>{{ localeHour(shift.startDateTime) }}</td>
          <td>{{ localeHour(shift.endDateTime) }}</td>
        </tr>
        <tr class="separator">
          <td colspan="4"></td>
        </tr>
        <tr
          class="assignements"
          v-for="assignment in main.getShiftAssignments(shift.id)"
          :key="assignment.id"
        >
          <VacationsAssignement :assignment="assignment" />
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else>Shift or station not found</div>
</template>

<style lang="css" scoped>
table {
  margin-bottom: 2rem;
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

.station {
  background-color: #aaaaaa;
  color: white;
  font-weight: bold;
}

.station.logistique-station {
  background-color: #990000;
}

.station.vps-station {
  background-color: #1565c0;
}

.station.poste-fixe-station {
  background-color: #2e7d32;
}

.station td {
  padding: 0.2rem 0;
}

.hours-titles {
  background-color: #434343;
  color: white;
  font-size: 0.6rem;
}

.hours-titles td {
  padding: 0.2rem 0;
  width: 25%;
}

td {
  border: 1px #717171 solid;
}

tr.assignements:nth-child(even) {
  background-color: #f2f2f2;
}

tr.separator {
  height: 1rem;
}

h4 {
  font-size: 1rem;
  text-align: center;
}
</style>
