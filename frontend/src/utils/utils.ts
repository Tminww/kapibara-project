export function dateFormat(date: string | Date, format = 'YYYY-MM-DD') {
    const newDate: Date = new Date(date)
    const year = newDate.getFullYear()
    const month = newDate.getMonth() >= 9 ? newDate.getMonth() + 1 : '0' + (newDate.getMonth() + 1)
    const day = newDate.getDate() > 9 ? newDate.getDate() : '0' + newDate.getDate()

    format = format.replace('YYYY', String(year))
    format = format.replace('MM', String(month))
    format = format.replace('DD', String(day))

    return format
}

export function getLastWeek(currentDate = new Date()) {
    let currentDay: number = (currentDate.getDay() + 6) % 7
    let daysForLastFriday: number = 3
    let daysForCurrentThursday: number = 3

    const endOfPeriod = new Date(currentDate)
    endOfPeriod.setDate(currentDate.getDate() - currentDay + daysForCurrentThursday)

    const startOfPeriod = new Date(currentDate)
    startOfPeriod.setDate(currentDate.getDate() - currentDay - daysForLastFriday)

    const startDate = dateFormat(startOfPeriod)
    const endDate = dateFormat(endOfPeriod)

    return { startDate, endDate }
}

export function getLastQuarter(currentDate = new Date()) {
    const currentMonth = currentDate.getMonth()
    const currentYear = currentDate.getFullYear()
    const currentQuarter = Math.floor(currentMonth / 3) + 1
    const previousQuarter = currentQuarter - 1

    const startOfPreviousQuarter = new Date(currentYear, (previousQuarter - 1) * 3, 1)
    const endOfPreviousQuarter = new Date(currentYear, previousQuarter * 3, 0)

    const startDate = dateFormat(startOfPreviousQuarter)
    const endDate = dateFormat(endOfPreviousQuarter)
    return { startDate, endDate }
}

export function getLastMonth(currentDate = new Date()) {
    const currentMonth = currentDate.getMonth()
    const currentYear = currentDate.getFullYear()
    const lastMonthStartDate = new Date(currentYear, currentMonth - 1, 1)
    const lastMonthEndDate = new Date(currentYear, currentMonth, 0)

    const startDate = dateFormat(lastMonthStartDate)
    const endDate = dateFormat(lastMonthEndDate)
    return { startDate, endDate }
}

export function getLastYear(currentDate = new Date()) {
    const currentYear = currentDate.getFullYear()
    const lastYearStartDate = new Date(currentYear - 1, 0, 1)
    const lastYearEndDate = new Date(currentYear, 0, 0)

    const startDate = dateFormat(lastYearStartDate)
    const endDate = dateFormat(lastYearEndDate)
    return { startDate, endDate }
}

export const mapDistrictNameToShortName = (name: string) => {
    const map = new Map<string, string>([
        ['Центральный Федеральный округ', 'ЦФО'],
        ['Северо-Западный Федеральный округ', 'СЗФО'],
        ['Северо-Кавказский Федеральный округ', 'СКФО'],
        ['Южный Федеральный округ', 'ЮФО'],
        ['Приволжский Федеральный округ', 'ПФО'],
        ['Уральский Федеральный округ', 'УФО'],
        ['Сибирский Федеральный округ', 'СФО'],
        ['Дальневосточный Федеральный округ', 'ДФО']
    ])
    return map.get(name)
}

export const mapDistrictShortNameToName = (name: string) => {
    const map = new Map<string, string>([
        ['ЦФО', 'Центральный Федеральный округ'],
        ['СЗФО', 'Северо-Западный Федеральный округ'],
        ['СКФО', 'Северо-Кавказский Федеральный округ'],
        ['ЮФО', 'Южный Федеральный округ'],
        ['ПФО', 'Приволжский Федеральный округ'],
        ['УФО', 'Уральский Федеральный округ'],
        ['СФО', 'Сибирский Федеральный округ'],
        ['ДФО', 'Дальневосточный Федеральный округ']
    ])

    return map.get(name)
}

export const mapStatusToIcon = {
    SUCCESS: 'mdi-check-circle',
    FAILURE: 'mdi-alert-circle',
    REVOKED: 'mdi-stop-circle',
    STARTED: 'mdi-progress-clock',
    PROGRESS: 'mdi-progress-clock',
    UNKNOWN: 'mdi-information-outline'

}
export const mapStatusToColor = {
    SUCCESS: 'success',
    FAILURE: 'error',
    REVOKED: 'error',
    STARTED: 'info',
    PROGRESS: 'info',
    UNKNOWN: 'gray'
}

export const formatDuration = (seconds: number) => {
    if (!seconds && seconds !== 0) return '-'

    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const remainingSeconds = Math.floor(seconds % 60)

    if (hours > 0) {
        return `${hours} ч ${minutes} мин ${remainingSeconds} сек`
    }
    if (minutes > 0) {
        return `${minutes} мин ${remainingSeconds} сек`
    }
    return `${remainingSeconds} сек`
}


export const formatDate = (dateString: string) => {
    if (!dateString) return '-'
    const date = new Date(dateString)
    const pad = (num: number) => String(num).padStart(2, '0')
    return `${pad(date.getDate())}.${pad(date.getMonth() + 1)}.${date.getFullYear()} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}