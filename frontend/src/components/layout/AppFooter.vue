<script setup>
import { ref, onMounted } from 'vue'

const currentYear = ref(new Date().getFullYear())
</script>

<template>
  <footer class="bg-light text-dark text-center py-4 mt-5">
    <p>Copyright, {{ currentYear }} HMS. All rights reserved.</p>
  </footer>
</template>

<style scoped>

</style>
