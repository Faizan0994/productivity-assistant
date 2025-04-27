from datetime import datetime, timedelta
from backend_modules.database import most_used_app, time_spent
from backend_modules.calc_time import current_time, to_utc, convert_seconds

midnight = to_utc(datetime.combine(datetime.today(), datetime.min.time())).isoformat()
lastMidnight = to_utc(datetime.combine(datetime.today() - timedelta(days=1), datetime.min.time())).isoformat()
currentTime = to_utc(current_time()).isoformat()
startOfWeek = to_utc(current_time() - timedelta(weeks=1)).isoformat()
startOfLastWeek = to_utc(current_time() - timedelta(weeks=2)).isoformat()

mostUsedApp = most_used_app(midnight, currentTime)[0] # first element is the name of the app
# calculate screen time
timeSpentSeconds = int(time_spent(midnight, currentTime).total_seconds())
timeSpent = convert_seconds(timeSpentSeconds)
yesterdayTimeSpentSeconds = int(time_spent(lastMidnight, midnight).total_seconds())
yesterdayTimeSpent = convert_seconds(yesterdayTimeSpentSeconds)
weeklyTimeSpentSeconds = int(time_spent(midnight, currentTime).total_seconds())
weeklyTimeSpent = convert_seconds(timeSpentSeconds)
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
    lastDayComparisonString = "same as yesterday"
# For comparison with previous week
lastWeekComparisonString = ""
if lastWeekComparison > 0:
    lastWeekComparisonString = f"{lastWeekComparison}h more than last week"
elif lastWeekComparison < 0:
    lastWeekComparison *= -1
    lastWeekComparisonString = f"{lastWeekComparison}h less than last week"
else:
    lastWeekComparisonString = "same as last week"


# Readable string format of time spent
screenTimeToday = f"{timeSpent[0]}h {timeSpent[1]}m {timeSpent[2]}s"
screenTimeThisWeek = f"{weeklyTimeSpent[0]}h {weeklyTimeSpent[1]}m {weeklyTimeSpent[2]}s"