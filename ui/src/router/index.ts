import { createRouter, createWebHashHistory } from 'vue-router'
import Report1View from '../views/Report1View.vue'
import Manques1View from '@/views/Manques1View.vue'
import DataView from '@/views/DataView.vue'
import RestrictionsView from '@/views/RestrictionsView.vue'
import VolunteerView from '@/views/VolunteerView.vue'
import ShiftView from '@/views/ShiftView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: { name: 'restrictions' }
    },
    {
      path: '/report1',
      name: 'report1',
      component: Report1View
    },
    {
      path: '/manques1',
      name: 'manques1',
      component: Manques1View
    },
    {
      path: '/data',
      name: 'data',
      component: DataView
    },
    {
      path: '/restrictions',
      name: 'restrictions',
      component: RestrictionsView
    },
    {
      path: '/volunteer/:nivol',
      name: 'volunteer',
      component: VolunteerView
    },
    {
      path: '/shift/:shiftId',
      name: 'shift',
      component: ShiftView
    }
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

export default router
