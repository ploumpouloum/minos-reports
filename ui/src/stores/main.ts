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
        state.shifts.map((shift: Shift) => shift.startDateTime.toISOString().split('T')[0])
      )
    },
    getShifts(state) {
      return (day: string): Shift[] => {
        return state.shifts.filter(
          (shift: Shift) => shift.startDateTime.toISOString().split('T')[0] == day
        )
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
          (assignment: Assignment) => assignment.idShift == shiftId
        )
      }
    }
  },
  actions: {
    async fetchData() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''
      this.volunteers = [
        { id: 'ba', firstname: 'Mohamed', lastname: 'Benali' } as Volunteer,
        { id: 'bc', firstname: 'Claire', lastname: 'Dubois' } as Volunteer,
        { id: 'bc', firstname: 'Claire', lastname: 'Dubois' } as Volunteer,
        { id: 'bd', firstname: 'Nathan', lastname: 'Cohen' } as Volunteer,
        { id: 'be', firstname: 'Fatoumata', lastname: 'Diara' } as Volunteer,
        { id: 'bf', firstname: 'Jean-Pierre', lastname: 'Leclerc' } as Volunteer,
        { id: 'bg', firstname: 'Lina', lastname: 'Ferreira' } as Volunteer,
        { id: 'bh', firstname: 'Yasmine', lastname: 'Haddad' } as Volunteer,
        { id: 'bi', firstname: 'Noé', lastname: 'Nguyen' } as Volunteer,
        { id: 'bj', firstname: 'Adèle', lastname: 'Kone' } as Volunteer,
        { id: 'bk', firstname: 'Victorien', lastname: 'Dupuis' } as Volunteer
      ]
      this.shifts = [
        {
          id: 'aa',
          idStation: 'aa',
          startDateTime: new Date(2025, 5, 30, 12),
          endDateTime: new Date(2025, 5, 30, 18)
        } as Shift,
        {
          id: 'ab',
          idStation: 'ab',
          startDateTime: new Date(2025, 5, 30, 11),
          endDateTime: new Date(2025, 5, 30, 15)
        } as Shift,
        {
          id: 'ac',
          idStation: 'aa',
          startDateTime: new Date(2025, 5, 31, 12),
          endDateTime: new Date(2025, 5, 31, 18)
        } as Shift,
        {
          id: 'ad',
          idStation: 'ab',
          startDateTime: new Date(2025, 5, 31, 10),
          endDateTime: new Date(2025, 5, 31, 16)
        } as Shift,
        {
          id: 'ae',
          idStation: 'ae',
          startDateTime: new Date(2025, 5, 30, 12),
          endDateTime: new Date(2025, 5, 30, 18)
        } as Shift,
        {
          id: 'af',
          idStation: 'af',
          startDateTime: new Date(2025, 5, 30, 11),
          endDateTime: new Date(2025, 5, 30, 15)
        } as Shift,
        {
          id: 'ag',
          idStation: 'ae',
          startDateTime: new Date(2025, 5, 31, 12),
          endDateTime: new Date(2025, 5, 31, 18)
        } as Shift,
        {
          id: 'ah',
          idStation: 'af',
          startDateTime: new Date(2025, 5, 31, 10),
          endDateTime: new Date(2025, 5, 31, 16)
        } as Shift
      ]
      this.stations = [
        {
          id: 'aa',
          label: 'Poste 1',
        } as Station,
        {
          id: 'ab',
          label: 'Poste 2',
        } as Station,
        {
          id: 'ae',
          label: 'Poste 3',
        } as Station,
        {
          id: 'af',
          label: 'Poste 4',
        } as Station,
      ]
      this.assignments = [
        { idShift: 'aa', idVolunteer: 'bd', role: 'CI' } as Assignment,
        { idShift: 'aa', idVolunteer: 'bg', role: 'PSE2' } as Assignment,
        { idShift: 'aa', idVolunteer: 'ba', role: 'PSE2' } as Assignment,
        { idShift: 'aa', idVolunteer: 'be', role: 'PSE1' } as Assignment,
        { idShift: 'ab', idVolunteer: 'bk', role: 'CI' } as Assignment,
        { idShift: 'ab', idVolunteer: 'bc', role: 'PSE2' } as Assignment,
        { idShift: 'ab', idVolunteer: 'bf', role: 'PSE2' } as Assignment,
        { idShift: 'ab', idVolunteer: 'bj', role: 'LOG' } as Assignment,
        { idShift: 'ac', idVolunteer: 'bd', role: 'CI' } as Assignment,
        { idShift: 'ac', idVolunteer: 'bj', role: 'LOG' } as Assignment,
        { idShift: 'ac', idVolunteer: 'bg', role: 'PSE2' } as Assignment,
        { idShift: 'ac', idVolunteer: 'ba', role: 'PSE2' } as Assignment,
        { idShift: 'ac', idVolunteer: 'bi', role: 'STAG' } as Assignment,
        { idShift: 'ad', idVolunteer: 'bk', role: 'CI' } as Assignment,
        { idShift: 'ad', idVolunteer: 'bf', role: 'PSE2' } as Assignment,
        { idShift: 'ad', idVolunteer: 'be', role: 'PSE1' } as Assignment,
        { idShift: 'ae', idVolunteer: 'bd', role: 'CI' } as Assignment,
        { idShift: 'ae', idVolunteer: 'bg', role: 'PSE2' } as Assignment,
        { idShift: 'ae', idVolunteer: 'ba', role: 'PSE2' } as Assignment,
        { idShift: 'ae', idVolunteer: 'be', role: 'PSE1' } as Assignment,
        { idShift: 'af', idVolunteer: 'bk', role: 'CI' } as Assignment,
        { idShift: 'af', idVolunteer: 'bc', role: 'PSE2' } as Assignment,
        { idShift: 'af', idVolunteer: 'bf', role: 'PSE2' } as Assignment,
        { idShift: 'af', idVolunteer: 'bj', role: 'LOG' } as Assignment,
        { idShift: 'ag', idVolunteer: 'bd', role: 'CI' } as Assignment,
        { idShift: 'ag', idVolunteer: 'bj', role: 'LOG' } as Assignment,
        { idShift: 'ag', idVolunteer: 'bg', role: 'PSE2' } as Assignment,
        { idShift: 'ag', idVolunteer: 'ba', role: 'PSE2' } as Assignment,
        { idShift: 'ag', idVolunteer: 'bi', role: 'STAG' } as Assignment,
        { idShift: 'ah', idVolunteer: 'bk', role: 'CI' } as Assignment,
        { idShift: 'ah', idVolunteer: 'bf', role: 'PSE2' } as Assignment,
        { idShift: 'ah', idVolunteer: 'be', role: 'PSE1' } as Assignment
      ]
      return
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
