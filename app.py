from flask import Flask, render_template, url_for, request, redirect
import pickle
import os
from werkzeug.datastructures import ImmutableMultiDict
from converter import optimal_time, pickle_reader
from scheduler import Schedule, blank_schedule

# set FLASK_APP=app.py
# set FLASK_ENV=development
# flask run

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # looks for post request and attempts to search for the name and event
    if request.method == "POST":
        event_name = request.form["event_name"].replace(" ", "").lower()
        person_name = request.form["person_name"].replace(" ", "")
        return redirect(f"/{event_name}/{person_name}")
    return render_template("index.html")


@app.route("/host", methods=["GET", "POST"])
def host():
    # looks for a post request and pickles info
    if request.method == "POST":
        event = request.form
        # converts event to a dictionary
        event_dict = ImmutableMultiDict.to_dict(event)
        event_name = event_dict["InputEventName"].replace(" ", "").lower()
        # saves names as list
        name_list = []
        for i in range(5):
            name = event_dict[f"name{i+1}"].replace(" ", "")
            if not name == "":
                name_list.append(name)
        if len(name_list) != len(set(name_list)):
            return render_template("errorpage.html")
        if not os.path.isfile(f"events/{event_name}.pickle"):
            # pickles info into event pickle and name pickle
            with open(f"events/{event_name}.pickle", "wb") as f:
                pickle.dump(event_dict, f)
            for name in name_list:
                with open(f"schedule/{event_name}_{name}.pickle", "wb") as p:
                    pickle.dump(name, p)
        else:
            return render_template("errorpage.html")
        if event:
            # if events exists, go to host schedule page
            return redirect(f"/{event_name}/{name_list[0]}")
    return render_template("hostpage.html")


@app.route("/<event_name>/<name>", methods=["GET", "POST"])
def event(event_name, name):
    # checks if event and person exists
    if not os.path.isfile(f"schedule/{event_name}_{name}.pickle"):
        return render_template("errorpage1.html")
    # open event pickle
    with open(f"events/{event_name}.pickle", "rb") as f:
        output = pickle.load(f)

    # writes in avaiable time of every person
    time_list = []
    check = False
    for i in range(5):
        time_name = output[f"name{i+1}"]
        # checks for case sensativity otherwise program breaks
        check = name == time_name or check
        # creates a schedule object from pickle_reader in converter and checks if it exists
        schedule = pickle_reader(time_name, event_name)
        if isinstance(schedule, str):
            time_list.append("")
        elif schedule.availability == blank_schedule():
            time_list.append(f"{time_name} has not submited their availability yet.")
        else:
            time_list.append(f"{time_name} has submited their availability.")
    if not check:
        # return render_template("errorpage1.html")
        return str(output)

    # calculates optimal time imported from converter
    scheduler_output = optimal_time(event_name)
    if len(scheduler_output) != 0:
        optimal = f"From {scheduler_output[0][1]} to {scheduler_output[0][2]}. "
    else:
        optimal = "No optimal time found."

    # looks for POST request
    if request.method == "POST":
        schedule = request.form
        person = [name]
        # converts schedule to list
        schedule_list = []
        for item in schedule:
            schedule_list.append(item)
        person.append(schedule_list)
        # opens event and name pickle and rewrites it with updated times
        with open(f"schedule/{event_name}_{person[0]}.pickle", "wb") as f:
            pickle.dump(person, f)
        # calculates optimal time imported from converter
        scheduler_output = optimal_time(event_name)
        if len(scheduler_output) != 0:
            optimal = f"From {scheduler_output[0][1]} to {scheduler_output[0][2]}. "
        else:
            optimal = "No optimal time found."
        # writes in whether people have inputted times
        time_list = []
        for i in range(5):
            time_name = output[f"name{i+1}"]
            # checks for case sensativity otherwise program breaks
            check = name == time_name or check
            # creates a schedule object from pickle_reader in converter and checks if it exists
            schedule = pickle_reader(time_name, event_name)
            if isinstance(schedule, str):
                time_list.append("")
            elif schedule.availability == blank_schedule():
                time_list.append(
                    f"{time_name} has not submited their availability yet."
                )
            else:
                time_list.append(f"{time_name} has submited their availability.")
    return render_template(
        "scheduler.html",
        event=output["InputEventName"],
        name1=output["name1"],
        name2=output["name2"],
        name3=output["name3"],
        name4=output["name4"],
        name5=output["name5"],
        time1=time_list[0],
        time2=time_list[1],
        time3=time_list[2],
        time4=time_list[3],
        time5=time_list[4],
        length=output["meetingTime"],
        optimal=optimal,
    )


# if __name__ host== "__main__":
#     app.run(debug=True)