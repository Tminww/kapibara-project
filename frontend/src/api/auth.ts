import client from './client'

class Auth {
    endpoint: string
    constructor(endpoint = '/api/login') {
        this.endpoint = endpoint
    }

    login = async (params: Record<string, string>) => {
        // return (await client.post(`${this.endpoint}/start`)).data
        const response = new Promise<Record<string, string>>((resolve) => {
            setTimeout(() => {
                params.username === 'admin' && params.password === 'admin'
                    ? resolve({
                          username: params.username,
                          role: params.username === 'admin' ? 'администратор' : 'пользователь',
                          token: '1234567890abcdef'
                      })
                    : resolve({
                          error: 'Неверный логин или пароль'
                      })
            }, 2000)
        })
        return response
    }
    logout = async () => {
        const response = new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    message: 'Вы вышли из системы'
                })
            }, 2000)
        })
        return response
    }
}

export default Auth
