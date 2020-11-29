from time_object import Time
import pickle
from scheduler import scheduler, Schedule, scheduler_print
import os


def time_converter(time_list):
    """inputs list of times (ex. sun-2:30pm) creates identical list of Time objects"""
    time_dict = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thur": 4, "fri": 5, "sat": 6}
    new_time = []
    for item in time_list:
        time_split = item.split("-")
        # time_split[0] is the day
        day = time_dict[time_split[0]]
        # time_split[1] is the time of which the format is hour:minute
        time_split[1] = time_split[1].replace("am", "")
        time_split[1] = time_split[1].replace("pm", "")
        time_split2 = time_split[1].split(":")
        hour = int(time_split2[0])
        if len(time_split2) > 1:
            minute = int(time_split2[1])
        else:
            minute = 0
        # account for am or pm
        if hour == 0 or item[-2] == "p" and hour != 12:
            hour += 12
        # creates time object
        time = Time(day, hour, minute)
        new_time.append(time)
    return new_time


def pickle_reader(person, event):
    """ reads in pickle based on person and event and outputs Schedule object"""
    # if pickle doesnt exist return blank string
    if not os.path.isfile(f"schedule/{event}_{person}.pickle"):
        return ""
    with open(f"schedule/{event}_{person}.pickle", "rb") as f:
        output = pickle.load(f)
    # output[0] is name and output[1] is a list of times they are free
    name = output
    time_list = []
    if isinstance(output, list):
        time_list = time_converter(output[1])
        name = output[0]
    return Schedule(name, time_list)


def optimal_time(event):
    """input event name, outputs optimal time to meet"""
    event_name = event.replace(" ", "")
    with open(f"events/{event_name}.pickle", "rb") as f:
        output = pickle.load(f)
    # creates a list of people and their info
    schedule_list = []
    for person in [
        output["name1"],
        output["name2"],
        output["name3"],
        output["name4"],
        output["name5"],
    ]:
        # if the person exists, append it to the list
        if os.path.isfile(f"schedule/{event_name}_{person}.pickle"):
            schedule_list.append(pickle_reader(person, event_name))
    length = int(output["meetingTime"].replace(" min", ""))
    # run scheduler function from scheduler mod
    optimal = scheduler(schedule_list, length)
    return optimal


def main():
    print(optimal_time("Input Event Name"))


if __name__ == "__main__":
    main()
