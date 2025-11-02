export {}

declare global {
  interface Window {
    pywebview?: {
      api: {
        open_url: (url: string) => void
      }
    }
  }
}