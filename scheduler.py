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
        return self.availability[time.day][time.hour][Time.minute_to_block(time)]

    def schedule_to_time(self):
        """converts schedule to time tuples in a list format"""
        time_list = []
        for day in self.availability:
            for hour in self.availability[day]:
                for i in range(len(self.availability[day][hour])):
                    if self.availability[day][hour][i]:
                        time = Time(day, hour, i * 30)
                        time_list.append(time)
        output = []
        for i in range(len(time_list)):
            if i == 0:
                start = time_list[0]
            elif i == len(time_list) - 1:
                end = time_list[-1] = 30
                output.append((start, end))
            elif Time.time_difference(time_list[i], time_list[i + 1]) > 30:
                end = time_list[i] + 30
                output.append((start, end))
                start = time_list[i + 1]
        return output


def blank_schedule():
    """we will use 30 min block schedules for 24 hours a day, every day of the week
    a first dictionary contains keys 0 - 6 representing the day
    a nested dictionary contains keys 0-23 representing 24 hours
    a nested list contains four boolean objects representing availability in minutes from 0-30, 30-60

    function returns a blank schedule with no availabilities
    """
    schedule = {}
    for day in range(7):
        hour_schedule = {}
        for hour in range(24):
            hour_schedule[hour] = [False, False]
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
        while start.minute % 30 != 0:
            start.minute += 1
        while end.minute % 30 != 0:
            end.minute -= 1
        difference = Time.time_difference(start, end)
        while difference > 0:
            schedule = change_schedule(schedule, start, True)
            # schedule_check(schedule, start)
            # print_time(start)
            # print(schedule)
            start = start + 30
            difference -= 30

    return schedule


def master_schedule(schedule_list):
    """inputs list of all schedule objects
    program determines best time to meet by assigning Schedule.name to each time block in a master schedule
    outputs master schedule"""
    master = Schedule("Master")
    master.availability = blank_schedule()
    for day in master.availability:
        for hour in master.availability[day]:
            for i in range(len(master.availability[day][hour])):
                block_list = []
                for schedule in schedule_list:
                    if schedule.availability[day][hour][i]:
                        block_list.append(schedule.name)
                time = Time(day, hour, i * 30)
                if len(block_list) > 0:
                    change_schedule(master.availability, time, block_list)
                else:
                    change_schedule(master.availability, time, [])
    return master


def scheduler(schedule_list, meeting_length, reverse=False):
    """inputs:
    schedule_list: list of Schedule object with everyone's avaiability
    meeting_length: how long the meeting should take by 30 minute intervals ex: 30, 60, 90 etc.
    """
    master = master_schedule(schedule_list)
    while meeting_length % 30 != 0:
        meeting_length += 1
    time_list = []
    for day in master.availability:
        for hour in master.availability[day]:
            for i in range(len(master.availability[day][hour])):
                if len(master.availability[day][hour][i]) > 0:
                    start = Time(day, hour, i * 30)
                    # print(master.schedule_check(start))
                    end = start + meeting_length
                    total = 0
                    people_list = []
                    for t in range(int(meeting_length / 30)):
                        time = start + t * 30
                        total = total + len(
                            master.availability[time.day][time.hour][
                                int(time.minute / 30)
                            ]
                        )
                        people_list.append([time, master.schedule_check(time)])
                    time_list.append([100 / total, start, end, people_list])
    output = sorted(time_list, reverse=reverse)
    return output
    # l = len(master.availability[day][hour][i])
    # print(master.availability[day][hour][i], time, l)


def scheduler_print(output, options, reverse=False):
    """prints best options sorted by: best score(calculated by number of available people), earliest time
    scheduler_output: list from scheduler output
    options: int of options to print
    prints strings
    """
    scheduler_output = sorted(output, reverse=reverse)
    while options > len(scheduler_output):
        options -= 1
    for i in range(options):
        free = f"From {scheduler_output[i][1]} to {scheduler_output[i][2]}. "
        for blocks in scheduler_output[i][3]:
            if len(blocks[1]) == 0:
                free += f"""
                No one is free from {blocks[0]} to {blocks[0]+30}."""
            elif 0 < len(blocks[1]) <= 1:
                free += f"""
                Person that is free from {blocks[0]} to {blocks[0]+30} is {blocks[1][0]}."""
            else:
                free += f"""
                People that are free from {blocks[0]} to {blocks[0]+30} are """
                for people in blocks[1]:
                    free += f"{people}"
                    if blocks[1].index(people) == len(blocks[1]) - 1:
                        free += "."
                    else:
                        free += ", "

        print(free)


# t1 = Time()
# t2 = Time(1, 5, 30)
# t3 = Time(2, 12, 45)
# t4 = Time(4, 6, 15)
# print(t2)
# print(t1)
# brandon = Schedule("Brandon", [(t1, t2), (t3, t4)])
# anna = Schedule("Anna", [(t1, t3)])
# from pprint import pprint

# master = master_schedule([anna, brandon])
# print(master.availability)
# pprint(brandon.availability)
# print(brandon)
# schedule = scheduler([anna, brandon], 90)
# for item in schedule:
#     free = f"From {item[1]} to {item[2]}. "
#     for blocks in item[3]:
#         free += f"""
#         people that are free from {blocks[0]} to {blocks[0]+15} are """
#         for people in blocks[1]:
#             free += f"{people}; "
# print(free)
b1 = Time(3, 9, 00)
b2 = Time(3, 11, 00)

b3 = Time(3, 12, 30)
b4 = Time(3, 13, 00)

b4 = Time(3, 15, 30)
b5 = Time(3, 19, 00)

b6 = Time(3, 21, 00)
b7 = Time(3, 22, 00)

k1 = Time(3, 8, 00)
k2 = Time(3, 10, 00)

k3 = Time(3, 13, 30)
k4 = Time(3, 14, 30)


brandon = Schedule("Brandon", [(b1, b2), (b3, b4), (b4, b5), (b6, b7)])
kevin = Schedule("Kevin", [(k1, k2), (k3, k4)])

schedule = scheduler([brandon, kevin], 60)
scheduler_print(schedule, 10)
