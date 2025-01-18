import { createRouter, createWebHashHistory } from 'vue-router'
import Report1View from '../views/Report1View.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'report1',
      component: Report1View
    }
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

export default router
