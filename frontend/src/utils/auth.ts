import { useStorage } from '@vueuse/core'

const stateStorage = useStorage('user', {
    username: '',
    role: '',
    token: ''
})

export default stateStorage
