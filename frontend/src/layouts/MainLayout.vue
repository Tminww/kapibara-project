<template>
  <t-header-widget :color="t('layouts.dashboard.header.color')">
    <template #title>
      <div @click="goToHome()">
        {{ t('layouts.dashboard.header.title') }}
      </div>
    </template>
    <template #auth>
      <v-btn v-if="!stateStorage.username" @click="goToLogin()" :disabled="route.name === 'login'">
        Войти
      </v-btn>
      <v-btn v-else @click="goToLogout()"> Выйти ({{ stateStorage.username }}) </v-btn>
    </template>
    <!-- <template #logout>
            Выйти
            <v-btn
                class="ml-2"
                color="primary"
                @click="goToLogout()"
                :disabled="route.name === 'home'"
            >
            </v-btn>
        </template> -->
  </t-header-widget>

  <v-main color="grey-lighten-4">
    <v-row v-if="route.meta.breadCrumb" no-gutters class="justify-start" color="grey-lighten-4">
      <v-col color="grey-lighten-4">
        <v-container fluid> <t-breadcrumbs divider="/"></t-breadcrumbs></v-container>
      </v-col>
    </v-row>
    <slot> </slot>
  </v-main>

  <Toaster richColors :expand="true" position="bottom-right" />
</template>

<script setup>
import { THeaderWidget, TBreadcrumbs } from '@/components/widgets'
import { Toaster } from 'vue-sonner'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import stateStorage from '@/utils/auth'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()

const goToLogin = async () => {
  await router.push({
    name: 'login'
  })
}

const goToLogout = async () => {
  localStorage.clear()

  await router.replace({
    name: 'home'
  })
  // Вызывается для того, чтобы очистить хранилище vuex,
  // считать данные из localStorage и заново отрендерить layout
  window.location.reload()
}

const goToHome = async () => {
  await router.push({
    name: 'home'
  })
}
</script>

<style scoped></style>
