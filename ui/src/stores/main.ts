import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'
import type { Assignment, Shift, Station, Volunteer } from '@/types/main'

export type RootState = {
  assignments: Assignment[]
  shifts: Shift[]
  stations: Station[]
  volunteers: Volunteer[]
  isLoading: boolean
  errorMessage: string
  errorDetails: string
}

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      assignments: [],
      shifts: [],
      stations: [],
      volunteers: [],
      isLoading: false,
      errorMessage: '',
      errorDetails: ''
    }) as RootState,
  getters: {
    startDays(state) {
      return new Set(
        state.shifts.map((shift: Shift) => shift.startDateTime.split('T')[0])
      )
    },
    getShifts(state) {
      return (day: string): Shift[] => {
        return state.shifts.filter(
          (shift: Shift) => shift.startDateTime.split('T')[0] == day
        ).sort(function (shift1: Shift, shift2: Shift) { return new Date(shift1.startDateTime).getTime() - new Date(shift2.startDateTime).getTime() })
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
    getShiftAssignments(state) {
      return (shiftId: string): Assignment[] => {
        return state.assignments.filter(
          (assignment: Assignment) => assignment.shiftId == shiftId
        )
      }
    }
  },
  actions: {
    async fetchData() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('http://127.0.0.1:61010/data').then(
        (response) => {
          this.isLoading = false
          console.log(response.data["stations"])
          this.volunteers = response.data["volunteers"] as Volunteer[]
          this.shifts = response.data["shifts"] as Shift[]
          this.stations = response.data["stations"] as Station[]
          this.assignments = response.data["assignments"] as Assignment[]
        },
        (error) => {
          this.isLoading = false
          this.volunteers = []
          this.shifts = []
          this.stations = []
          this.assignments = []
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
