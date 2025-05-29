export interface Shift {
  id: string
  stationId: string
  startDateTime: Date
  endDateTime: Date
  meetDateTime: Date
}

export interface Station {
  id: string
  label: string
  kind?: string
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
  roles: string[] | undefined
  department: string
  dlus_email: string
  arrived: boolean
}

export interface Assignment {
  id: string
  shiftId: string
  volunteerId: string | undefined
  role: string
  comments: string | undefined
}

export enum FreeBusyStatus {
  Busy,
  NotAvailable,
  Free
}
