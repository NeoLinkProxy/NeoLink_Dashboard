<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
// import hljs from 'highlight.js'
// import 'highlight.js/styles/github-dark.css'

const title = ref('')

async function renderMarkdown() {
  try {
    const response = await fetch(`/UserAgreementAndDisclaimer.md`)
    if (!response.ok) throw new Error('用户协议与免责声明加载失败')
    const markdownText = await response.text()
    title.value = `用户协议与免责声明`
    document.title = `用户协议与免责声明`
    const html = await marked(markdownText) // 转换为 HTML
    document.getElementById('content')!.innerHTML = html
    // hljs.highlightAll()

    fixAdjacentPreTags()
  } catch (error: unknown) {
    if (error instanceof Error) {
      fail(error)
    } else {
      fail(new Error('发生未知错误'))
    }
  }
}

function fail(error: Error) {
  document.getElementById('content')!.innerHTML = `！失败 -  ${error.message} ！`;
  document.title = `！失败 -  ${error.message} ！`
}

onMounted(() => {
  renderMarkdown()
})

function fixAdjacentPreTags() {
  const content = document.getElementById('content')
  if (!content) return
  
  const preElements = content.querySelectorAll('pre')
  
  for (let i = 0; i < preElements.length - 1; i++) {
    const current = preElements[i]
    const next = preElements[i + 1]
    
    if (current.nextSibling?.nextSibling === next) {
      const p = document.createElement('p')
      p.innerHTML = '&nbsp;'
      
      current.parentNode?.insertBefore(p, next)
    }
  }
}

onMounted(async () => {
  window.appState?.GetIsChinaUser()
})

</script>

<template>
  <div class="container">
    <div class="header">
      <h1 class="title">{{ title }}</h1>
    </div>
    <div class="content-wrapper">
      <pre id="content" class="content"></pre>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 960px;
  margin: 20px auto;
  padding: 0 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px 0;
  border-bottom: 2px solid #3a3a3a;
}

.title {
  color: #e0e0e0;
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.3;
}

.content-wrapper {
  background: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.content {
  padding: 40px;
  line-height: 1.8;
  color: #cccccc;
  font-size: 17px;
}

/* 文本元素样式 */
.content h1,
.content h2,
.content h3,
.content h4,
.content h5,
.content h6 {
  color: #e0e0e0;
  margin-top: 1.5em;
  margin-bottom: 1em;
  font-weight: 600;
}

.content h1 {
  font-size: 2em;
  border-bottom: 1px solid #3a3a3a;
  padding-bottom: 0.5em;
}

.content h2 {
  font-size: 1.7em;
  border-bottom: 1px solid #3a3a3a;
  padding-bottom: 0.4em;
}

.content p {
  margin-bottom: 1.2em;
}

.content a {
  color: #64b5f6;
  text-decoration: none;
  border-bottom: 1px dashed #64b5f6;
}

.content a:hover {
  color: #90caf9;
  border-bottom-style: solid;
}

.content strong {
  font-weight: 700;
  color: #e0e0e0;
}

.content em {
  font-style: italic;
}

/* 列表样式 */
.content ul,
.content ol {
  margin: 1.2em 0;
  padding-left: 2em;
}

.content li {
  margin-bottom: 0.5em;
}

.content ul li {
  list-style-type: disc;
}

.content ol li {
  list-style-type: decimal;
}

/* 引用块样式 */
.content blockquote {
  margin: 1.5em 0;
  padding: 1.2em 1.5em;
  background-color: #2d2d2d;
  border-left: 4px solid #64b5f6;
  color: #cccccc;
  font-style: italic;
}

/* 代码块样式 */
.content pre {
  background-color: #2d3748;
  border-radius: 8px;
  padding: 20px;
  overflow: auto;
  margin: 1.5em 0;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
}

.content code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 0.9em;
}

.content pre code {
  background-color: transparent;
  padding: 0;
}

.content :not(pre) > code {
  background-color: #2d2d2d;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  color: #ff6b6b;
  font-weight: 500;
}

/* 表格样式 */
.content table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5em 0;
  background-color: #1e1e1e;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  overflow: hidden;
}

.content table th,
.content table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #3a3a3a;
}

.content table th {
  background-color: #2d2d2d;
  font-weight: 600;
  color: #e0e0e0;
}

.content table tr:last-child td {
  border-bottom: none;
}

.content table tr:nth-child(even) {
  background-color: #252525;
}

/* 分割线 */
.content hr {
  border: none;
  height: 1px;
  background-color: #3a3a3a;
  margin: 2em 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 0 15px;
  }
  
  .title {
    font-size: 1.8rem;
  }
  
  .content {
    padding: 25px 20px;
    font-size: 16px;
  }
  
  .content h1 {
    font-size: 1.7em;
  }
  
  .content h2 {
    font-size: 1.5em;
  }
  
  .content pre {
    padding: 15px;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 1.5rem;
  }
  
  .content {
    padding: 20px 15px;
  }
  
  .content h1,
  .content h2,
  .content h3 {
    margin-top: 1.2em;
    margin-bottom: 0.8em;
  }
}
</style>