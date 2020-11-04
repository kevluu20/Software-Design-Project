from time_object import Time
from copy import copy


class Schedule:
    """schedule object that contains attributes:
    name: the name of the schedule
    availability: dictionary schedule maker
    """

    def __init__(self, name="Unclaimed", time_list=[]):
        self.name = name
        self.availability = schedule_maker(time_list)

    def __str__(self):
        """prints schedule object"""
        schedule_list = self.schedule_to_time()
        output = f"{self.name} is free from "
        for start, end in schedule_list:
            output += f"{start} to {end}; "
        return output

    def schedule_check(self, time):
        """for testing: checks whether you are free at time"""
        print(self.availability[time.day][time.hour][Time.minute_to_block(time)])

    def schedule_to_time(self):
        """converts schedule to time tuples in a list format"""
        time_list = []
        for day in self.availability:
            for hour in self.availability[day]:
                for i in range(len(self.availability[day][hour])):
                    if self.availability[day][hour][i]:
                        time = Time()
                        time.day = day
                        time.hour = hour
                        time.minute = i * 15
                        time_list.append(time)
        output = []
        for i in range(len(time_list)):
            if i == 0:
                start = time_list[0]
            elif i == len(time_list) - 1:
                end = Time.time_add(time_list[-1], 15)
                output.append((start, end))
            elif Time.time_difference(time_list[i], time_list[i + 1]) > 15:
                end = Time.time_add(time_list[i], 15)
                output.append((start, end))
                start = time_list[i + 1]
        return output


def blank_schedule():
    """we will use 15 min block schedules for 24 hours a day, every day of the week
    a first dictionary contains keys 0 - 6 representing the day
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


def change_schedule(schedule, time, available):
    """changes the availability of one block of time
    input schedule, start of avaiability, available or unavailable in boolean

    returns new schedule
    """
    schedule[time.day][time.hour][Time.minute_to_block(time)] = available
    return schedule


def schedule_maker(time_list):
    """list of range of avaiable times in tuple format, outputs schedule in dictionary"""
    schedule = blank_schedule()

    for starttime, endtime in time_list:
        if Time.time_difference(starttime, endtime) < 0:
            return "Error: time range(s) not in order"
        start = copy(starttime)
        end = copy(endtime)
        while start.minute % 15 != 0:
            start.minute += 1
        while end.minute % 15 != 0:
            end.minute -= 1
        difference = Time.time_difference(start, end)
        while difference > 0:
            schedule = change_schedule(schedule, start, True)
            # schedule_check(schedule, start)
            # print_time(start)
            # print(schedule)
            start = Time.time_add(start, 15)
            difference -= 15

    return schedule


def master_schedule(schedule_list):
    """inputs list of all schedule objects
    program determines best time to meet by assigning Schedule.name to each time block in a master schedule
    outputs master schedule"""
    master = Schedule()
    master.name = "Master"
    master.availability = blank_schedule()
    for day in master.availability:
        for hour in master.availability[day]:
            for i in range(len(master.availability[day][hour])):
                block_list = []
                for schedule in schedule_list:
                    if schedule.availability[day][hour][i]:
                        block_list.append(schedule.name)
                time = Time()
                time.day = day
                time.hour = hour
                time.minute = i * 15
                if len(block_list) > 0:
                    change_schedule(master.availability, time, block_list)
    return master


def scheduler(schedule_list, meeting_length, meeting_restrict, options):
    """inputs:
    schedule_list: list of Schedule object with everyone's avaiability
    meeting_length: how long the meeting should take by 15 minute intervals ex: 15, 30, 45, 60, 75, etc.
    meeting_restrict: schedule object with restricted times
    options: int of number of options to show
    """
    pass


t1 = Time()
t2 = Time(1, 5, 30)
t3 = Time(2, 12, 45)
t4 = Time(4, 6, 15)
print(t2)
print(t1)
brandon = Schedule("Brandon", [(t1, t2), (t3, t4)])
from pprint import pprint

pprint(brandon.availability)
print(brandon)
