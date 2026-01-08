from datetime import datetime

def get_first_activity_date(booking):
    dates = []

    for pkg_act in booking["pkg"]["packageActivities"]:
        for d in pkg_act["activity"]["activityDates"]:
            dates.append(datetime.strptime(d, "%d-%m-%Y").date())

    return min(dates)
