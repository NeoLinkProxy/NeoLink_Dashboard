import GreatDialog from '@/components/GreatDialog.vue';

export {}

declare global {
  interface Window {
    appState?: {
      info: string,
      errorinfo: string,
      updateInfo: (newInfo: string) => void,
      updateErrorInfo: (newErrorInfo: string) => void,
      appendErrorInfo: (newErrorInfo: string) => void,
      updateIsChinaUser: (newIsChinaUser: boolean) => void,
      GetIsChinaUser: () => void,
      greatDialog: Ref<InstanceType<typeof GreatDialog>>
    }
  }
}
