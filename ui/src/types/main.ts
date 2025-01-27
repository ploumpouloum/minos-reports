export interface Shift {
  id: string
  stationId: string
  startDateTime: string
  endDateTime: string
}

export interface Station {
  id: string
  label: string
}

export interface Volunteer {
  id: string
  firstname: string
  lastname: string
}

export interface Assignment {
  shiftId: string
  volunteerId: string
  role: string
}
