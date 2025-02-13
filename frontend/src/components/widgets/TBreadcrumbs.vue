<template>
	<v-breadcrumbs :items="breadCrumbs">
		<template v-slot:item="{ item }">
			<v-breadcrumbs-item :to="item.to" :disabled="item.disabled">
				<div v-if="!item.to" class="font-weight-bold">
					{{ item.text }}
				</div>
				<div v-else>
					{{ item.text }}
				</div>
			</v-breadcrumbs-item>
		</template>
	</v-breadcrumbs>
</template>

<script setup>
	import { computed } from 'vue'
	import { useRoute } from 'vue-router'

	const route = useRoute()

	const breadCrumbs = computed(() => {
		if (typeof route.meta.breadCrumb === 'function') {
			return route.meta.breadCrumb.call(this, route)
		}
		return route.meta.breadCrumb
	})
</script>
