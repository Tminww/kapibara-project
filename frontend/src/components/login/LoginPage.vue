<template>
    <v-container class="d-flex align-center justify-center h-100">
        <v-card class="pa-8" elevation="3" min-width="450" max-width="500">
            <h3 class="">Логин</h3>

            <v-text-field
                v-model="username"
                density="compact"
                placeholder="Имя пользователя"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                color="primary"
                :error="usernameError"
                :error-messages="usernameError ? 'Введите имя пользователя' : ''"
            ></v-text-field>

            <h3 class="">Пароль</h3>

            <v-text-field
                v-model="password"
                :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                :type="visible ? 'text' : 'password'"
                density="compact"
                placeholder="Введите пароль"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                color="primary"
                :error="passwordError"
                :error-messages="passwordError ? 'Введите пароль' : ''"
                @click:append-inner="visible = !visible"
            ></v-text-field>

            <v-btn
                class="my-4"
                color="primary"
                size="large"
                variant="tonal"
                block
                :loading="isLoading"
                :disabled="isLoading"
                @click="submit"
            >
                <template v-slot:loader>
                    <v-progress-circular
                        indeterminate
                        color="white"
                        size="20"
                    ></v-progress-circular>
                </template>
                Войти
            </v-btn>
        </v-card>
    </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import stateStorage from '@/utils/auth'

import api from '@/api'

const router = useRouter()
const route = useRoute()

const visible = ref(false)
const username = ref('')
const password = ref('')
const usernameError = ref(false)
const passwordError = ref(false)
const isLoading = ref(false)

const submit = async () => {
    usernameError.value = !username.value
    passwordError.value = !password.value

    if (!usernameError.value && !passwordError.value) {
        isLoading.value = true
        try {
            const response = await api.auth.login({
                username: username.value,
                password: password.value
            })

            if (!response.error) {
                stateStorage.value = {
                    username: response.username,
                    role: response.role,
                    token: response.token
                }
                // Redirect to the dashboard or home page
                router.push({ name: (route.query.redirect as string) || 'home' })
            } else {
                console.error('Login error:', response.error)
            }
        } catch (error) {
            console.error('Login failed:', error)
        } finally {
            isLoading.value = false
        }
    }
}
</script>

<style scoped>
.vh-100 {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
