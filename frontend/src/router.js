import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/Home.vue';
import UserRegister from './views/Register.vue';
import UserLogin from './views/Login.vue';
import AdminLogin from './views/AdminLogin.vue';
import UserProfile from './views/Profile.vue';
import AddAlbum from './album/AddAlbum.vue';
import ShowAlbums from './album/ShowAlbums.vue';
import AllAlbums from './album/AllAlbums.vue';
import EditAlbum from './album/EditAlbum.vue';
import AddSong from './song/AddSong.vue'
import ShowSong from './song/ShowSong'


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
  {
    path: '/add-album',
    name: 'AddAlbum',
    component: AddAlbum
  },
  {
    path: '/albums',
    name: 'ShowAlbums',
    component: ShowAlbums
  },
  {
    path: '/albums/all',
    name: 'AllAlbums',
    component: AllAlbums
  },
  {
    path: '/albums/:id/edit',
    name: 'EditAlbum',
    component: EditAlbum
  },
  {
    path: '/albums/:id/add-song',
    name: 'AddSong',
    component: AddSong
  },
  {
    path: '/albums/:id/songs',
    name: 'ShowSong',
    component: ShowSong
  },
  
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;