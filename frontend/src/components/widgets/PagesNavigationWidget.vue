<template>
	<v-slide-group>
		<v-slide-group-item
			v-for="page in pages"
			:key="page.name"
			v-slot="{ isSelected, toggle }"
		>
			<v-btn
				v-if="page.role == userRole"
				:color="isSelected ? color : 'dark'"
				class="ma-1"
				:ripple="false"
				variant="flat"
				@click="
					() => {
						toggle()
						switchPage(page.name)
					}
				"
			>
				{{ page.title }}
			</v-btn>
		</v-slide-group-item>
	</v-slide-group>
</template>

<script setup>
	import { getAuthDataFromLocalStorage } from '@/utils/auth'
	import { computed, defineProps } from 'vue'
	import { useI18n } from 'vue-i18n'
	import { useRouter } from 'vue-router'

	const router = useRouter()
	const { t } = useI18n()

	const props = defineProps({
		color: {
			type: String,
			default: 'light',
		},
	})

	const authData = computed(() => {
		console.log(getAuthDataFromLocalStorage())
		return getAuthDataFromLocalStorage()
	})
	const userRole = computed(() => {
		const currentRole =
			authData.value.role === 'администратор' ? 'admin' : 'operator'
		console.log(currentRole)
		return currentRole
	})

	const switchPage = routeName => {
		router.push({
			name: routeName,
		})
	}

	const pages = [
		{
			name: 'naprs',
			title: t('layouts.naprs'),
			role: 'operator',
		},
		{
			name: 'obrs',
			title: t('layouts.obrs'),
			role: 'operator',
		},
		{
			name: 'results',
			title: t('layouts.results'),
			role: 'operator',
		},
		{
			name: 'resobjects',
			title: t('layouts.resobjects'),
			role: 'operator',
		},
		{
			name: 'sandoctors',
			title: t('layouts.sandoctors'),
			role: 'operator',
		},
		{
			name: 'podrs',
			title: t('layouts.podrs'),
			role: 'operator',
		},
		{
			name: 'targets',
			title: t('layouts.targets'),
			role: 'operator',
		},
		{
			name: 'obr-types',
			title: t('layouts.obr-types'),
			role: 'operator',
		},
		{
			name: 'poks',
			title: t('layouts.poks'),
			role: 'operator',
		},
		{
			name: 'protocol-types',
			title: t('layouts.protocol-types'),
			role: 'operator',
		},
		{
			name: 'zakls',
			title: t('layouts.zakls'),
			role: 'operator',
		},
		{
			name: 'protocols',
			title: t('layouts.protocols'),
			role: 'operator',
		},
		{
			name: 'users',
			title: t('layouts.users'),
			role: 'admin',
		},
	]
</script>

<style scoped></style>
