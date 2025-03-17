export interface Shift {
  id: string
  stationId: string
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
  nivol: string | undefined
  minor: boolean | undefined
  mission_restrictions: string[] | undefined
  food_restrictions: string[] | undefined
  incoming_date_time: Date
  outgoing_date_time: Date
}

export interface Assignment {
  shiftId: string
  volunteerId: string | undefined
  role: string
}

export enum FreeBusyStatus {
  Busy,
  NotAvailable,
  Free
}
