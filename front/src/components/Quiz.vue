<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// ── Inline SVG icon components (no external dependency) ────────────────────
const SVG_ATTRS = 'xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'

const CheckCircle2 = {
  template: `<svg ${SVG_ATTRS}><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>`
}
const XCircle = {
  template: `<svg ${SVG_ATTRS}><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>`
}
const ChevronRight = {
  template: `<svg ${SVG_ATTRS}><path d="m9 18 6-6-6-6"/></svg>`
}
const RotateCcw = {
  template: `<svg ${SVG_ATTRS}><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>`
}
const Trophy = {
  template: `<svg ${SVG_ATTRS}><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>`
}
const Sparkles = {
  template: `<svg ${SVG_ATTRS}><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>`
}
// ───────────────────────────────────────────────────────────────────────────

let observer = null
const error = ref(null)

const res = await fetch("/api/quiz")

let questions = await res.json()

questions = questions.questions

onMounted( async () => {
  // Intersection observer
  observer = new IntersectionObserver(
    ([entry]) => { if (entry.isIntersecting) isVisible.value = true },
    { threshold: 0.2 }
  )
  if (sectionRef.value) observer.observe(sectionRef.value)
})

const currentQuestion = ref(0)
const selectedAnswer = ref(null)
const hasAnswered = ref(false)
const score = ref(0)
const isComplete = ref(false)
const isVisible = ref(false)
const sectionRef = ref(null)

onUnmounted(() => { observer?.disconnect() })

const percentage = computed(() => Math.round((score.value / questions.length) * 100))

const progressWidth = computed(() => `${((currentQuestion.value + 1) / questions.length) * 100}%`)

const strokeDashoffset = computed(() => 553 - (553 * percentage.value) / 100)

const resultMessage = computed(() => {
  if (percentage.value >= 80) return "Amazing! You're a true shark expert!"
  if (percentage.value >= 60) return "Great job! You know your sharks well!"
  if (percentage.value >= 40) return "Not bad! Keep learning about these fascinating creatures."
  return "Time to look around and learn more!"
})

const trophyGradient = computed(() => {
  if (percentage.value >= 80) return { '--g-from': '#10b981', '--g-to': '#06b6d4' }
  if (percentage.value >= 60) return { '--g-from': '#06b6d4', '--g-to': '#3b82f6' }
  if (percentage.value >= 40) return { '--g-from': '#f59e0b', '--g-to': '#f97316' }
  return { '--g-from': '#f43f5e', '--g-to': '#ec4899' }
})

function selectAnswer(index) {
  if (hasAnswered.value) return
  selectedAnswer.value = index
  hasAnswered.value = true
  if (questions[currentQuestion.value].options[selectedAnswer.value].is_correct) score.value++
}

function next() {
  if (currentQuestion.value < questions.length - 1) {
    currentQuestion.value++
    selectedAnswer.value = null
    hasAnswered.value = false
  } else {
    isComplete.value = true
  }
}

function restart() {
  currentQuestion.value = 0
  selectedAnswer.value = null
  hasAnswered.value = false
  score.value = 0
  isComplete.value = false
}

function optionClass(index, isCorrect) {
  const isSelected = selectedAnswer.value === index
  if (!hasAnswered.value) return isSelected ? 'option--selected' : ''
  if (isCorrect) return 'option--correct'
  if (isSelected) return 'option--wrong'
  return 'option--dimmed'
}

function letterClass(index, isCorrect) {
  const isSelected = selectedAnswer.value === index
  if (!hasAnswered.value) return ''
  if (isCorrect) return 'letter--correct'
  if (isSelected) return 'letter--wrong'
  return 'letter--dimmed'
}

const bubbles = Array.from({ length: 15 }, (_, i) => ({
  id: i,
  left: `${Math.floor(Math.random() * 100)}%`,
  duration: `${8 + Math.random() * 4}s`,
  delay: `${Math.random() * 5}s`,
  size: `${6 + Math.floor(Math.random() * 10)}px`
}))
</script>

