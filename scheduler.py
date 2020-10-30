### creating objects for schedule and related functions
### the scheduler will be built on 15 minute intervals starting from 00:00 to 23:59


class Time:
    """Time represents the time of the day and the day of the week

    attributes: day, hour, minute
    day: [sunday = 0, monday = 1, tuesday = 2, wednesday = 3, thursday = 4, friday = 5, saturday = 6]
    """


def print_time(time):
    """prints time object for testing"""
    day = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    print(f"{time.hour:02}:{time.minute:02} {day[time.day]}")


def blank_schedule():
    """we will use 15 min block schedules for 24 hours a day, every day of the week
    a first dictionary contains keys 0 - 6 representing the week
    a nested dictionary contains keys 0-23 representing 24 hours
    a nested list contains four boolean objects representing availability in minutes from 0-15, 15-30, 30-45, 45-60

    function returns a blank schedule with no availabilities
    """
    schedule = {}
    for day in range(7):
        hour_schedule = {}
        for hour in range(24):
            hour_schedule[hour] = [False, False, False, False]
        schedule[day] = hour_schedule
    return schedule


def minute_to_block(time):
    """converts time.minute to block time"""
    if time.minute < 15:
        return 0
    elif 15 <= time.minute < 30:
        return 1
    elif 30 <= time.minute < 45:
        return 2
    else:
        return 3


def change_schedule(schedule, time, available):
    """changes the availability of one block of time
    input schedule, start of avaiability, available or unavailable in boolean

    returns new schedule
    """
    schedule[time.day][time.hour][minute_to_block(time)] = available
    return schedule


def schedule_maker(*time_range):
    """puts in range of avaiable times in tuple format, outputs schedule in dictionary"""
    pass


def error_check(time_range):
    """makes sure tuples are in order or returns error"""


from pprint import pprint

now = Time()
now.day = 5
now.hour = 0
now.minute = 31
print_time(now)
schedule = blank_schedule()
print(schedule)
change_schedule(schedule, now, True)
pprint(schedule)
