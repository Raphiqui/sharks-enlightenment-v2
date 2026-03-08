import { createApp } from "vue";
import "./tailwind.css";
import "./style.scss";
import Quiz from "./components/Quiz.vue";
import ScrollIndicator from "./components/ScrollIndicator.vue";

const quizEl = document.querySelector("#quiz");
if (quizEl) {
  createApp(Quiz).mount(quizEl);
}

const scrollIndicatorEl = document.querySelector("#scroll-indicator");
if (scrollIndicatorEl) {
  createApp(ScrollIndicator).mount(scrollIndicatorEl);
}
