<template>
  <div>
    <div v-if="error">Oops! Error encountered: {{ error.message }}</div>
    <div v-else-if="data">
      Data loaded:
      <pre>{{ data }}</pre>
    </div>
    <div v-else>Loading...</div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'

  const data = ref(null)
  const error = ref(null)

  fetch("/api/quiz")
    .then((res) => res.json())
    .then((json) => (data.value = json))
    .catch((err) => (error.value = err))

  const questions = ref([]);
  const userResponseSkeleton = ref(null);
  const userResponses = ref(null);
  const questionIndex = ref(0);
  const show = ref(true);
  const showQuestion = ref(true);
  const showCorrectAnswer = ref(false);
  const score = ref(0);
  const isCorrect = ref(false);
</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>
