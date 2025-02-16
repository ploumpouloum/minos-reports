import { createRouter, createWebHashHistory } from 'vue-router'
import Report1View from '../views/Report1View.vue'
import Manques1View from '@/views/Manques1View.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Manques1View
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
    }
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

export default router
