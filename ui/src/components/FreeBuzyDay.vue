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
  <div id="main">
    <h2>
      {{
        props.day.toLocaleDateString('fr-FR', {
          weekday: 'long',
          day: '2-digit',
          month: 'long'
        })
      }}
    </h2>
    <table>
      <thead>
        <tr>
          <th>Volontaire</th>
          <th
            class="fb-cell"
            colspan="2"
            v-for="hour in Array.from({ length: 24 }, (v, k) => k)"
            :key="hour"
          >
            {{ hour }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="volunteer in main.volunteersPresent(props.day)" :key="volunteer.id">
          <td>{{ volunteer.firstname }} {{ volunteer.lastname }}</td>
          <template v-for="hour in Array.from({ length: 24 }, (v, k) => k)" :key="hour">
            <td class="fb-cell" :class="[getFreeBusyClass(getFreeBusyStatus(volunteer, hour, 0))]">
              &nbsp;
            </td>
            <td class="fb-cell" :class="[getFreeBusyClass(getFreeBusyStatus(volunteer, hour, 30))]">
              &nbsp;
            </td>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
#main {
  overflow: scroll;
}
h2 {
  text-align: center;
  padding-bottom: 10px;
}
table {
  table-layout: fixed;
  width: 1350px;
  border-spacing: 0;
  margin: 0 auto;
}
th.fb-cell {
  width: 48px;
  text-align: left;
}
td.fb-cell {
  width: 24px;
  border: 1px solid black;
}
td.fb-cell.free {
  background-color: green;
}
td.fb-cell.busy {
  background-color: red;
}
td.fb-cell.na {
  background-color: gray;
}
</style>
