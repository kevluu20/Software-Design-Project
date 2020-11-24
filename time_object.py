### creating objects for schedule and related functions
### the scheduler will be built on 15 minute intervals starting from 00:00 to 23:59


class Time:
    """Time represents the time of the day and the day of the week

    attributes: day, hour, minute
    day: [sunday = 0, monday = 1, tuesday = 2, wednesday = 3, thursday = 4, friday = 5, saturday = 6]
    """

    def __init__(self, day=0, hour=0, minute=0):
        """input day as integer 0-6, hour as integer 0-23, minute as integer 0-59"""
        self.day = day
        self.hour = hour
        self.minute = minute

    def __str__(self):
        """string obj for"""
        day = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        return f"{day[self.day]} {self.hour:02}:{self.minute:02}"

    def __gt__(self, other):
        """compares 2 Times to create special method: greater than"""
        if self.day > other.day:
            return True
        elif self.day < other.day:
            return False
        elif self.hour > other.hour:
            return True
        elif self.hour < other.hour:
            return False
        elif self.minute > other.minute:
            return True
        elif self.minute < other.minute:
            return False
        return False

    def __add__(self, minutes):
        """input time object and int of minutes, returns new time"""
        # copies self into new_time and adds extra muinutes
        new_time = Time(self.day, self.hour, self.minute + minutes)
        # turns extra minutes to hours
        if new_time.minute >= 60:
            extra = int(new_time.minute / 60)
            new_time.minute -= 60 * extra
            new_time.hour += extra
        # turns extra hours to days
        if new_time.hour >= 24:
            extra = int(new_time.hour / 24)
            new_time.hour -= 24 * extra
            new_time.day += extra
        # sets extra days to max saturday
        if new_time.day >= 7:
            new_time.day = 6
        return new_time

    def time_difference(self, other):
        """input 2 time objects, returns difference minutes"""
        difference = (other.day - self.day) * 24 * 60
        difference += (other.hour - self.hour) * 60
        difference += other.minute - self.minute
        return difference

    def minute_to_block(self):
        """converts time to block time"""
        if self.minute < 30:
            return 0
        return 1


def main():

    from pprint import pprint

    now = Time()
    now.day = 5
    now.hour = 0
    now.minute = 31
    t2 = Time()
    t2.day = 6
    t2.hour = 0
    t2.minute = 29
    # print_time(now)
    # schedule = blank_schedule()
    # print(schedule)
    # change_schedule(schedule, now, True)
    # pprint(schedule)


if __name__ == "__main__":
    main()
