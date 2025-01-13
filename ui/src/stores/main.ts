import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'
import type { Assignment, Station, Volunteer } from '@/types/main'

export type RootState = {
  assignments: Assignment[]
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
      stations: [],
      volunteers: [],
      isLoading: false,
      errorMessage: '',
      errorDetails: ''
    }) as RootState,
  getters: {
    startDays(state) {
      return new Set(state.stations.map((station: Station) => station.startDateTime.toISOString().split('T')[0]))
    },
    getStations(state) {
      return (day: String): Station[] => {
        return state.stations.filter((station: Station) => station.startDateTime.toISOString().split('T')[0] == day)
      }
    },
    getStation(state) {
      return (stationId: String): Station => {
        return state.stations.filter((station: Station) => station.id == stationId)[0]
      }
    },
    getVolunteer(state) {
      return (volunteerId: String): Volunteer => {
        return state.volunteers.filter((volunteer: Volunteer) => volunteer.id == volunteerId)[0]
      }
    },
    getStationAssignments(state) {
      return (stationId: String): Assignment[] => {
        return state.assignments.filter((assignment: Assignment) => assignment.idStation == stationId)
      }
    }
  },
  actions: {
    async fetchData() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''
      this.volunteers = [
        { id: "ba", firstname: "Mohamed", lastname: "Benali" } as Volunteer, 
        { id: "bc", firstname: "Claire", lastname: "Dubois" } as Volunteer,
        { id: "bc", firstname: "Claire", lastname: "Dubois" } as Volunteer,
        { id: "bd", firstname: "Nathan", lastname: "Cohen" } as Volunteer,
        { id: "be", firstname: "Fatoumata", lastname: "Diara" } as Volunteer,
        { id: "bf", firstname: "Jean-Pierre", lastname: "Leclerc" } as Volunteer,
        { id: "bg", firstname: "Lina", lastname: "Ferreira" } as Volunteer,
        { id: "bh", firstname: "Yasmine", lastname: "Haddad" } as Volunteer,
        { id: "bi", firstname: "Noé", lastname: "Nguyen" } as Volunteer,
        { id: "bj", firstname: "Adèle", lastname: "Kone" } as Volunteer,
        { id: "bk", firstname: "Victorien", lastname: "Dupuis" } as Volunteer,
      ]
      this.stations = [
        { id: "aa", label: "Poste 1", startDateTime: new Date(2025, 5, 30, 12), endDateTime: new Date(2025, 5, 30, 18)} as Station, 
        { id: "ab", label: "Poste 2", startDateTime: new Date(2025, 5, 30, 11), endDateTime: new Date(2025, 5, 30, 15)} as Station, 
        { id: "ac", label: "Poste 1", startDateTime: new Date(2025, 5, 31, 12), endDateTime: new Date(2025, 5, 31, 18)} as Station, 
        { id: "ad", label: "Poste 2", startDateTime: new Date(2025, 5, 31, 10), endDateTime: new Date(2025, 5, 31, 16)} as Station, 
        { id: "ae", label: "Poste 3", startDateTime: new Date(2025, 5, 30, 12), endDateTime: new Date(2025, 5, 30, 18)} as Station, 
        { id: "af", label: "Poste 4", startDateTime: new Date(2025, 5, 30, 11), endDateTime: new Date(2025, 5, 30, 15)} as Station, 
        { id: "ag", label: "Poste 3", startDateTime: new Date(2025, 5, 31, 12), endDateTime: new Date(2025, 5, 31, 18)} as Station, 
        { id: "ah", label: "Poste 4", startDateTime: new Date(2025, 5, 31, 10), endDateTime: new Date(2025, 5, 31, 16)} as Station, 
      ]
      this.assignments = [
        { idStation: "aa", idVolunteer: 'bd', role: 'CI' } as Assignment,
        { idStation: "aa", idVolunteer: 'bg', role: 'PSE2' } as Assignment,
        { idStation: "aa", idVolunteer: 'ba', role: 'PSE2' } as Assignment,
        { idStation: "aa", idVolunteer: 'be', role: 'PSE1' } as Assignment,
        { idStation: "ab", idVolunteer: 'bk', role: 'CI' } as Assignment,
        { idStation: "ab", idVolunteer: 'bc', role: 'PSE2' } as Assignment,
        { idStation: "ab", idVolunteer: 'bf', role: 'PSE2' } as Assignment,
        { idStation: "ab", idVolunteer: 'bj', role: 'LOG' } as Assignment,
        { idStation: "ac", idVolunteer: 'bd', role: 'CI' } as Assignment,
        { idStation: "ac", idVolunteer: 'bj', role: 'LOG' } as Assignment,
        { idStation: "ac", idVolunteer: 'bg', role: 'PSE2' } as Assignment,
        { idStation: "ac", idVolunteer: 'ba', role: 'PSE2' } as Assignment,
        { idStation: "ac", idVolunteer: 'bi', role: 'STAG' } as Assignment,
        { idStation: "ad", idVolunteer: 'bk', role: 'CI' } as Assignment,
        { idStation: "ad", idVolunteer: 'bf', role: 'PSE2' } as Assignment,
        { idStation: "ad", idVolunteer: 'be', role: 'PSE1' } as Assignment,
        { idStation: "ae", idVolunteer: 'bd', role: 'CI' } as Assignment,
        { idStation: "ae", idVolunteer: 'bg', role: 'PSE2' } as Assignment,
        { idStation: "ae", idVolunteer: 'ba', role: 'PSE2' } as Assignment,
        { idStation: "ae", idVolunteer: 'be', role: 'PSE1' } as Assignment,
        { idStation: "af", idVolunteer: 'bk', role: 'CI' } as Assignment,
        { idStation: "af", idVolunteer: 'bc', role: 'PSE2' } as Assignment,
        { idStation: "af", idVolunteer: 'bf', role: 'PSE2' } as Assignment,
        { idStation: "af", idVolunteer: 'bj', role: 'LOG' } as Assignment,
        { idStation: "ag", idVolunteer: 'bd', role: 'CI' } as Assignment,
        { idStation: "ag", idVolunteer: 'bj', role: 'LOG' } as Assignment,
        { idStation: "ag", idVolunteer: 'bg', role: 'PSE2' } as Assignment,
        { idStation: "ag", idVolunteer: 'ba', role: 'PSE2' } as Assignment,
        { idStation: "ag", idVolunteer: 'bi', role: 'STAG' } as Assignment,
        { idStation: "ah", idVolunteer: 'bk', role: 'CI' } as Assignment,
        { idStation: "ah", idVolunteer: 'bf', role: 'PSE2' } as Assignment,
        { idStation: "ah", idVolunteer: 'be', role: 'PSE1' } as Assignment,
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
