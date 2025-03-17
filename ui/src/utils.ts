import { parseISO } from 'date-fns'

export function getRouteParam(param: string | string[]): string {
  if (Array.isArray(param)) {
    return param[0]
  } else {
    return param
  }
}

const ISODateFormat = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d*)?(?:[-+]\d{2}:?\d{2}|Z)?$/

const isIsoDateString = (value: unknown): value is string => {
  return typeof value === 'string' && ISODateFormat.test(value)
}

export function handleDates(data: unknown) {
  if (isIsoDateString(data)) return parseISO(data)
  if (data === null || data === undefined || typeof data !== 'object') return data

  for (const [key, val] of Object.entries(data)) {
    // @ts-expect-error this is a hack to make the type checker happy
    if (isIsoDateString(val)) data[key] = parseISO(val)
    else if (typeof val === 'object') handleDates(val)
  }

  return data
}
