import { createApp } from 'vue'
import './tailwind.css'
import './style.scss'
import Quiz from './components/Quiz.vue'
@source "../back/templates/**/*.html";

createApp(Quiz).mount('#quiz')
