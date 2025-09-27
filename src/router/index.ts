import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/home.vue'
import SignUp from '@/views/signup.vue'
import SignIn from '@/views/signin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: HomeView,
    },
		{
			path: "/signup",
			name: "SignUp",
			component: SignUp,
		},
		{
			path: "/signin",
			name: "SignIn",
			component: SignIn,
		},
    {
      path: "/recommendations",
      name: "Recommendations",
      component: () => import("@/views/recommendations.vue"),
    },
    {
      path: "/form",
      name: "Form",
      component: () => import("@/views/form.vue"),
    }
  ],
})

export default router
