from tzlocal    import get_localzone_name
from pytz       import timezone
from datetime   import datetime
from datetime   import timedelta

def current_time ():
    return add_local_tz(datetime.today ())

def add_local_tz (datetimeObj: datetime):
    zone = timezone (get_localzone_name ())
    return zone.localize (datetimeObj)

def to_utc (datetimeObj: datetime):
    return datetimeObj.astimezone (timezone ("UTC"))

def weekdays () -> list:
    weeklist = []
    today = current_time ()
    for n in range (7):
        weeklist.append ((today - timedelta (days = n)).weekday ())
    return weeklist