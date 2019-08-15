import Vue from 'vue';
import Router from 'vue-router';
import Asgs from './components/Asgs.vue';
import Ping from './components/Ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Asgs',
      component: Asgs,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
