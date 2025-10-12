<!-- src/components/Edition_logs.vue -->
<template>
  <div ref="btn" class="btn">
    <svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 48 48">
      <g fill="none" stroke-linejoin="round" stroke-width="4" data-swindex="0">
        <rect width="28" height="34" x="13" y="10" fill="#2F88FF" stroke="#000"></rect>
        <path stroke="#000" stroke-linecap="round" d="M35 10V4H8C7.44772 4 7 4.44772 7 5V38H13"></path>
        <path stroke="#fff" stroke-linecap="round" d="M21 22H33"></path>
        <path stroke="#fff" stroke-linecap="round" d="M21 30H33"></path>
      </g>
    </svg>
    <p>版本日志</p>
  </div>

  <dialog ref="ELD" id="ELD" class="ELD">
    <div class="ELDC">
      <h1>ESC键退出</h1>
      <hr>
      <h1>版本日志：</h1>
      <div class="content-container">
        <pre>{{ EL }}</pre>
      </div>
    </div>
  </dialog>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps<{
  EL: string
}>()

const btn = ref<HTMLButtonElement | null>(null)
const ELD = ref<HTMLDialogElement | null>(null)

onMounted(() => {
  // if (ELD.value) {ELD.value.style.display='none'}
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})



const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (target.closest('.btn')) {
    if (ELD.value) {
      ELD.value.showModal()
      // ELD.value.style.display = 'flex'
    }
  }
}
</script>

<style scoped>
.ELD {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  height: 80%;
  padding: 20px;
}

.ELDC {
  position: fixed;
  width: 100%;
  height: 100%;
  background-color: #181818;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  flex-direction: column;
}

.ELD::backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

.content-container {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #fff;
  padding: 10px;
  margin: 10px 0;
}

.content-container pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #fff;
  font-family: 'SarasaMonoSC', monospace;
}

.btn {
  cursor: pointer;
  padding: 20px;
  height: 135px;
  width: 135px;
  border-radius: 50%;
  background-color: rgba(54, 0, 126, 0.7);
  border: 1px solid #fff;
  position: absolute;
  right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn:hover {
  background-color: rgba(67, 67, 67, 0.7);
}
</style>