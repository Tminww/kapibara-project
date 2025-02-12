<template></template>

<script setup>
	import { useI18n } from 'vue-i18n'

	const { t } = useI18n()
	defineProps({
		color: {
			type: String,
			default: 'primary',
		},
	})
</script>
