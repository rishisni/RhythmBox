import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/Home.vue';
import UserRegister from '@/views/Register.vue';
import UserLogin from '@/views/Login.vue';
import AdminLogin from '@/views/AdminLogin.vue';
import UserProfile from '@/views/Profile.vue';
import AddAlbum from '@/album/AddAlbum.vue';
import ShowAlbums from '@/album/ShowAlbums.vue';
import AllAlbums from '@/album/AllAlbums.vue';
import EditAlbum from '@/album/EditAlbum.vue';
import AddSong from '@/song/AddSong.vue'
import ShowSong from '@/song/ShowSong.vue'
import LyricsPage from '@/song/LyricsPage.vue'
import EditSong from '@/song/EditSong.vue'
import AllSongs from '@/song/AllSongs.vue';
import AlbumSong from '@/song/AlbumSong.vue';


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
    path: '/albums/:albumId/add-song',
    name: 'AddSong',
    component: AddSong
  },
  {
    path: '/albums/:albumId/songs',
    name: 'ShowSong',
    component: ShowSong
  },
  {
    path: '/albums/:albumId/album-songs',
    name: 'AlbumSong',
    component: AlbumSong
  },
  {
    path: '/albums/:albumId/songs/:lyrics',
    name: 'LyricsPage',
    component: LyricsPage
  },
  {
    path: '/albums/:albumId/songs/:songId/edit',
    name: 'EditSong',
    component: EditSong,
  },
  {
    path: '/all-songs',
    name: 'AllSongs',
    component: AllSongs,
  },
  
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;