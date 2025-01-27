export interface Shift {
  id: string
  idStation: string
  startDateTime: Date
  endDateTime: Date
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
  idShift: string
  idVolunteer: string
  role: string
}
