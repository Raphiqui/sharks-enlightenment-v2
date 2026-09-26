import { createApp } from "vue";
import "./tailwind.css";
import "./style.scss";
import QuizContainer from "./components/QuizContainer.vue";
import ScrollIndicator from "./components/ScrollIndicator.vue";
import { initHeader } from "./header.js";

initHeader();

const quizContainerEl = document.querySelector("#quiz");
if (quizContainerEl) {
  createApp(QuizContainer).mount(quizContainerEl);
}

const scrollIndicatorEl = document.querySelector("#scroll-indicator");
if (scrollIndicatorEl) {
  createApp(ScrollIndicator).mount(scrollIndicatorEl);
}
