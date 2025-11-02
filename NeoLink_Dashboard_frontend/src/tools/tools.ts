const openInBrowser = (url: string) => {
  // 使用 pywebview 的 API 在外部浏览器中打开链接
  if (window.pywebview) {
    window.pywebview.api.open_url(url)
  } else {
    // 开发环境下使用 window.open 作为备选方案
    window.open(url, '_blank')
  }
}

const ReportError = async (error_: any) => {
  try {
    // alert(`发生错误，上报错误中：${error_}`)
    const response = await fetch('http://localhost:23104/error', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: error_.message,
        stack: error_.stack,
        name: error_.name,
        timestamp: new Date().toISOString()
      }),
    });
  } catch (error: unknown) {
    // 类型检查
    if (error instanceof Error) {
      window.appState?.appendErrorInfo(`上报错误失败: ${error.message}。请复制内容并联系管理员\n`)
      window.appState?.appendErrorInfo(`详细错误: ${error_.message} ${error_.stack} ${error_.name} ${error_.message} ${error_.stack} ${error_.name}\n`)
    } else {
      window.appState?.appendErrorInfo(`上报错误失败: 未知错误。请复制内容并联系管理员\n`)
      window.appState?.appendErrorInfo(`详细错误: 未知错误 ${error_.message} ${error_.stack} ${error_.name} ${error_.message} ${error_.stack} ${error_.name}\n`)
    }
    // console.error('详细错误:', error, error_);
  }
}

const showSponsorDialog = () => {
  window.appState?.greatDialog.showAlert()
}

export {
  openInBrowser,
  ReportError,
  showSponsorDialog
}
