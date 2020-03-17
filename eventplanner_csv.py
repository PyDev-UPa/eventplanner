"""Eventplanner csv importer - just a helper module for separation of import
logic from other logic"""

import csv
from datetime import datetime


def import_staff(file):
    staff = []
    with open(file) as f:
        reader = csv.reader(f)
        for r in reader:
            staff.append(r[0])
    return staff


def import_locations(file):
    locs = []
    with open(file) as f:
        reader = csv.reader(f)
        for r in reader:
            locs.append(r[0])
    return locs


def import_events(file):
    events = []
    with open(file) as f:
        reader = csv.reader(f)
        for r in reader:
            event_name = r[0]
            event_start = datetime.strptime(r[1], "%d.%m.%Y")
            event_end = datetime.strptime(r[2], "%d.%m.%Y")

            new_event = {
                "name": event_name,
                "start": event_start,
                "end": event_end
            }

            events.append(new_event)
    return events


def import_activities(file, staff=None, locations=None, events=None):
    activities = []
    with open(file) as f:
        reader = csv.reader(f)
        for r in reader:
            act_event = r[0]
            if events:
                assert act_event in [e["name"] for e in events], \
                    "{} not in defined events".format(act_event)

            act_name = r[1]

            act_staff = r[2].split("|")
            if staff:
                for s in act_staff:
                    assert s in staff, \
                        "{} not in defined staff".format(s)

            act_start = datetime.strptime(r[3], "%d.%m.%Y %H:%M")
            act_end = datetime.strptime(r[4], "%d.%m.%Y %H:%M")

            act_loc = r[5]
            if locations:
                assert act_loc in locations, \
                    "{} not in defined events".format(act_loc)

            new_activity = {
                "event": act_event,
                "name": act_name,
                "staff": act_staff,
                "activity_start": act_start,
                "activity_end": act_end,
                "activity_location": act_loc
            }
            activities.append(new_activity)
    return activities
