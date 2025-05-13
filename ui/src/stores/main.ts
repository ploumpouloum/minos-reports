import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'
import type { Assignment, Shift, Station, Volunteer } from '@/types/main'
import { handleDates } from '@/utils'
import { isEqual, startOfDay } from 'date-fns'
import { stationsRolesOrder, stationsRolesMaps } from '@/constants'

axios.interceptors.response.use((rep) => {
  handleDates(rep.data)
  return rep
})

export type RootState = {
  snackbarShown: boolean
  snackbarText: string
  whoami: string
  assignments: Assignment[]
  shifts: Shift[]
  stations: Station[]
  volunteers: Volunteer[]
  isSupervisor: boolean
  isDlus: boolean
  myVolunteerId: string | null
  dataLoaded: boolean
  isLoading: boolean
  errorMessage: string
  errorDetails: string
  stationsRoles: string[]
  volunteersRoles: string[]
}

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      snackbarShown: false,
      snackbarText: '',
      whoami: '',
      assignments: [],
      shifts: [],
      stations: [],
      volunteers: [],
      isSupervisor: false,
      isDlus: false,
      myVolunteerId: null,
      dataLoaded: false,
      isLoading: false,
      errorMessage: '',
      errorDetails: '',
      stationsRoles: [],
      volunteersRoles: []
    }) as RootState,
  getters: {
    startDays(state) {
      return Array.from(
        new Set(state.shifts.map((shift: Shift) => startOfDay(shift.startDateTime).getTime()))
      )
        .sort()
        .map((timestamp: number) => new Date(timestamp))
    },
    volunteersPresent(state) {
      return (day: Date): Volunteer[] => {
        return state.volunteers.filter(
          (volunteer: Volunteer) =>
            startOfDay(volunteer.incoming_date_time) <= day &&
            startOfDay(volunteer.outgoing_date_time) >= day &&
            !isEqual(volunteer.outgoing_date_time, day)
        )
      }
    },
    getShifts(state) {
      return (day: Date): Shift[] => {
        return state.shifts
          .filter((shift: Shift) => isEqual(startOfDay(shift.startDateTime), day))
          .sort(function (shift1: Shift, shift2: Shift) {
            return (
              new Date(shift1.startDateTime).getTime() - new Date(shift2.startDateTime).getTime()
            )
          })
      }
    },
    getShiftsWithManques(state) {
      return (day: Date, showComplet: boolean): Shift[] => {
        return state.shifts
          .filter(
            (shift: Shift) =>
              isEqual(startOfDay(shift.startDateTime), day) &&
              (Object.keys(this.getManques(shift.id)).length > 0 || showComplet)
          )
          .sort(function (shift1: Shift, shift2: Shift) {
            return (
              new Date(shift1.startDateTime).getTime() - new Date(shift2.startDateTime).getTime()
            )
          })
      }
    },
    getShift(state) {
      return (shiftId: string): Shift => {
        return state.shifts.filter((shift: Shift) => shift.id == shiftId)[0]
      }
    },
    getStation(state) {
      return (stationId: string): Station => {
        return state.stations.filter((station: Station) => station.id == stationId)[0]
      }
    },
    getVolunteer(state) {
      return (volunteerId: string): Volunteer => {
        return state.volunteers.filter((volunteer: Volunteer) => volunteer.id == volunteerId)[0]
      }
    },
    getVolunteerByNivol(state) {
      return (nivol: string): Volunteer => {
        return state.volunteers.filter((volunteer: Volunteer) => volunteer.nivol == nivol)[0]
      }
    },
    getVolunteerAssignmentsDays(state) {
      return (volunteerId: string): Date[] => {
        return Array.from(
          new Set(
            state.assignments
              .filter((assignment: Assignment) => assignment.volunteerId == volunteerId)
              .map((assignment: Assignment) =>
                startOfDay(this.getShift(assignment.shiftId).startDateTime).getTime()
              )
          )
        )
          .sort()
          .map((timestamp: number) => new Date(timestamp))
      }
    },
    getVolunteerAssignmentsByDay(state) {
      return (volunteerId: string, day: Date): Assignment[] => {
        return state.assignments
          .filter(
            (assignment: Assignment) =>
              assignment.volunteerId == volunteerId &&
              isEqual(startOfDay(this.getShift(assignment.shiftId).startDateTime), day)
          )
          .sort(
            (a, b) =>
              this.getShift(a.shiftId).startDateTime.getTime() -
              this.getShift(b.shiftId).startDateTime.getTime()
          )
      }
    },
    getVolunteerAssignments(state) {
      return (volunteerId: string): Assignment[] => {
        return state.assignments
          .filter((assignment: Assignment) => assignment.volunteerId == volunteerId)
          .sort(
            (a, b) =>
              this.getShift(a.shiftId).startDateTime.getTime() -
              this.getShift(b.shiftId).startDateTime.getTime()
          )
      }
    },
    getShiftAssignments(state) {
      return (shiftId: string): Assignment[] => {
        return state.assignments.filter((assignment: Assignment) => assignment.shiftId == shiftId)
      }
    },
    getManques(state) {
      return (shiftId: string, total: boolean = false): { [dict_key: string]: number } => {
        return state.assignments
          .filter(
            (assignment: Assignment) =>
              assignment.shiftId == shiftId && (total || !assignment.volunteerId)
          )
          .reduce((manques: { [dict_key: string]: number }, assignment) => {
            manques[assignment.role] = (manques[assignment.role] || 0) + 1
            return manques
          }, {})
      }
    },
    getTotalManques(state) {
      return (
        day: Date,
        showComplet: boolean,
        total: boolean = false
      ): { [dict_key: string]: number } => {
        const shifts = this.getShiftsWithManques(day, showComplet)
        return state.assignments
          .filter(
            (assignment: Assignment) =>
              shifts.some((shift) => assignment.shiftId == shift.id) &&
              (total || !assignment.volunteerId)
          )
          .reduce((manques: { [dict_key: string]: number }, assignment) => {
            manques[assignment.role] = (manques[assignment.role] || 0) + 1
            return manques
          }, {})
      }
    }
  },
  actions: {
    async fetchData(force: boolean = false) {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      if (!force && this.dataLoaded) {
        return
      }

      return Promise.all([
        axios.get(this.config.backend_api + '/whoami'),
        axios.get(this.config.backend_api + '/data')
      ]).then(
        ([whoami_response, data_response]) => {
          this.whoami = whoami_response.data
          this.isLoading = false
          this.volunteers = data_response.data['volunteers'] as Volunteer[]
          this.shifts = data_response.data['shifts'] as Shift[]
          this.stations = data_response.data['stations'] as Station[]
          this.assignments = data_response.data['assignments'] as Assignment[]
          this.isSupervisor = data_response.data['isSupervisor']
          this.isDlus = data_response.data['isDlus']
          this.myVolunteerId = data_response.data['myVolunteerId']
          this.dataLoaded = true
          this.volunteersRoles = Array.from(
            new Set(...this.volunteers.map((volunteer) => volunteer.roles))
          )
          this.stationsRoles = Array.from(
            new Set(this.assignments.map((assignment) => assignment.role))
          ).sort(function (a, b) {
            return (
              stationsRolesOrder.indexOf(stationsRolesMaps[a]) -
              stationsRolesOrder.indexOf(stationsRolesMaps[b])
            )
          })
        },
        (error) => {
          this.isLoading = false
          this.volunteers = []
          this.shifts = []
          this.stations = []
          this.assignments = []
          this.isSupervisor = false
          this.isDlus = false
          this.myVolunteerId = null
          this.errorMessage = 'Failed to load data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    checkResponseObject(response: unknown, msg: string = '') {
      if (response === null || typeof response !== 'object') {
        if (msg !== '') {
          this.errorDetails = msg
        }
        throw new Error('Invalid response object.')
      }
    },
    handleAxiosError(error: AxiosError<object>) {
      if (axios.isAxiosError(error) && error.response) {
        const status = error.response.status
        switch (status) {
          case 400:
            this.errorDetails =
              'HTTP 400: Bad Request. The server could not understand the request.'
            break
          case 404:
            this.errorDetails =
              'HTTP 404: Not Found. The requested resource could not be found on the server.'
            break
          case 500:
            this.errorDetails =
              'HTTP 500: Internal Server Error. The server encountered an unexpected error.'
            break
        }
      }
    },
    setErrorMessage(message: string) {
      this.errorMessage = message
    }
  }
})
