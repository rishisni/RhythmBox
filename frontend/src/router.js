import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/Home.vue';
import UserRegister from './views/Register.vue';
import UserLogin from './views/Login.vue';
import AdminLogin from './views/AdminLogin.vue';
import UserProfile from './views/Profile.vue';


const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/register',
    name: 'Register',
    component: UserRegister
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin
  },
  {
    path: '/admin-login',
    name: 'AdminLogin',
    component: AdminLogin
  },
  {
    path: '/profile',
    name: 'Profile',
    component: UserProfile
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
