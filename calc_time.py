from tzlocal    import get_localzone_name
from pytz       import timezone
from datetime   import datetime

def add_local_tz (datetimeObj):
    zone = timezone (get_localzone_name ())
    return zone.localize (datetimeObj)

def to_utc (datetimeObj):
    return datetimeObj.astimezone (timezone ("UTC"))
