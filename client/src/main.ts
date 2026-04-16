import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import 'primeicons/primeicons.css';
import Aura from '@primeuix/themes/aura';
import StyleClass from 'primevue/styleclass';
import './style.css';
import App from './App.vue';
import router from './router';
import { ToastService } from 'primevue';
import ConfirmationService from 'primevue/confirmationservice';

const app = createApp(App);

app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.p-dark', 
        }
    }
});
app.use(ToastService);
app.use(ConfirmationService);
app.directive('styleclass', StyleClass);
app.mount('#app');