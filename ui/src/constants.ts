import type { InjectionKey } from 'vue'
import type { Config } from './config'

export const stationsRolesMaps: { [role: string]: string } = {
  'Conducteur VL': 'CH VL',
  Logisticien: 'LOG',
  'PSE 2 Conducteur VPSP': 'CH VPSP',
  'Opérateur PC': 'OP PC',
  Participant: 'PART',
  'Logisticien administratif et technique (sur DPS)': 'LAT',
  'PSE 1': 'PSE1',
  'PSE 2': 'PSE2',
  CI: 'CI',
  CDMGE: 'CDMGE',
  CS: 'CS',
  CDPE: 'CDPE'
}

export const stationsRolesOrder = [
  'CDMGE',
  'CS',
  'CDPE',
  'CI',
  'OP PC',
  'CI',
  'CH VPSP',
  'PSE2',
  'PSE1',
  'LOG',
  'LAT',
  'PART',
  'CH VL'
]

export default {
  config: Symbol() as InjectionKey<Config>
}
