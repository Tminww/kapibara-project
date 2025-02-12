function dateFormat(date) {
	const year = date.getFullYear()
	const month =
		date.getMonth() >= 9 ? date.getMonth() + 1 : '0' + (date.getMonth() + 1)
	const day = date.getDate() >= 9 ? date.getDate() : '0' + date.getDate()
	console.log(`${year}-${month}-${day}`)
	return `${year}-${month}-${day}`
}

export function getLastQuarter(currentDate = new Date()) {
	const currentMonth = currentDate.getMonth()
	const currentYear = currentDate.getFullYear()
	const currentQuarter = Math.floor(currentMonth / 3) + 1
	const previousQuarter = currentQuarter - 1

	const startOfPreviousQuarter = new Date(
		currentYear,
		(previousQuarter - 1) * 3,
		1,
	)
	const endOfPreviousQuarter = new Date(currentYear, previousQuarter * 3, 0)

	const startDate = dateFormat(startOfPreviousQuarter)
	const endDate = dateFormat(endOfPreviousQuarter)
	return { startDate, endDate }
}

export function getLastMonth(currentDate = new Date()) {
	const currentMonth = currentDate.getMonth()
	const currentYear = currentDate.getFullYear()
	let startDate = new Date(currentYear, currentMonth - 1, 1)
	let endDate = new Date(currentYear, currentMonth, 0)

	startDate = dateFormat(startDate)
	endDate = dateFormat(endDate)
	return { startDate, endDate }
}

export function getLastYear(currentDate = new Date()) {
	const currentYear = currentDate.getFullYear()
	let startDate = new Date(currentYear - 1, 0, 1)
	let endDate = new Date(currentYear, 0, 0)

	startDate = dateFormat(startDate)
	endDate = dateFormat(endDate)
	return { startDate, endDate }
}

export const mapDistrictNameToShortName = name => {
	const map = {
		'Центральный Федеральный округ': 'ЦФО',
		'Северо-Западный Федеральный округ': 'СЗФО',
		'Северо-Кавказский Федеральный округ': 'СКФО',
		'Южный Федеральный округ': 'ЮФО',
		'Приволжский Федеральный округ': 'ПФО',
		'Уральский Федеральный округ': 'УФО',
		'Сибирский Федеральный округ': 'СФО',
		'Дальневосточный Федеральный округ': 'ДФО',
	}
	return map[name]
}

export const mapDistrictShortNameToName = name => {
	const map = {
		ЦФО: 'Центральный Федеральный округ',
		СЗФО: 'Северо-Западный Федеральный округ',
		СКФО: 'Северо-Кавказский Федеральный округ',
		ЮФО: 'Южный Федеральный округ',
		ПФО: 'Приволжский Федеральный округ',
		УФО: 'Уральский Федеральный округ',
		СФО: 'Сибирский Федеральный округ',
		ДФО: 'Дальневосточный Федеральный округ',
	}
	return map[name]
}
