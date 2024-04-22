function dateFormat(date) {
	const year = date.getFullYear()
	const month =
		date.getMonth() >= 9 ? date.getMonth() + 1 : '0' + (date.getMonth() + 1)
	const day = date.getDate() >= 9 ? date.getDate() : '0' + date.getDate()
	console.log(`${year}-${month}-${day}`)
	return `${year}-${month}-${day}`
}

export function getLastQuarter() {
	const currentDate = new Date()
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

export function getLastMonth() {
	const currentDate = new Date()
	const currentMonth = currentDate.getMonth()
	const currentYear = currentDate.getFullYear()
	let startDate = new Date(currentYear, currentMonth - 1, 1)
	let endDate = new Date(currentYear, currentMonth, 0)

	startDate = dateFormat(startDate)
	endDate = dateFormat(endDate)
	return { startDate, endDate }
}

export function getLastYear() {
	const currentDate = new Date()
	const currentYear = currentDate.getFullYear()
	let startDate = new Date(currentYear - 1, 0, 1)
	let endDate = new Date(currentYear, 0, 0)

	startDate = dateFormat(startDate)
	endDate = dateFormat(endDate)
	return { startDate, endDate }
}
