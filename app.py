from flask import Flask, render_template, url_for, request, redirect
import pickle
import os
from werkzeug.datastructures import ImmutableMultiDict
from converter import optimal_time

# set FLASK_APP=app.py
# set FLASK_ENV=development
# flask run

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/host", methods=["GET", "POST"])
def host():
    if request.method == "POST":
        event = request.form
        event_name = event["InputEventName"].replace(" ", "")
        if not os.path.isfile(f"events/{event_name}.pickle"):
            event_dict = ImmutableMultiDict.to_dict(event)
            with open(f"events/{event_name}.pickle", "wb") as f:
                pickle.dump(event_dict, f)
        else:
            return "EVENT NAME ALREADY EXISTS"  # need help
        if event:
            return redirect(f"/{event_name}")
    return render_template("hostpage.html")


@app.route("/<name>", methods=["GET", "POST"])
def event(name):
    if not os.path.isfile(f"events/{name}.pickle"):
        return "EVENT DOES NOT EXIST"
    with open(f"events/{name}.pickle", "rb") as f:
        output = pickle.load(f)
    optimal = ""
    free = ""
    if request.method == "POST":
        schedule = request.form
        person = ["Kevin"]
        schedule_list = []
        for item in schedule:
            schedule_list.append(item)
        person.append(schedule_list)
        with open(f"schedule/{person[0]}{name}.pickle", "wb") as f:
            pickle.dump(person, f)
        scheduler_output = optimal_time(output["InputEventName"])
        optimal = f"From {scheduler_output[0][1]} to {scheduler_output[0][2]}. "
        free = ""
        for blocks in scheduler_output[0][3]:
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

    return render_template(
        "scheduler.html",
        event=output["InputEventName"],
        name1=output["name1"],
        name2=output["name2"],
        name3=output["name3"],
        name4=output["name4"],
        name5=output["name5"],
        length=output["meetingTime"],
        optimal=optimal,
        detail=free,
    )


# if __name__ host== "__main__":
#     app.run(debug=True)