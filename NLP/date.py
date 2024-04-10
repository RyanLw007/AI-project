from datetime import datetime, timedelta
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
def date_conversion(weekday):
    index = weekdays.index(weekday)
    today = datetime.today()
    todayindex = today.weekday()
    if todayindex == index:
        return datetime.today() + timedelta(days=7)
    else :
        if today.weekday() < index:
            return datetime.today() + timedelta(days=(index - todayindex))
        else :
            return datetime.today() + timedelta(days=7 - today.weekday() + index)


print(date_conversion("sunday").strftime("%Y-%m-%d"))
