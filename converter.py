from time_object import Time
import pickle
from scheduler import scheduler, Schedule, scheduler_print
import os


def time_converter(time_list):
    """inputs list of times (ex. sun-2pm) creates identical list of Time objects"""
    time_dict = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6}
    new_time = []
    for item in time_list:
        day = time_dict[item[0:3]]
        hour = int(item[-3])
        if item[-2] == "p":
            hour += 12
        time = Time(day, hour)
        new_time.append(time)
    return new_time


def pickle_reader(person, event):
    """ reads in pickle based on person and event and outputs Schedule object"""
    with open(f"schedule/{person}{event}.pickle", "rb") as f:
        output = pickle.load(f)
    name = output[0]
    time_list = time_converter(output[1])
    return Schedule(name, time_list)


def optimal_time(event):
    """input event name, outputs optimal time to meet"""
    event_name = event.replace(" ", "")
    with open(f"events/{event_name}.pickle", "rb") as f:
        output = pickle.load(f)
    schedule_list = []
    for person in [
        output["name1"],
        output["name2"],
        output["name3"],
        output["name4"],
        output["name5"],
    ]:
        if os.path.isfile(f"schedule/{person}{event_name}.pickle"):
            schedule_list.append(pickle_reader(person, event_name))
    length = int(output["meetingTime"].replace(" min", ""))
    optimal = scheduler(schedule_list, length)
    return optimal


def main():
    print(optimal_time("python meeting4"))


if __name__ == "__main__":
    main()