<template>
<section ref="sectionRef">
    <div class="sq-container">
      <!-- Card wrapper -->
      <div class="sq-card-wrap" :class="{ 'sq-card-wrap--visible': isVisible }">
        <!-- Bubbles -->
        <div class="sq-bubbles">
          <div
              v-for="b in bubbles"
              :key="b.id"
              class="sq-bubble"
              :style="{ left: b.left, animationDuration: b.duration, animationDelay: b.delay, width: b.size, height: b.size }"
              />
          </div>

        <div class="sq-card">
          <div class="sq-card-glow" />

          <!-- Quiz panel -->
          <Transition name="slide" mode="out-in">
            <div v-if="!isComplete" :key="currentQuestion" class="sq-panel">

              <!-- Progress -->
              <div class="sq-progress">
                <div class="sq-progress-labels">
                  <span>Question {{ currentQuestion + 1 }} of {{ questions.length }}</span>
                  <span>{{ score }} correct</span>
                </div>
                <div class="sq-progress-track">
                  <div class="sq-progress-fill" :style="{ width: progressWidth }" />
                </div>
              </div>

              <!-- Question -->
              <h3 class="sq-question">{{ questions[currentQuestion].question }}</h3>

              <!-- Options -->
              <div class="sq-options">
                <button
                  v-for="(optionObj, index) in questions[currentQuestion].options"
                  :key="index"
                  class="sq-option"
                  :class="optionClass(index, optionObj.is_correct)"
                  :disabled="hasAnswered"
                  @click="selectAnswer(index)"
                >
                  <div class="sq-option-inner">
                    <div class="sq-option-left">
                      <span class="sq-letter" :class="letterClass(index, optionObj.is_correct)">
                        {{ String.fromCharCode(65 + index) }}
                      </span>
                      <span class="sq-option-text" :class="letterClass(index, optionObj.is_correct)">{{ optionObj.option }}</span>
                    </div>
                    <Transition name="pop">
                      <div v-if="hasAnswered" class="sq-icon-wrap">
                        <CheckCircle2
                          v-if="optionObj.is_correct"
                          class="sq-icon sq-icon--correct"
                        />
                        <XCircle
                          v-else-if="selectedAnswer === index"
                          class="sq-icon sq-icon--wrong"
                        />
                      </div>
                    </Transition>
                  </div>
                </button>
              </div>

              <!-- Explanation -->
              <Transition name="expand">
                <div v-if="hasAnswered" class="sq-explanation-wrap">
                  <div
                    class="sq-explanation"
                    :class="questions[currentQuestion].options[selectedAnswer].is_correct ? 'sq-explanation--correct' : 'sq-explanation--wrong'"
                  >
                    <Sparkles class="sq-sparkle" :class="questions[currentQuestion].options[selectedAnswer].is_correct ? 'sq-sparkle--correct' : 'sq-sparkle--wrong'" />
                    <p class="sq-explanation-text">{{ questions[currentQuestion].explanation }}</p>
                  </div>
                </div>
              </Transition>

              <!-- Next button -->
              <Transition name="fade-up">
                <div v-if="hasAnswered" class="sq-next-row">
                  <button class="sq-btn sq-btn--next" @click="next">
                    <template v-if="currentQuestion < questions.length - 1">
                      Next Question <ChevronRight class="sq-btn-icon" />
                    </template>
                    <template v-else>
                      See Results <Trophy class="sq-btn-icon" />
                    </template>
                  </button>
                </div>
              </Transition>
            </div>

            <!-- Results panel -->
            <div v-else key="results" class="sq-results">
              <div class="sq-trophy-wrap" :style="trophyGradient">
                <Trophy class="sq-trophy" />
              </div>

              <h3 class="sq-result-title">Quiz Complete!</h3>

              <div class="sq-score-circle">
                <svg class="sq-score-svg" viewBox="0 0 192 192">
                  <circle cx="96" cy="96" r="88" fill="none" stroke="currentColor" stroke-width="8" class="sq-score-track" />
                  <circle
                    cx="96" cy="96" r="88"
                    fill="none"
                    stroke="url(#scoreGrad)"
                    stroke-width="8"
                    stroke-linecap="round"
                    :stroke-dasharray="553"
                    :stroke-dashoffset="strokeDashoffset"
                    class="sq-score-arc"
                  />
                  <defs>
                    <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stop-color="#06b6d4" />
                      <stop offset="100%" stop-color="#3b82f6" />
                    </linearGradient>
                  </defs>
                </svg>
                <div class="sq-score-content">
                  <span class="sq-score-pct">{{ percentage }}%</span>
                  <span class="sq-score-sub">{{ score }} of {{ questions.length }} correct</span>
                </div>
              </div>

              <p class="sq-result-msg">{{ resultMessage }}</p>

              <button class="sq-btn sq-btn--restart" @click="restart">
                <RotateCcw class="sq-btn-icon sq-btn-icon--left" /> Try Again
              </button>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>

