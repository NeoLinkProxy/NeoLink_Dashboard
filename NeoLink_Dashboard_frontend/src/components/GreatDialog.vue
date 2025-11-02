<template>
  <dialog id="greatDialog" ref="dialog">
    <!-- 使用默认插槽让用户自定义内容 -->
    <!-- <slot id="greatDialogSlot"></slot> -->
    <div id="greatDialogContent"></div>
    <div id="greatDialogCloseButton" class="button" @click="closeDialog()">关闭</div>
  </dialog>
</template>

<script setup lang='ts'>
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'close'): void
}>()

const dialog = ref<HTMLDialogElement | null>(null)

// 修改 showAlert 方法，不再设置 info_dag，而是直接显示对话框
const showAlert = () => {
  if (dialog.value) {
    dialog.value.getAnimations().forEach((animation) => {
      animation.cancel()
    })
    dialog.value.showModal()
    if (Math.random() > 0.5) {
      dialog.value.animate({
        transform: ['rotate(-15deg)', 'rotate(15deg)', 'rotate(0deg)']
      }, {
        duration: 150,
        fill: 'forwards',
        easing: 'ease-in-out',
      })
    } else {
      dialog.value.style.transformOrigin = 'left bottom'
      dialog.value.animate({
        transform: ['rotate(15deg)', 'rotate(-15deg)', 'rotate(0deg)']
      }, {
        duration: 150,
        fill: 'forwards',
        easing: 'ease-in-out',
      })
      setTimeout(() => {
        if (dialog.value) {
          dialog.value.style.transformOrigin = ''
        }
      }, 145)
    }
  }
};

const closeDialog = () => {
  if (dialog.value) {
    dialog.value.getAnimations().forEach((animation) => {
      animation.cancel()
    })
    if (Math.random() > 0.5) {
      dialog.value.animate({
        transform: ['rotate(-15deg)', 'rotate(0deg)', 'rotate(15deg)']
      }, {
        duration: 150,
        fill: 'forwards',
        easing: 'ease-in-out',
      })
    } else {
      dialog.value.style.transformOrigin = 'left bottom'
      dialog.value.animate({
        transform: ['rotate(-15deg)', 'rotate(0deg)', 'rotate(15deg)']
      }, {
        duration: 150,
        fill: 'forwards',
        easing: 'ease-in-out',
      })
      setTimeout(() => {
        if (dialog.value) {
          dialog.value.style.transformOrigin = ''
        }
      }, 145)
    }
    setTimeout(() => {
      if (dialog.value) {
        dialog.value.close()
      }
      emit('close')

    }, 145)
  }
}

defineExpose({
  showAlert,
  closeDialog,
})
</script>

<style>
dialog {
  margin: auto;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 1px solid #444;
}

.button {
  padding: 8px 16px;
  background-color: #002850;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 10px;
}

.button:hover {
  background-color: #003d7a;
}
</style>
