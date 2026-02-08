import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import StyleClass from 'primevue/styleclass';
import './style.css';
import App from './App.vue';
import router from './router';
import { ToastService } from 'primevue';

const app = createApp(App);

app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(ToastService);
app.directive('styleclass', StyleClass);
app.mount('#app');