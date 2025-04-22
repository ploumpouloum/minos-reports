import { createRouter, createWebHashHistory } from 'vue-router'
import Report1View from '../views/Report1View.vue'
import ManquesView from '@/views/ManquesView.vue'
import DataView from '@/views/DataView.vue'
import HomeView from '@/views/HomeView.vue'
import RestrictionsView from '@/views/RestrictionsView.vue'
import VolunteerView from '@/views/VolunteerView.vue'
import VolunteersDlusView from '@/views/VolunteersDlusView.vue'
import VolunteersView from '@/views/VolunteersView.vue'
import ShiftView from '@/views/ShiftView.vue'
import FreeBuzyView from '@/views/FreeBuzyView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/report1',
      name: 'report1',
      component: Report1View
    },
    {
      path: '/manques',
      name: 'manques',
      component: ManquesView
    },
    {
      path: '/data',
      name: 'data',
      component: DataView
    },
    {
      path: '/freebuzy',
      name: 'freebuzy',
      component: FreeBuzyView
    },
    {
      path: '/restrictions',
      name: 'restrictions',
      component: RestrictionsView
    },
    {
      path: '/volunteers',
      name: 'volunteers',
      component: VolunteersView
    },
    {
      path: '/volunteers-dlus',
      name: 'volunteers-dlus',
      component: VolunteersDlusView
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
    },
    {
      path: '/:catchAll(.*)',
      name: 'catchAll',
      redirect: { name: 'home' }
    }
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

export default router
