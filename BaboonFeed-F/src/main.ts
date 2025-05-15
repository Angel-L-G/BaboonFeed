import './assets/styles/custom.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import FontAwesomeIcon from './plugins/fontawesome/fontawesome.ts'

import App from './App.vue'
import router from './router'

import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
