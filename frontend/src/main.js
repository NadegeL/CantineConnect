import { createApp } from 'vue';

import { createPinia } from 'pinia';

import 'uno.css';

import 'virtual:uno.css';

import VueTelInput from 'vue-tel-input';
import 'vue-tel-input/vue-tel-input.css';

import App from './App.vue';
import router from './router';
import './style.css';

const app = createApp(App);
const pinia = createPinia();
app.use(VueTelInput);
app.use(pinia);
app.use(router);

app.mount('#app');
