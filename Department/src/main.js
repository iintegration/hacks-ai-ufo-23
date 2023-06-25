import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import store from './stores'
import tooltip from "./directives/tooltip.js";
import "@/assets/tooltip.css";

const app = createApp(App)

app.directive("tooltip", tooltip)
app.use(createPinia())
app.use(router)
app.mount('#app')
app.use(store)
