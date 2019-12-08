# TODO: document
def month_name(row):
    return row["time_step_start"].month_name()

# TODO: document
def day_name(row):
    return row["time_step_start"].day_name()

# TODO: document
def is_weekend(row):
    return row["time_step_start"].day_name() in ["Saturday", "Sunday"]

# TODO: document
def is_night(row):
    hour = row["time_step_start"].hour
    return 18 <= hour < 24 or 0 <= hour < 7

# TODO: document - meteorogical seasons 
# (https://www.timeanddate.com/calendar/aboutseasons.html)
def season(row):
    month = row["time_step_start"].month
    if 3 <= month < 6:
        return "Spring"
    if 6 <= month < 9:
        return "Summer"
    if 9 <= month < 12:
        return "Fall"
    return "Winter"

# TODO: document
def day_of_month(row):
    return row["time_step_start"].day

# TODO: document
def thirth_of_month(row):
    day = row["time_step_start"].day
    if 0 < day <= 10:
        return "First"
    if 10 < day <= 20:
        return "Second"
    if 20 < day:
        return "Third"

# TODO: document
def part_of_day(row):
    hour = row["time_step_start"].hour
    if 5 < hour <= 9:
        return "EarlyMorning"
    if 9 < hour <= 15:
        return "Midday"
    if 15 < hour <= 19:
        return "Afternoon"
    if 19 < hour <= 24:
        return "Evening"
    return "LateNight"

def hour_of_day(row):
    return row["time_step_start"].hour