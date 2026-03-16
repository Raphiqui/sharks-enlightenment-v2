<template>
  <section ref="QuizContainer">
    <Suspense>
      <Quiz />
      <template #fallback>
        Loading...
      </template>
    </Suspense>
  </section>
</template>

<script setup>
  import Quiz from "./Quiz.vue"
</script>
