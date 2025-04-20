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

# maximum points: 10
def x_points (start: datetime, end: datetime) -> list:
    difference = end - start

    if difference >= timedelta (minutes = 1):
        if difference < timedelta (hours = 1):
            start = start - timedelta (seconds = start.second)
            end = start - timedelta (seconds = end.second)

            increment = timedelta (minutes = 1)
            pointsTemp = [start]
            totalRange = range (difference.seconds // 60)

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
        # sorry... what?
        pass
    
    # print (difference)

x_points (datetime(2025, 4, 20, 12, 0, 0), datetime(2025, 4, 20, 12, 59, 0))