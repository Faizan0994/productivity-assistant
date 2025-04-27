from tzlocal    import get_localzone_name
from pytz       import timezone
from datetime   import datetime
from datetime   import timedelta

def current_time () -> datetime:
    return add_local_tz(datetime.today ())

def add_local_tz (datetimeObj: datetime) -> datetime:
    zone = timezone (get_localzone_name ())
    return zone.localize (datetimeObj)

def to_utc (datetimeObj: datetime) -> datetime:
    return datetimeObj.astimezone (timezone ("UTC"))

def x_points (start: datetime, end: datetime) -> list:
    """
    This scary function returns the list of maximum 10
    points of any given range between 1 minute to  any 
    number of days. Drops time from start if can't fit
    time in the range of 10.
    """
    
    difference = end - start

    if difference >= timedelta (minutes = 1):
        if difference < timedelta (hours = 1):
            end = end - timedelta (seconds = end.second)
            decrement = timedelta (minutes = 1)
        elif difference < timedelta (days = 1):
            end = end - timedelta (minutes = end.minute, seconds = end.second)
            decrement = timedelta (hours = 1)
        else:
            end = end - timedelta (hours = end.hour, minutes = end.minute, seconds = end.second)
            decrement = timedelta (days = 1)

        unitTime = int (difference.total_seconds () // decrement.total_seconds ())
        rows = int (unitTime // 10)
        points = []

        if rows == 0:
            itter = range (unitTime + 1)
        else:
            itter = range (11)
            decrement = decrement * rows 
        
        for n in itter:
                points.append(end - (n * decrement))        
        points.reverse ()

        return points
    else:
        class SmallInterval (Exception):
            def __init__(self, message):
                self.message = message
                super().__init__(message)
            def __str__ (self):
                return self.message
        raise SmallInterval (f"The interval is small: {difference}")
    
def weekdays (datetimeObj: datetime) -> int:
    return datetimeObj.weekday ()

def total_hours (timedeltaObj: timedelta):
    return timedeltaObj.total_seconds () / 3600

def convert_seconds(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return (hours, minutes, seconds)