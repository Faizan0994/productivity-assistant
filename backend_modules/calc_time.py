from tzlocal    import get_localzone_name
from pytz       import timezone
from datetime   import datetime
from datetime   import timedelta
from copy       import deepcopy

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
    number of days.
    """

    difference = end - start

    if difference >= timedelta (minutes = 1):
        if difference < timedelta (hours = 1):
            start = start - timedelta (seconds = start.second)

            increment = timedelta (minutes = 1)
            pointsTemp = [start]
            totalRange = range (difference.seconds // 60)
        
        elif difference < timedelta (hours = 24):
            start = start - timedelta (minutes = start.minute, seconds = start.second)

            increment = timedelta (days = 1)
            pointsTemp = [start]
            totalRange = range (difference.seconds // (60 * 60))
            
        else:
            start = start - timedelta (hours = start.hour, minutes = start.minute, seconds = start.second)

            increment = timedelta (days = 1)
            pointsTemp = [start]
            totalRange = range (difference.days)
            
        for i in totalRange:
            pointsTemp.append (pointsTemp[-1] + increment)
        
        del (totalRange, increment, start, end)

        length = len (pointsTemp) 
        if length > 10:
            totalPoints = length // 10
            pointsTemp = pointsTemp [length - (totalPoints * 10):]
            
            points = []
            length = len (pointsTemp)

            for i in range (length):
                if i % totalPoints == 0:
                    points.append (pointsTemp[-(i + 1)])
            points.reverse ()
        
        else:
            points = deepcopy (pointsTemp)

        del (pointsTemp)

        
        points.insert(0, points[0] - (points[1] - points[0]))

        for i in points:
            print (i)
    else:
        raise Exception (f"x points:\ttime delta is very smale")
    
    # print (difference)

x_points (datetime(2025, 4, 3, 0, 0, 0), datetime(2025, 4, 30, 12, 0, 0))