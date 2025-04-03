from tzlocal    import get_localzone_name
from pytz       import timezone

def add_local_tz (datetimeObj):
    zone = timezone (get_localzone_name ())
    return zone.localize (datetimeObj)
