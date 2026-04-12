import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import router from './router'

import * as bootstrap from 'bootstrap'

createApp(App).use(router).mount('#app')
