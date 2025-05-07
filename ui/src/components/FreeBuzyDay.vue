<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { FreeBusyStatus, type Volunteer } from '@/types/main'
import { addHours, addMinutes } from 'date-fns'

const main = useMainStore()

const props = defineProps({
  day: {
    type: Date,
    required: true
  }
})

const getFreeBusyStatus = function (
  volunteer: Volunteer,
  hour: number,
  minute: number
): FreeBusyStatus {
  const currentDate = addMinutes(addHours(props.day, hour), minute)
  if (volunteer.incoming_date_time > currentDate) {
    return FreeBusyStatus.NotAvailable
  }
  if (volunteer.outgoing_date_time <= currentDate) {
    return FreeBusyStatus.NotAvailable
  }

  for (const assignement of main.getVolunteerAssignments(volunteer.id)) {
    const shift = main.shifts.filter((shift) => shift.id == assignement.shiftId)[0]

    if (shift.startDateTime <= currentDate && shift.endDateTime >= currentDate) {
      return FreeBusyStatus.Busy
    }
  }
  return FreeBusyStatus.Free
}

const getFreeBusyClass = function (status: FreeBusyStatus) {
  if (status == FreeBusyStatus.Busy) {
    return 'busy'
  } else if (status == FreeBusyStatus.Free) {
    return 'free'
  } else if (status == FreeBusyStatus.NotAvailable) {
    return 'na'
  } else {
    throw Error(`Unknow status ${status}`)
  }
}
</script>

<template>
  <div class="container">
    <div class="header">
      <h2>
        {{
          props.day.toLocaleDateString('fr-FR', {
            weekday: 'long',
            day: '2-digit',
            month: 'long'
          })
        }}
      </h2>
      <div class="table">
        <div class="full-header">Volontaire</div>
        <div
          class="column-header"
          v-for="hour in Array.from({ length: 24 }, (v, k) => k)"
          :key="hour"
        >
          {{ hour }}
        </div>
      </div>
    </div>
    <div class="table">
      <template v-for="volunteer in main.volunteersPresent(props.day)" :key="volunteer.id">
        <div class="row-header">
          {{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department }})
        </div>
        <template v-for="hour in Array.from({ length: 24 }, (v, k) => k)" :key="hour">
          <div
            class="fb-cell"
            :class="[getFreeBusyClass(getFreeBusyStatus(volunteer, hour, 0))]"
          ></div>
          <div
            class="fb-cell"
            :class="[getFreeBusyClass(getFreeBusyStatus(volunteer, hour, 30))]"
          ></div>
        </template>
      </template>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow-y: auto;
  padding: 0 25px;
  margin: 10px 5px;
}
h2 {
  padding-bottom: 10px;
}
.header {
  text-align: center;
  position: sticky;
  z-index: 1;
  background-color: white;
  top: 0;
}
.fb-cell {
  outline: 1px solid black;
}
.fb-cell.free {
  background-color: green;
}
.fb-cell.busy {
  background-color: red;
}
.fb-cell.na {
  background-color: gray;
}

.table {
  display: grid;
  gap: 1px;
  grid-template-columns: 10rem repeat(48, minmax(0, 1fr));
  width: 100%;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.row-header {
  justify-content: right;
  text-align: right;
  padding-right: 1rem;
  min-width: 10rem;
  font-size: 0.8rem;
  min-height: 1.4rem;
  align-items: center;
  display: flex;
}

.full-header {
  text-align: right;
  padding-right: 1rem;
  font-weight: bold;
}

.column-header {
  grid-column: span 2;
  font-weight: bold;
  font-size: 0.9rem;
  text-align: left;
}

@media print {
  #main {
    max-height: none;
    overflow: visible;
  }
}
</style>
