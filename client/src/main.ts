import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import StyleClass from 'primevue/styleclass';
import './style.css';
import App from './App.vue';
import router from './router';

const app = createApp(App);

app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.directive('styleclass', StyleClass);
app.mount('#app');