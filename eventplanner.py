from datetime import datetime
from eventplanner_csv import *


def print_event_schedule(activities, event):
    event_act = [a for a in activities if a["event"] == event]
    event_act = sorted(event_act, key=lambda x: x["activity_start"])

    for a in event_act:
        print("{} \nat {} from {} to {}\norganized by{}\n".format(
            a["name"],
            a["activity_location"],
            a["activity_start"].strftime("%H:%M"),
            a["activity_end"].strftime("%H:%M"),
            a["staff"]
        ))


def prepare_activities_map(activities):
    ... 


if __name__ == "__main__":
    org_staff = import_staff("test_data/staff.csv")
    locs = import_locations("test_data/locations.csv")
    evs = import_events("test_data/events.csv")

    activities = import_activities(
        "test_data/activities.csv",
        staff=org_staff,
        locations=locs,
        events=evs
    )

    print_event_schedule(activities, "SummerSchool2020")
