import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginForm from '../views/LoginForm.vue'
import WidgetsView from '../views/WidgetsView.vue'
import WidgetInfo from '../views/WidgetInfo.vue'
import store from '../stores'



const router = createRouter({
  
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: '/login',
      name: 'Login',
      component: LoginForm,
    }, 
    {
      path: '/',
      name: 'widgets',
      component: WidgetsView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/Widget/:obj_id',
      name: 'Widget',
      component: WidgetInfo,
      meta: {
        requiresAuth: true
      }
    },
  ]
})
router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
      
    }
    next('/login') 
  } else {
    next()
  }
})


export default router
