import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/home.vue";
import SignUp from "@/views/signup.vue";
import SignIn from "@/views/signin.vue";
import Profile from "@/views/profile.vue";
// import Schedule from "@/views/schedule.vue";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "Home",
			component: HomeView,
		},
		// {
		// 	path: "/schedule",
		// 	name: "Schedule",
		// 	component: Schedule,
		// },
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
			path: "/profile",
			name: "Profile",
			component: Profile,
		},
	],
});

export default router;
