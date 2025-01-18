export interface Station {
  id: string
  label: string
  startDateTime: Date
  endDateTime: Date
}

export interface Volunteer {
  id: string
  firstname: string
  lastname: string
}

export interface Assignment {
  idStation: string
  idVolunteer: string
  role: string
}
