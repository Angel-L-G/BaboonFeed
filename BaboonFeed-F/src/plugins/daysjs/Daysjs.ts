import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import localizedFormat from 'dayjs/plugin/localizedFormat'

dayjs.extend(relativeTime)
dayjs.extend(localizedFormat)

export const formatDate = (dateStr: string) => {
    const now = dayjs()
    const date = dayjs(dateStr)
    const diffHours = now.diff(date, 'hour')

    if (diffHours < 24) {
        return dayjs(dateStr).fromNow(true)
    } else {
        return date.format('MMM D')
    }
}