/* ── Bubbles ── */
.sq-bubbles { position: absolute; inset: 0; z-index: 1; pointer-events: none; }
.sq-bubble {
  position: absolute;
  bottom: -20px;
  border-radius: 50%;
  background: rgba(99, 202, 235, 0.35);
  border: 1px solid rgba(99, 202, 235, 0.5);
  animation: rise linear infinite;
}

@keyframes rise {
  0%   { transform: translateY(0)   scale(1);   opacity: 0.6; }
  100% { transform: translateY(-110vh) scale(0.4); opacity: 0; }
}

/* ── Container ── */
.sq-container {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 42rem;
  margin: 0 auto;
}

/* ── Card ── */
.sq-card-wrap {
  overflow: hidden;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease 0.2s, transform 0.6s ease 0.2s;
}
.sq-card-wrap--visible { opacity: 1; transform: translateY(0); }

.sq-card {
  position: relative;
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1.5rem;
  padding: 2rem;
  overflow: hidden;
}

.sq-card-glow {
  position: absolute;
  inset: -2px;
  border-radius: 1.5rem;
  background: linear-gradient(135deg, rgba(6,182,212,0.3), rgba(59,130,246,0.3), transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.sq-panel, .sq-results { position: relative; z-index: 1; }

/* ── Progress ── */
.sq-progress { margin-bottom: 1.5rem; }
.sq-progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #93c5fd;
  margin-bottom: 0.5rem;
}
.sq-progress-track {
  height: 6px;
  background: rgba(255,255,255,0.1);
  border-radius: 9999px;
  overflow: hidden;
}
.sq-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #06b6d4, #3b82f6);
  border-radius: 9999px;
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Question ── */
.sq-question {
  font-size: clamp(1rem, 3vw, 1.25rem);
  font-weight: 700;
  color: #fff;
  margin: 0 0 1.5rem;
  line-height: 1.4;
}

/* ── Options ── */
.sq-options { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1rem; }

.sq-option {
  width: 100%;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 0.75rem;
  padding: 0.875rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #e2e8f0;
  text-align: left;
}
.sq-option:not(:disabled):hover {
  background: rgba(6,182,212,0.1);
  border-color: rgba(6,182,212,0.4);
  transform: translateY(-1px);
}

.sq-option--correct  { background: rgba(16,185,129,0.15); border-color: #10b981 !important; }
.sq-option--wrong    { background: rgba(239,68,68,0.15);  border-color: #ef4444 !important; }
.sq-option--selected { background: rgba(6,182,212,0.15);  border-color: #06b6d4 !important; }
.sq-option--dimmed   { opacity: 0.45; }

.sq-option-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sq-option-left { display: flex; align-items: center; gap: 0.75rem; }

.sq-letter {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  font-size: 0.75rem;
  font-weight: 700;
  color: #cbd5e1;
  flex-shrink: 0;
  transition: background 0.2s;
}
.letter--correct { background: rgba(16,185,129,0.3); color: #6ee7b7; }
.letter--wrong   { background: rgba(239,68,68,0.3);  color: #fca5a5; }
.letter--dimmed  { opacity: 0.5; }

.sq-option-text { font-size: 0.9rem; font-weight: 500; transition: color 0.2s; }
.letter--correct.sq-option-text { color: #6ee7b7; }
.letter--wrong.sq-option-text   { color: #fca5a5; }

.sq-icon-wrap { flex-shrink: 0; }
.sq-icon { width: 1.25rem; height: 1.25rem; }
.sq-icon--correct { color: #10b981; }
.sq-icon--wrong   { color: #ef4444; }

/* ── Explanation ── */
.sq-explanation-wrap { overflow: hidden; }
.sq-explanation {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.75rem;
  margin-bottom: 1rem;
}
.sq-explanation--correct { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); }
.sq-explanation--wrong   { background: rgba(239,68,68,0.1);  border: 1px solid rgba(239,68,68,0.3); }

.sq-sparkle { width: 1.1rem; height: 1.1rem; flex-shrink: 0; margin-top: 2px; }
.sq-sparkle--correct { color: #10b981; }
.sq-sparkle--wrong   { color: #ef4444; }

.sq-explanation-text { font-size: 0.875rem; color: #cbd5e1; line-height: 1.6; margin: 0; }

/* ── Buttons ── */
.sq-next-row { display: flex; justify-content: flex-end; }

.sq-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.7rem 1.6rem;
  border-radius: 0.75rem;
  border: none;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.sq-btn--next {
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
  color: #fff;
  box-shadow: 0 4px 16px rgba(6,182,212,0.35);
}
.sq-btn--next:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(6,182,212,0.5); }

.sq-btn-icon      { width: 1.1rem; height: 1.1rem; }
.sq-btn-icon--left { margin-right: 0.2rem; }

/* ── Results ── */
.sq-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem 0;
}

.sq-trophy-wrap {
  width: 5rem;
  height: 5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--g-from), var(--g-to));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
  box-shadow: 0 8px 30px rgba(6,182,212,0.4);
  animation: trophy-pop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes trophy-pop {
  from { transform: scale(0) rotate(-180deg); opacity: 0; }
  to   { transform: scale(1) rotate(0deg);   opacity: 1; }
}

.sq-trophy { width: 2.25rem; height: 2.25rem; color: #fff; }

.sq-result-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #fff;
  margin: 0 0 1.5rem;
}

/* Score circle */
.sq-score-circle {
  position: relative;
  width: 192px;
  height: 192px;
  margin-bottom: 1.5rem;
}
.sq-score-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}
.sq-score-track { color: rgba(255,255,255,0.08); }
.sq-score-arc {
  transition: stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1) 0.3s;
}
.sq-score-content {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.sq-score-pct {
  font-size: 2.5rem;
  font-weight: 800;
  color: #fff;
  line-height: 1;
}
.sq-score-sub { font-size: 0.8rem; color: #93c5fd; margin-top: 0.25rem; }

.sq-result-msg {
  font-size: 1rem;
  color: #93c5fd;
  margin: 0 0 1.5rem;
  max-width: 24rem;
}

.sq-btn--restart {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.2);
  color: #fff;
}
.sq-btn--restart:hover {
  background: rgba(255,255,255,0.14);
  transform: translateY(-2px);
}

/* ── Vue Transitions ── */
.slide-enter-active, .slide-leave-active { transition: all 0.3s ease; }
.slide-enter-from  { opacity: 0; transform: translateX(20px); }
.slide-leave-to    { opacity: 0; transform: translateX(-20px); }

.pop-enter-active  { transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop-enter-from    { opacity: 0; transform: scale(0); }

.expand-enter-active, .expand-leave-active { transition: all 0.3s ease; overflow: hidden; }
.expand-enter-from, .expand-leave-to       { opacity: 0; max-height: 0; }
.expand-enter-to, .expand-leave-from       { opacity: 1; max-height: 200px; }

.fade-up-enter-active { transition: all 0.3s ease 0.2s; }
.fade-up-enter-from   { opacity: 0; transform: translateY(10px); }
</style>
