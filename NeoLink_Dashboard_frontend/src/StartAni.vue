<script setup lang="ts">
import { ref, onMounted } from 'vue'

const Img = ref<HTMLImageElement | null>(null)
const Text = ref<HTMLParagraphElement | null>(null)

onMounted(() => {
    if (!Img.value || !Text.value) return
    // 图片慢慢变大，图片和文字透明度慢慢变小，用 Web Anim API
    Img.value.animate([
        { transform: 'scale(1)' , opacity: '1' },
        { transform: 'scale(1.2)' , opacity: '0' },
    ], {
        duration: 1000,
        fill: 'forwards'
    })
    setTimeout(
        () => {
            if (!Text.value) return
            Text.value.animate([
                { opacity: '1' },
                { opacity: '0' }
            ], {
                duration: 1000,
                fill: 'forwards'
            })
        },
        1000
    )
})

</script>

<template>
    <h1 style="height: 100px;"></h1>
    <h1></h1>
    <div class="stan">
        <img ref="Img" src="/Images/NeoLink_仪表盘_NeoLink_Dashboard.png" alt="NeoLink_仪表盘_NeoLink_Dashboard.png">
        <br>
        <p ref="Text">NeoLink 仪表盘<br>NeoLink Dashboard</p>
    </div>
</template>

<style scoped>
body {
    background-color: #181818;
    margin: 0;
    min-height: 100vh;
    font-family: 'SmileySans-Oblique';
}
 
.stan {
    display: flex;
    justify-content: center;
    align-items: center;
}

img {
    width: calc(128px * 2);
    height: calc(128px * 2);
}
p {
    font-size: 23px;
    /* color: #fff; */
}
</style>
