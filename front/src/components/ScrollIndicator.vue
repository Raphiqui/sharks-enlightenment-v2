<template>
  <div
    class="absolute bottom-10 left-1/2"
    style="animation: bounce 1s infinite; cursor: pointer;"
    @click="scrollDown"
  >
    <svg
      class="w-8 h-8 text-ocean-glow/60"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      stroke-width="2"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M19 14l-7 7m0 0l-7-7m7 7V3"
      />
    </svg>
  </div>
</template>

<script setup>
  function scrollDown() {
    const root = document.documentElement;
    const vh = root.clientHeight;
    const currentScroll = root.scrollTop;
    const nextSnap = Math.ceil((currentScroll + 1) / vh) * vh;

    root.scrollTo({ top: nextSnap, behavior: 'smooth' });
  }
</script>
