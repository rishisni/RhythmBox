createApp(App).mount('#app')
import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
import '@/assets/css/styles.css';


import router from './router';




createApp(App)
  .use(router) 
  .mount('#app');

