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
  nivol: string | undefined
  minor: boolean | undefined
  mission_restrictions: string[] | undefined
  food_restrictions: string[] | undefined
}

export interface Assignment {
  shiftId: string
  volunteerId: string | undefined
  role: string
}
