from datetime import datetime, timedelta
from backend_modules.database import (most_used_app, 
                                      time_spent, 
                                      cordinates, 
                                      app_usage,
                                      all_programs,
                                      add_daily_limit,
                                      all_daily_limits,
                                      NoRecordFound)
from backend_modules.calc_time import (current_time, 
                                       to_utc, 
                                       convert_seconds, 
                                       weekdays, 
                                       x_points, 
                                       total_hours)

def convert_weekdays(weekdays) -> list:
    """
    Converts the weekdays from 0-6 to values prior to taking modulus 7.
    This is done to prevent the graph from distorting due to default sorting of pyqtgraph
    """

    newWeekDays = []
    factor = 0
    for i in range (len(weekdays)):
        val = weekdays[i]
        if i == 0:
            newWeekDays.append(val)
            continue # for the first element, no need to add factor
        prev = weekdays[i - 1]
        if val <= prev: # detect restart of week
            factor += 7
        newWeekDays.append(val + factor)
    return newWeekDays


def daily_limit(appName, limit):
    appId = appIds[appNames.index(appName)] # Get corresponding appId
    add_daily_limit(appId, limit)


def limitsInfo():
    limits = all_daily_limits()
    limitedAppNames = [item[1] for item in limits]
    limitedAppLimits = [item[2] for item in limits]
    limitedAppLimits = [f"{item // 60}h {item % 60}m" for item in limitedAppLimits]
    limitedAppUsage = [item[1] for target in limitedAppNames for item in appUsageList if item[0] == target] # Don't worry, it works :)
    return list(zip(limitedAppNames, limitedAppUsage, limitedAppLimits))


midnight = datetime.combine(datetime.today(), datetime.min.time()).isoformat()
lastMidnight = datetime.combine(datetime.today() - timedelta(days=1), datetime.min.time()).isoformat()
currentTime = current_time().isoformat()
startOfWeek = (current_time() - timedelta(weeks=1)).isoformat()
startOfLastWeek = (current_time() - timedelta(weeks=2)).isoformat()
try:
    mostUsedApp = most_used_app(midnight, currentTime) [0] # first element is the name of the app
except NoRecordFound:
    mostUsedApp = "--"
# calculate screen time
timeSpentSeconds = int(time_spent(midnight, currentTime).total_seconds())
timeSpent = convert_seconds(timeSpentSeconds)
yesterdayTimeSpentSeconds = int(time_spent(lastMidnight, midnight).total_seconds())
yesterdayTimeSpent = convert_seconds(yesterdayTimeSpentSeconds)
weeklyTimeSpentSeconds = int(time_spent(startOfWeek, currentTime).total_seconds())
weeklyTimeSpent = convert_seconds(weeklyTimeSpentSeconds)
lastWeekTimeSpentSeconds = int(time_spent(startOfLastWeek, startOfWeek).total_seconds())
lastWeekTimeSpent = convert_seconds(lastWeekTimeSpentSeconds)
lastDayComparison = timeSpent[0] - yesterdayTimeSpent[0]
lastWeekComparison = weeklyTimeSpent[0] - lastWeekTimeSpent[0]

# For comparison with previous day
lastDayComparisonString = ""
if lastDayComparison > 0:
    lastDayComparisonString = f"{lastDayComparison}h more than yesterday"
elif lastDayComparison < 0:
    lastDayComparison *= -1
    lastDayComparisonString = f"{lastDayComparison}h less than yesterday"
else:
    lastDayComparisonString = "almost same as yesterday"
# For comparison with previous week
lastWeekComparisonString = ""
if lastWeekComparison > 0:
    lastWeekComparisonString = f"{lastWeekComparison}h more than last week"
elif lastWeekComparison < 0:
    lastWeekComparison *= -1
    lastWeekComparisonString = f"{lastWeekComparison}h less than last week"
else:
    lastWeekComparisonString = "almost same as last week"


# Readable string format of time spent
screenTimeToday = f"{timeSpent[0]}h {timeSpent[1]}m {timeSpent[2]}s"
screenTimeThisWeek = f"{weeklyTimeSpent[0]}h {weeklyTimeSpent[1]}m {weeklyTimeSpent[2]}s"

now = current_time ()
xPoints = x_points (now - timedelta (weeks = 1), now)
axis = cordinates (xPoints)
xPoints = [weekdays (point [0]) for point in axis]
xPoints = convert_weekdays(xPoints)
yPoints = [total_hours (point [1]) for point in axis]

# Apps used in the current week
appUsageList = app_usage (startOfWeek, currentTime)
appList = [data[0] for data in appUsageList]
usageList = [int(data[1].total_seconds()) for data in appUsageList]
usageData = [convert_seconds(data) for data in usageList]
usageStrings = [f"{data[0]}h {data[1]}m {data[2]}s" for data in usageData]
appUsageList = list(zip(appList, usageStrings))

# All the apps in record
apps = all_programs()
appIds = [app[0] for app in apps]
appNames = [app[1] for app in apps]

limitsData = limitsInfo()
