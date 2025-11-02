<template>
  <div style="background-color: #181818;">
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'

onMounted(async () => {
  window.appState?.GetIsChinaUser()
})
</script>