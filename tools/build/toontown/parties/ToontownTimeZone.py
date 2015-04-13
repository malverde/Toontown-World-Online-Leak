from datetime import datetime, timedelta, tzinfo


# In the U.S., DST starts at 2AM (standard time) on the first Sunday in April:
DST_START = datetime(1, 4, 1, 2)

# ...and it ends at 2AM (DST time; 1AM standard time) on the last Sunday in
# October, which is the first Sunday on or after October 25th:
DST_END = datetime(1, 10, 25, 1)


def forwardToSunday(dt):
    daysLeft = 6 - dt.weekday()
    if daysLeft:
        dt += timedelta(daysLeft)
    return dt


class UTC(tzinfo):
    def tzname(self, dt):
        return 'UTC'

    def utcoffset(self, dt):
        return timedelta(0)

    def dst(self, dt):
        return timedelta(0)


class ToontownTimeZone(tzinfo):
    def __init__(self):
        timeZoneInfo = config.GetString('server-timezone', 'EST/EDT/-5')
        self.stdName, self.dstName, self.stdOffset = timeZoneInfo.split('/')
        self.stdOffset = int(self.stdOffset)

    def tzname(self, dt):
        if self.dst(dt):
            return self.dstName
        else:
            return self.stdName

    def utcoffset(self, dt):
        return timedelta(hours=self.stdOffset) + self.dst(dt)

    def dst(self, dt):
        # Find the first Sunday in April, and the last in October:
        start = forwardToSunday(DST_START.replace(year=dt.year))
        end = forwardToSunday(DST_END.replace(year=dt.year))

        if start <= dt.replace(tzinfo=None) < end:
            return timedelta(hours=1)
        else:
            return timedelta(0)
