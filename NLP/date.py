from datetime import *
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

def time_conversion(time):

    if "noon" in str(time).lower():
        return datetime.strptime("12:00", "%H:%M").strftime("%H:%M")
    if "midnight" in str(time).lower():
        return datetime.strptime("00:00", "%H:%M").strftime("%H:%M")
    if "afternoon" in str(time).lower():
        return datetime.strptime("15:00", "%H:%M").strftime("%H:%M")
    if "morning" in str(time).lower():
        return datetime.strptime("09:00", "%H:%M").strftime("%H:%M")
    if "evening" in str(time).lower():
        return datetime.strptime("18:00", "%H:%M").strftime("%H:%M")
    if "am" in str(time).lower() or "pm" in str(time).lower():
        return datetime.strptime(time, "%I%p").strftime("%H:%M")
    if str(time).isdigit():
        return datetime.strptime(time, "%H%M").strftime("%H:%M")
    if ":" in str(time):
        return datetime.strptime(time, "%H:%M").strftime("%H:%M")

print(date_conversion("sunday").strftime("%Y-%m-%d"))

print(time_conversion("2pm"))
print(time_conversion("2am"))
print(time_conversion("1400"))
print(time_conversion("14:00"))
print(time_conversion("Noon"))
print(time_conversion("midnight"))

