<template>
	<v-container>
		<v-row no-gutters>
			<v-col :cols="auto" v-for="block in blocks" :key="block.link">
				<v-container>
					<t-organ-card
						:title="block.title"
						:description="block.description"
						:icon="block.icon"
						:linkName="block.linkName"
						:max-width="400"
						:min-width="350"
					>
						<template #chart>
							<!-- <div v-for="i in block.count" :key="i">
								{{ testLabels[i - 1] }}: {{ testSeries[i - 1] }}
							</div> -->
							<!-- <t-donut-chart
								legend-position="bottom"
								:labels="
									testLabels.sort().slice(0, block.count)
								"
								:series="testSeries.slice(0, block.count)"
							></t-donut-chart> -->
							<!-- <apexchart
								:options="chartOptions"
								:series="testSeries"
							></apexchart> -->
						</template>
					</t-organ-card>
				</v-container>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup>
	import { TOrganCard } from '@/components/widgets'
	import { TDonutChart } from '@/components/widgets'

	const blocks = [
		// {
		// 	linkName: 'president',
		// 	icon: 'president',
		// 	description: `Законы РФ о поправке к Конституции РФ,
		//    федеральные конституционные законы, федеральные законы, указы Президента РФ,
		//    распоряжения Президента РФ`,
		// 	title: 'Президент РФ',
		// 	count: 8,
		// },
		// {
		// 	linkName: 'council_1',
		// 	icon: 'council_1',
		// 	description: `Постановления Совета Федерации, принятые по вопросам,
		//    отнесенным к ведению палаты частью 1 статьи 102 Конституции РФ`,
		// 	title: 'Совет Федерации Федерального Собрания РФ',
		// 	count: 1,
		// },
		// {
		// 	linkName: 'council_2',
		// 	icon: 'council_2',
		// 	description: `Постановления Государственной Думы, принятые по вопросам,
		//    отнесенным к ведению палаты частью 1 статьи 103 Конституции РФ`,
		// 	title: 'Государственная Дума Федерального Собрания РФ',
		// 	count: 1,
		// },
		// {
		// 	linkName: 'government',
		// 	icon: 'government',
		// 	description: 'Правовые акты Правительства РФ',
		// 	title: 'Правительство РФ',
		// 	count: 2,
		// },
		// {
		// 	linkName: 'federal_authorities',
		// 	icon: 'federal_authorities',
		// 	description:
		// 		'Правовые акты федеральных органов исполнительной власти и федеральных государственных органов РФ',
		// 	title: 'ФОИВ и ФГО РФ',
		// 	count: 5,
		// },
		// {
		// 	linkName: 'court',
		// 	icon: 'court',
		// 	description:
		// 		'Постановления Конституционного Суда РФ, определения Конституционного Суда РФ и иные решения Конституционного Суда РФ',
		// 	title: 'Конституционный Суд РФ',
		// 	count: 5,
		// },
		// {
		// 	linkName: 'subjects',
		// 	icon: 'subjects',
		// 	description: 'Законы и иные правовые акты субъектов РФ',
		// 	title: 'Органы государственной власти субъектов РФ',
		// 	count: 9, //29
		// },
		// {
		// 	linkName: 'international',
		// 	icon: 'international',
		// 	description:
		// 		'Международные договоры, вступившие в силу для РФ, временно применяемые международные договоры РФ',
		// 	title: 'Международные договоры РФ',
		// 	count: 9, //13
		// },
		// {
		// 	linkName: 'un_securitycouncil',
		// 	icon: 'un_securitycouncil',
		// 	description:
		// 		'Резолюции Совета Безопасности Организации Объединённых Наций',
		// 	title: 'Совет Безопасности ООН',
		// 	count: 1,
		// },
		{
			linkName: 'dashboard',
			icon: 'dashboard',
			description:
				'Информационная панель, обощающая информацию по количеству опубликованных нормативных правовых актатов РФ',
			title: 'Информационная панель',
			count: 1,
		},
	]

	const testSeries = [
		100, 99, 98, 97, 96, 95, 95, 94, 93, 93, 92, 91, 91, 90, 90, 89, 88, 88,
		87, 87, 85, 80, 78, 78, 75, 70, 69, 68, 67, 66, 64, 62, 60, 58, 58, 56,
		54, 52, 51, 50, 49, 49, 48, 45, 44,
	]

	const testLabels = [
		'Конституция',
		'Закон Российской Федерации о поправке к Конституции Российской Федерации',
		'Федеральный конституционный закон',
		'Федеральный закон',
		'Указ',
		'Постановление',
		'Постановление Правления',
		'Распоряжение',
		'Резолюция',
		'Соглашение',
		'Конвенция',
		'Международный договор',
		'Договор',
		'Апелляционное определение',
		'Определение',
		'Протокол',
		'Поправки',
		'Дополнение',
		'Дополнительный протокол',
		'Меморандум',
		'Исполнительный протокол',
		'Сообщение Президента Российской Федерации',
		'Сообщение о принятии Решения',
		'Сообщение о судебном Решении',
		'Официальное сообщение Министерства иностранных дел',
		'Приказ',
		'Положение',
		'Конституционный закон',
		'Регламент',
		'Устав',
		'Устав (Основной Закон)',
		'Закон о поправках к Уставу',
		'Поправки к Уставу',
		'Закон о внесении поправок в Устав Красноярского края',
		'Закон Республики Бурятия о внесении поправок в Конституцию Республики Бурятия',
		'Закон',
		'Областной закон',
		'Уставный закон',
		'Решение правления',
		'Решение',
		'Заключение',
		'Извещение',
		'Указание',
		'Сообщение о принятии апелляционного решения',
		'Сообщение о принятии апелляционного определения',
	]
	const chartOptions = {
		chart: {
			type: 'bar',
			height: 350,
			group: 'someId',
		},
		plotOptions: {
			bar: {
				borderRadius: 4,
				borderRadiusApplication: 'end',
				horizontal: true,
			},
		},
		dataLabels: {
			enabled: true,
		},
		xaxis: {
			show: false,
			categories: testLabels,
		},
	}
</script>
